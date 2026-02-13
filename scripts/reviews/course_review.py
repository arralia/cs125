"""
RateMyProfessor Scraper for UCI Course Reviews
================================================
Directly scrapes RMP's GraphQL API to get freeform student reviews
for COMPSCI and I&C SCI courses at UCI.

No third-party RMP libraries needed — just `requests`.

Dependencies:
    pip install requests

Usage:
    python rmp_scraper.py
    python rmp_scraper.py --max-professors 10
    python rmp_scraper.py --output reviews.json --include-meta
    python rmp_scraper.py --departments COMPSCI "I&C SCI" IN4MATX
"""

import argparse
import json
import logging
import re
import time
from collections import Counter
from pathlib import Path

import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# ─── RMP GraphQL Configuration ──────────────────────────────────────────────

RMP_GRAPHQL_URL = "https://www.ratemyprofessors.com/graphql"

# This is the well-known auth header used by RMP's frontend.
# base64("test:test") = "dGVzdDp0ZXN0"
RMP_AUTH_HEADER = "Basic dGVzdDp0ZXN0"

RMP_HEADERS = {
    "Authorization": RMP_AUTH_HEADER,
    "Content-Type": "application/json",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    ),
    "Referer": "https://www.ratemyprofessors.com/",
}

# UCI's RMP school ID. You can verify by searching on ratemyprofessors.com.
# The GraphQL ID is base64("School-1074") = "U2Nob29sLTEwNzQ="
UCI_SCHOOL_ID = 1074
UCI_SCHOOL_NODE_ID = "U2Nob29sLTEwNzQ="  # CHANGED: hardcoded from actual RMP response instead of base64 encoding
UCI_SCHOOL_NAME = "UC Irvine"

ICS_ALLOWED = {"ICS31", "ICS32", "ICS33", "ICS32A", "ICSH32", "ICS45C", "ICS46", "ICS51", "ICS53", "ICS6B", "ICS6D", "ICS139W", "ICS45J"}

# Build course → [keywords] lookup from keywords.json
def _build_course_keywords() -> dict[str, list[str]]:
    path = Path(__file__).parent.parent.parent / "data" / "keywords.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    lookup: dict[str, list[str]] = {}
    for entry in data.get("keywords", []):
        kw = entry["keyword"]
        for course in entry.get("courses", []) + entry.get("prerequisites", []):
            cid = course["id"]
            lookup.setdefault(cid, [])
            if kw not in lookup[cid]:
                lookup[cid].append(kw)
    return lookup

COURSE_KEYWORDS = _build_course_keywords()

UCI_DEPT_IDS = [
    "RGVwYXJ0bWVudC0xMQ==",    # Computer Science (id=11)
    "RGVwYXJ0bWVudC0xMzQ2",    # Informatics (id=1346)
    "RGVwYXJ0bWVudC0xMzM2",    # Computer Information Systems (id=1336)
]

# Rate limiting
REQUEST_DELAY = 1.5  # seconds between RMP requests

# ─── GraphQL Queries ─────────────────────────────────────────────────────────
# These mirror the queries RMP's own frontend makes.

SEARCH_SCHOOL_QUERY = """
query SearchSchool($query: String!) {
  newSearch {
    schools(query: { text: $query }) {
      edges {
        node {
          id
          legacyId
          name
          city
          state
        }
      }
    }
  }
}
"""

SEARCH_TEACHERS_QUERY = """
query SearchTeachers($query: TeacherSearchQuery!, $after: String) {
  newSearch {
    teachers(query: $query, first: 1000, after: $after) {
      edges {
        cursor
        node {
          id
          firstName
          lastName
          department
          numRatings
        }
      }
      pageInfo {
        hasNextPage
        endCursor
      }
    }
  }
}
"""

TEACHER_RATINGS_QUERY = """
query TeacherRatings($id: ID!, $after: String) {
  node(id: $id) {
    ... on Teacher {
      ratings(first: 1000, after: $after) {
        edges {
          node {
            comment
            class
            date
            difficultyRatingRounded
          }
        }
        pageInfo {
          hasNextPage
          endCursor
        }
      }
    }
  }
}
"""


# ─── GraphQL Client ─────────────────────────────────────────────────────────

def graphql_request(query: str, variables: dict, retries: int = 3) -> dict | None:
    """Make a GraphQL request to RMP with retry logic."""
    payload = {"query": query, "variables": variables}

    for attempt in range(retries):
        try:
            resp = requests.post(
                RMP_GRAPHQL_URL,
                json=payload,
                headers=RMP_HEADERS,
                timeout=15,
            )

            if resp.status_code == 200:
                data = resp.json()
                if "errors" in data:
                    logger.warning(f"GraphQL errors: {data['errors']}")
                return data.get("data")

            elif resp.status_code == 429:
                wait = (attempt + 1) * 5
                logger.warning(f"Rate limited (429). Waiting {wait}s...")
                time.sleep(wait)
                continue

            else:
                logger.warning(f"HTTP {resp.status_code}: {resp.text[:200]}")
                if attempt < retries - 1:
                    time.sleep(2)
                    continue
                return None

        except requests.RequestException as e:
            logger.warning(f"Request failed (attempt {attempt + 1}/{retries}): {e}")
            if attempt < retries - 1:
                time.sleep(2)
            else:
                return None

    return None


# ─── RMP Data Fetchers ───────────────────────────────────────────────────────

def search_school(name: str) -> dict | None:
    """Search for a school on RMP and return the first match."""
    data = graphql_request(SEARCH_SCHOOL_QUERY, {"query": name})
    if not data:
        return None

    edges = (
        data.get("newSearch", {})
        .get("schools", {})
        .get("edges", [])
    )
    if not edges:
        return None

    node = edges[0]["node"]
    logger.info(f"Found school: {node['name']} ({node['city']}, {node['state']}) [id={node['legacyId']}]")
    return node


def get_all_professors(school_node_id: str) -> list[dict]:
    """Fetch all professors across CS, Informatics, and CIS departments."""
    professors = {}

    for dept_id in UCI_DEPT_IDS:
        data = graphql_request(SEARCH_TEACHERS_QUERY, {
            "query": {
                "text": "",
                "schoolID": school_node_id,
                "departmentID": dept_id,
            }
        })

        if not data:
            logger.warning(f"No data returned for departmentID {dept_id}")
            continue

        edges = (
            data.get("newSearch", {})
            .get("teachers", {})
            .get("edges", [])
        )

        for edge in edges:
            prof = edge["node"]
            prof_id = prof.get("id")
            if prof_id and prof_id not in professors:
                professors[prof_id] = prof

        logger.info(f"  dept {dept_id}: {len(edges)} professors fetched")

    logger.info(f"Found {len(professors)} professors total")
    return list(professors.values())


def get_professor_ratings(teacher_node_id: str, year: int | None = None) -> list[dict]:
    """Fetch all ratings (reviews) for a professor, paginating through all pages."""
    ratings = []
    cursor = None

    while True:
        variables = {"id": teacher_node_id}
        if cursor:
            variables["after"] = cursor

        data = graphql_request(TEACHER_RATINGS_QUERY, variables)
        if not data or not data.get("node"):
            break

        node = data["node"]
        ratings_data = node.get("ratings", {})
        edges = ratings_data.get("edges", [])

        for edge in edges:
            rating = edge["node"]
            if year:
                date_str = rating.get("date") or ""
                year_match = re.match(r"(\d{4})", date_str)
                if not year_match or int(year_match.group(1)) < year:
                    continue
            cls = (rating.get("class") or "").upper().replace(" ", "").replace("&", "").replace("ICSCI", "ICS").replace("I&CSCI", "ICS")
            is_cs_upper = re.match(r"^(COMPSCI|CS)1\d{2}[A-Z]?$", cls)
            is_ics = cls in ICS_ALLOWED
            if is_cs_upper or is_ics:
                ratings.append(rating)

        page_info = ratings_data.get("pageInfo", {})
        if page_info.get("hasNextPage") and page_info.get("endCursor"):
            cursor = page_info["endCursor"]
            time.sleep(REQUEST_DELAY * 0.5)  # Slightly faster for sub-pages
        else:
            break

    return ratings


# ─── Text Analysis ───────────────────────────────────────────────────────────

STOPWORDS = set("""
a about above after again against all am an and any are as at be because been
before being below between both but by can cannot could did do does doing down
during each few for from further get got had has have having he her here hers
herself him himself his how i if in into is it its itself just let me more most
my myself no nor not now of off on once only or other our ours ourselves out over
own same she should so some such than that the their theirs them themselves then
there these they this those through to too under until up us very was we were
what when where which while who whom why will with would you your yours yourself
also really like get got one even much would could make take took going go thing
things way well good very still think know back lot something anything
said going way well take took said even just would could make back thing things
class course professor teacher lecture lectures exam exams midterm final finals
homework assignment assignments quiz quizzes grade grades grading quarter ta tas
student students took take taking taken pretty really also actually every still
""".split())

CS_DOMAIN_TERMS = set("""
algorithm algorithms data structures recursion sorting searching trees graphs
hash hashing dynamic programming greedy complexity runtime analysis proof proofs
object-oriented oop polymorphism inheritance encapsulation abstraction
python java c++ javascript assembly machine learning ai artificial intelligence
neural network deep learning nlp computer vision database sql nosql query
optimization normalization operating system systems kernel process thread
concurrency synchronization memory management network networking tcp protocol
compiler compilers parsing syntax security cryptography encryption web development
frontend backend api rest software engineering design patterns testing debugging
parallel distributed computing graphics rendering linear algebra calculus
probability statistics reinforcement learning robotics embedded functional
programming version control git ethics privacy project group
""".split())

DIFFICULTY_SIGNALS = {
    1: ["easy", "easiest", "breeze", "cakewalk", "effortless", "simple",
        "trivial", "gpa booster", "barely studied"],
    2: ["fairly easy", "not too bad", "manageable", "doable", "reasonable",
        "not difficult", "pretty chill", "laid back"],
    3: ["moderate", "average", "decent amount", "some effort", "fair",
        "balanced", "medium", "normal"],
    4: ["hard", "difficult", "challenging", "tough", "demanding", "heavy workload",
        "time consuming", "lots of work", "struggled", "not easy", "study a lot"],
    5: ["extremely hard", "hardest", "insane", "brutal", "impossible", "killer",
        "nightmare", "overwhelming", "most difficult", "weed out", "weeder",
        "soul crushing", "destroyed"],
}


def estimate_difficulty(comment: str, rmp_difficulty: float = None) -> int:
    """Estimate 1-5 difficulty from review text + optional RMP difficulty score."""
    text = comment.lower()

    if rmp_difficulty is not None and 1 <= rmp_difficulty <= 5:
        base = rmp_difficulty
    else:
        base = 3.0

    text_score = 0
    matches = 0
    for level, phrases in DIFFICULTY_SIGNALS.items():
        for phrase in phrases:
            if phrase in text:
                text_score += level
                matches += 1

    if matches > 0:
        text_avg = text_score / matches
        final = 0.6 * base + 0.4 * text_avg if rmp_difficulty else text_avg
    else:
        final = base

    return max(1, min(5, round(final)))


def extract_keywords(text: str, max_keywords: int = 10) -> list[str]:
    """Extract significant keywords from review text, boosting CS domain terms."""
    words = re.findall(r"[a-z](?:[a-z'-]*[a-z])?", text.lower())
    counts = Counter()

    for w in words:
        if w not in STOPWORDS and len(w) > 2:
            counts[w] += 1

    # Check bigrams
    for i in range(len(words) - 1):
        bigram = f"{words[i]} {words[i+1]}"
        if words[i] not in STOPWORDS and words[i+1] not in STOPWORDS:
            if bigram in CS_DOMAIN_TERMS:
                counts[bigram] += 2

    scored = {}
    for word, count in counts.items():
        score = count
        if word in CS_DOMAIN_TERMS:
            score *= 3
        if len(word) > 6:
            score *= 1.5
        scored[word] = score

    return [kw for kw, _ in sorted(scored.items(), key=lambda x: x[1], reverse=True)[:max_keywords]]


# ─── Course Name Resolution ─────────────────────────────────────────────────

DEPT_SHORTHAND = {
    "CS": "COMPSCI",
    "ICS": "I&C SCI",
    "COMP SCI": "COMPSCI",
    "COMPSCI": "COMPSCI",
    "I&CSCI": "I&C SCI",
    "I&C SCI": "I&C SCI",
    "IN4MATX": "IN4MATX",
    "INF": "IN4MATX",
    "INF": "IN4MATX",
    "SWE": "SWE",
    "STATS": "STATS",
    "STAT": "STATS",
}


def normalize_course_name(raw_class: str) -> str | None:
    """
    Normalize RMP class names like 'CS161', 'COMPSCI 161', 'ICS33' into
    standard format like 'COMPSCI 161', 'I&C SCI 33'.
    """
    if not raw_class:
        return None

    raw = raw_class.strip().upper()

    # Try to match "DEPT NUMBER" or "DEPTNUMBER" patterns
    for short, full in sorted(DEPT_SHORTHAND.items(), key=lambda x: -len(x[0])):
        escaped = re.escape(short)
        match = re.match(rf"^{escaped}\s*(\d{{1,3}}[A-Z]?)$", raw)
        if match:
            return f"{full} {match.group(1)}"

    # If it already looks like "DEPT NUM", return as-is
    if re.match(r"^[A-Z&\s]+\d{1,3}[A-Z]?$", raw):
        return raw

    return raw  # Return whatever we got


def is_target_course(course_name: str, departments: list[str]) -> bool:
    """Check if a course belongs to one of our target departments."""
    if not course_name:
        return False
    upper = course_name.upper()
    return any(upper.startswith(d.upper()) for d in departments)


# ─── Main Pipeline ───────────────────────────────────────────────────────────

def run_scraper(
    departments: list[str],
    year: int | None = None,
    limit: int | None = None,
) -> list[dict]:
    """
    Main scraping pipeline:
    1. Find UCI on RMP
    2. Get all CS-related professors
    3. For each, pull all ratings with text reviews
    4. Normalize course names, estimate difficulty, extract keywords
    """

    # ── Step 1: Verify school ──
    logger.info("=" * 60)
    logger.info("Step 1: Finding UCI on RateMyProfessor...")
    logger.info("=" * 60)

    school_id = UCI_SCHOOL_NODE_ID
    logger.info(f"School: {UCI_SCHOOL_NAME} (id={school_id})")
    
    # ── Step 2: Get professors ──
    logger.info("")
    logger.info("=" * 60)
    logger.info("Step 2: Fetching professors (this may take a few minutes)...")
    logger.info("=" * 60)

    professors = get_all_professors(school_id)
    logger.info(f"Will scrape {len(professors)} professors")

    # ── Step 3: Get reviews ──
    logger.info("")
    logger.info("=" * 60)
    logger.info("Step 3: Fetching reviews...")
    logger.info("=" * 60)

    all_reviews = []
    total = len(professors)

    for i, prof in enumerate(professors, 1):
        name = f"{prof.get('firstName', '')} {prof.get('lastName', '')}".strip()
        dept = prof.get("department", "Unknown")
        num = prof.get("numRatings", 0)

        logger.info(f"  [{i}/{total}] {name} ({dept}) — {num} ratings")

        if num == 0:
            continue

        ratings = get_professor_ratings(prof["id"], year=year)
        text_ratings = [r for r in ratings if r.get("comment", "").strip()]
        logger.info(f"    → {len(text_ratings)} text reviews")

        for rating in text_ratings:
            comment = rating.get("comment", "").strip()
            if not comment:
                continue

            # Normalize course name
            raw_class = (rating.get("class") or "").upper().replace(" ", "").replace("&", "").replace("I&CSCI", "ICS").replace("ICSCI", "ICS")
            if raw_class in ICS_ALLOWED:
                if "ICS" not in departments:
                    continue
                code = raw_class[3:]  # strip "ICS" prefix → "31", "32A", "6B", etc.
                course_name = f"I&CSCI{code}"
            else:
                if "COMPSCI" not in departments:
                    continue
                num = re.search(r"(1\d{2}[A-Z]?)$", raw_class)
                course_name = f"COMPSCI{num.group(1)}" if num else raw_class

            difficulty = estimate_difficulty(comment, rating.get("difficultyRatingRounded"))
            # keywords = extract_keywords(comment)

            review = {
                "courseName": course_name or f"UNKNOWN ({name})",
                "instructor": name,
                "difficulty": difficulty,
                "description": comment,
                "keywords": COURSE_KEYWORDS.get(course_name, [])
                # "_meta": {
                #     "professor": name,
                #     "department": dept,
                #     "rmpClass": raw_class,
                #     "difficultyRating": rating.get("difficultyRating"),
                #     "helpfulRating": rating.get("helpfulRating"),
                #     "clarityRating": rating.get("clarityRating"),
                #     "grade": rating.get("grade"),
                #     "date": rating.get("date"),
                #     "wouldTakeAgain": rating.get("wouldTakeAgain"),
                #     "tags": rating.get("ratingTags"),
                #     "thumbsUp": rating.get("thumbsUpTotal"),
                #     "thumbsDown": rating.get("thumbsDownTotal"),
                #     "isOnline": rating.get("isForOnlineClass"),
                # },
            }
            all_reviews.append(review)
            if limit and len(all_reviews) >= limit:
                return all_reviews

        time.sleep(REQUEST_DELAY)

    logger.info(f"\nCollected {len(all_reviews)} total reviews")
    return all_reviews


def deduplicate(reviews: list[dict]) -> list[dict]:
    """Remove duplicate reviews based on comment + course."""
    seen = set()
    out = []
    for r in reviews:
        key = (r["courseName"], r["description"][:100])
        if key not in seen:
            seen.add(key)
            out.append(r)
    removed = len(reviews) - len(out)
    if removed:
        logger.info(f"Removed {removed} duplicates")
    return out


def print_summary(reviews: list[dict]):
    """Print a summary of what was collected."""
    course_counts = Counter(r["courseName"] for r in reviews)
    logger.info(f"\n{'=' * 60}")
    logger.info(f"SUMMARY: {len(reviews)} reviews across {len(course_counts)} courses")
    logger.info(f"{'=' * 60}")
    logger.info("Top 25 courses by review count:")
    for course, count in course_counts.most_common(25):
        avg_diff = sum(r["difficulty"] for r in reviews if r["courseName"] == course) / count
        logger.info(f"  {course}: {count} reviews (avg difficulty: {avg_diff:.1f})")


# ─── CLI ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Scrape RateMyProfessor reviews for UCI CS courses.",
    )
    parser.add_argument(
        "--departments", nargs="+", choices=["COMPSCI", "ICS"], default=["COMPSCI", "ICS"],
        help="Departments to scrape: COMPSCI, ICS, or both (default: both).",
    )
    parser.add_argument(
        "--year", type=int, default=None,
        help="Oldest year to include reviews from (e.g. 2020).",
    )
    parser.add_argument(
        "--limit", "-n", type=int, default=None,
        help="Max number of reviews to collect (default: all).",
    )
    parser.add_argument(
        "--delay", type=float, default=1.5,
        help="Seconds between requests (default: 1.5). Be respectful.",
    )

    args = parser.parse_args()

    global REQUEST_DELAY
    REQUEST_DELAY = args.delay

    logger.info("RateMyProfessor Scraper for UCI")
    logger.info(f"Departments: {args.departments}")
    if args.year:
        logger.info(f"Min year: {args.year}")
    logger.info("")

    # Run
    reviews = run_scraper(departments=args.departments, year=args.year, limit=args.limit)

    # Clean up
    reviews = deduplicate(reviews)

    # Summary
    print_summary(reviews)

    # Build output filename: {dept_prefix}Reviews{year}.json
    selected = set(args.departments)
    if selected == {"COMPSCI", "ICS"}:
        dept_prefix = "ICSCOMPSCI"
    elif "COMPSCI" in selected:
        dept_prefix = "COMPSCI"
    else:
        dept_prefix = "ICS"
    year_suffix = str(args.year) if args.year else ""
    output_path = Path(f"../../data/{dept_prefix}Reviews{year_suffix}.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(reviews, f, indent=2, ensure_ascii=False)

    logger.info(f"\nWrote {len(reviews)} reviews to {output_path}")
    logger.info(f"File size: {output_path.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()