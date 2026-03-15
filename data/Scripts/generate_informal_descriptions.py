"""Generate 2-sentence, student-geared informal descriptions for courses.

For each document in the `courses` collection this script:
- finds reviews in the `reviews` collection where `courseName` matches the course `id`;
- derives a two-sentence informal summary using the course description and reviews;
- updates the course document with `informalDescription` field.

Usage:
  python generate_informal_descriptions.py [--commit]

By default runs in dry-run and prints planned updates; pass `--commit` to write.
"""
from __future__ import annotations
import argparse
import re
import sys
from collections import Counter
from pathlib import Path
from typing import List

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from backend.database import Database
try:
    from backend.gemini import Gemini
except Exception:
    Gemini = None


POSITIVE = ["good", "great", "fun", "interesting", "easy", "useful", "recommended", "solid", "helpful", "nice"]
NEGATIVE = ["tough", "hard", "difficult", "boring", "bad", "annoying", "disorganized", "stressful", "ripoff", "hate", "heavy"]
WORKLOAD = ["project", "homework", "assignment", "exam", "midterm", "workload", "heavy", "lab", "deploy", "docker"]


def first_sentence(text: str) -> str:
    text = (text or "").strip()
    if not text:
        return ""
    # split on sentence terminators
    m = re.split(r"(?<=[.!?])\s+", text)
    return m[0].strip()


def analyze_reviews(reviews: List[dict]):
    if not reviews:
        return {
            "count": 0,
            "avg_difficulty": None,
            "sentiment": "none",
            "workload_tags": [],
            "top_words": []
        }

    difficulties = [r.get("difficulty") for r in reviews if isinstance(r.get("difficulty"), (int, float))]
    avg_diff = sum(difficulties) / len(difficulties) if difficulties else None

    text = " ".join((r.get("description") or "") for r in reviews).lower()
    # simple keyword counts
    pos = sum(text.count(p) for p in POSITIVE)
    neg = sum(text.count(n) for n in NEGATIVE)
    sentiment = "mixed"
    if pos >= 2 * neg and pos > 0:
        sentiment = "positive"
    elif neg >= 2 * pos and neg > 0:
        sentiment = "negative"
    elif pos == 0 and neg == 0:
        sentiment = "neutral"

    workload_hits = [w for w in WORKLOAD if w in text]

    # top words (naive): split and count, ignore short/stopwords
    words = re.findall(r"[a-z]{3,}", text)
    stop = {"the","and","for","with","this","that","have","not","but","you","class","course","professor","prof","really"}
    filtered = [w for w in words if w not in stop]
    top = [w for w, _ in Counter(filtered).most_common(5)]

    return {
        "count": len(reviews),
        "avg_difficulty": avg_diff,
        "sentiment": sentiment,
        "workload_tags": workload_hits,
        "top_words": top,
    }


def build_summary(course_desc: str, analysis: dict) -> str:
    s1 = first_sentence(course_desc) or "No formal course description available."

    if analysis["count"] == 0:
        s2 = "Student reviews are scarce for this offering; check prerequisites and ask peers or the instructor for current expectations."
        return f"{s1} {s2}" if s1 else s2

    # difficulty phrasing
    avg = analysis["avg_difficulty"]
    if avg is None:
        diff_phrase = "expect a typical workload"
    elif avg <= 2:
        diff_phrase = "students generally find it relatively easy"
    elif avg >= 4:
        diff_phrase = "students often report this as challenging"
    else:
        diff_phrase = "students find it moderately demanding"

    # sentiment / workload
    sentiment = analysis["sentiment"]
    if sentiment == "positive":
        sent_phrase = "overall positive student feedback"
    elif sentiment == "negative":
        sent_phrase = "mixed to negative feedback from students"
    else:
        sent_phrase = "mixed student feedback"

    workload = "".join(analysis["workload_tags"])  # e.g., 'projecthomework'
    if analysis["workload_tags"]:
        # pick some notable workload terms
        wl = ", ".join(dict.fromkeys(analysis["workload_tags"]))
        wl_phrase = f"Expect a focus on {wl} and practical projects."
    else:
        wl_phrase = ""

    # prefer concise 2 sentences
    s2_parts = [diff_phrase, sent_phrase]
    if wl_phrase:
        s2_parts.append(wl_phrase)

    # assemble second sentence but keep it short
    s2 = ", ".join(s2_parts)
    # ensure it ends with a period and limit length
    s2 = s2.strip()
    if not s2.endswith('.'):
        s2 = s2 + '.'

    # Trim to two sentences: s1 + s2
    return f"{s1} {s2}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--commit", action="store_true", help="Write informalDescription into the DB")
    parser.add_argument("--use-gemini", action="store_true", help="Use Gemini API to generate descriptions (requires GEMINI_API_KEY)")
    args = parser.parse_args()

    db = Database()
    courses_coll = db.get_collection("courses")
    reviews_coll = db.get_collection("reviews")

    gem = None
    if args.use_gemini:
        if Gemini is None:
            print("Gemini client not available in workspace. Falling back to heuristic.")
        else:
            try:
                gem = Gemini()
            except Exception as e:
                print(f"Failed to initialize Gemini client: {e}. Falling back to heuristic.")
                gem = None

    updated = 0
    planned = []

    for course in courses_coll.find():
        # match course code
        course_code = course.get("id") or course.get("courseId") or course.get("courseName")
        if not course_code:
            continue

        reviews = list(reviews_coll.find({"courseName": course_code}))
        analysis = analyze_reviews(reviews)
        # Prefer Gemini if requested and available
        summary = None
        if gem is not None:
            # assemble prompt: include course id, title, short description, and up to 6 reviews
            title = course.get("title", "")
            short_desc = first_sentence(course.get("description", ""))
            review_texts = []
            for r in reviews[:6]:
                d = r.get("description", "")
                review_texts.append(f"- {d}")
            reviews_block = "\n".join(review_texts) or "No student reviews available."

            prompt = (
                f"You are a helpful, informal UCI computer science student advisor.\n"
                f"Write a concise, student-friendly, informal summary of the course in at most two sentences (2 total).\n"
                f"Tone: casual, clear, and helpful — what a student would want to know before taking the class.\n"
                f"Constraints: max 2 sentences. Do NOT include grading policy or profanity. Keep it <= 40 words per sentence.\n\n"
                f"Course: {course_code} — {title}\n"
                f"Description: {short_desc}\n"
                f"Student reviews (examples):\n{reviews_block}\n\n"
                f"Output only the two-sentence summary."
            )

            try:
                resp = gem.generate_content(prompt)
                # prefer .text if available, else string conversion
                generated = getattr(resp, "text", None) or str(resp)
                # sanitize
                generated = re.sub(r"\s+", " ", generated).strip()
                # ensure <= 2 sentences: keep first two sentences
                parts = re.split(r"(?<=[.!?])\s+", generated)
                summary = " ".join(parts[:2]).strip()
                if not summary:
                    summary = build_summary(course.get("description", ""), analysis)
            except Exception as e:
                print(f"Gemini generation failed for {course_code}: {e}")
                summary = build_summary(course.get("description", ""), analysis)
        else:
            summary = build_summary(course.get("description", ""), analysis)

        planned.append((course_code, summary))

        if args.commit:
            courses_coll.update_one({"_id": course.get("_id")}, {"$set": {"informalDescription": summary}})
            updated += 1

    # report
    print(f"Planned updates for {len(planned)} courses.")
    if args.commit:
        print(f"Wrote informalDescription for {updated} course docs.")
    else:
        # print a small sample of planned updates
        for code, summ in planned[:10]:
            print(f"{code}: {summ}")


if __name__ == "__main__":
    main()
