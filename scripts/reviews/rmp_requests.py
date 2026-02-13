"""
RMP GraphQL Tester
===================
Interactive script to send GraphQL queries to RateMyProfessor
and inspect raw responses. Useful for debugging schema changes.

Usage:
    python rmp_test.py                  # runs all preset tests
    python rmp_test.py --test search    # run just the school search test
    python rmp_test.py --test teachers  # run just the teacher search test
    python rmp_test.py --test ratings   # run just the ratings test
    python rmp_test.py --test introspect  # introspect the schema
    python rmp_test.py --custom         # enter your own query interactively
"""

import argparse
import base64
import json
import requests

# ─── Config ──────────────────────────────────────────────────────────────────

RMP_GRAPHQL_URL = "https://www.ratemyprofessors.com/graphql"
RMP_AUTH_HEADER = "Basic dGVzdDp0ZXN0"

HEADERS = {
    "Authorization": RMP_AUTH_HEADER,
    "Content-Type": "application/json",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    ),
    "Referer": "https://www.ratemyprofessors.com/",
}

# UCI school info
UCI_SCHOOL_ID = 1074
UCI_SCHOOL_NODE_ID = "U2Nob29sLTEwNzQ="  # CHANGED: hardcoded from actual RMP response instead of base64 encoding
UCI_SCHOOL_NAME = "UC Irvine"

# ─── Send query and pretty-print ────────────────────────────────────────────

def send_query(query: str, variables: dict = None, label: str = ""):
    """Send a GraphQL query and print the full response."""
    payload = {"query": query}
    if variables:
        payload["variables"] = variables

    print(f"\n{'=' * 70}")
    if label:
        print(f"TEST: {label}")
        print(f"{'=' * 70}")

    print(f"\n--- REQUEST ---")
    print(f"URL: {RMP_GRAPHQL_URL}")
    print(f"Variables: {json.dumps(variables, indent=2) if variables else 'None'}")
    print(f"Query:\n{query.strip()}")

    try:
        resp = requests.post(
            RMP_GRAPHQL_URL,
            json=payload,
            headers=HEADERS,
            timeout=15,
        )

        print(f"\n--- RESPONSE ---")
        print(f"Status: {resp.status_code}")
        print(f"Headers: {dict(resp.headers)}")

        try:
            data = resp.json()
            print(f"\nBody:\n{json.dumps(data, indent=2)}")
        except Exception:
            print(f"\nRaw body:\n{resp.text[:2000]}")

        return data if resp.status_code == 200 else None

    except requests.RequestException as e:
        print(f"\nERROR: {e}")
        return None


# ─── Preset Tests ────────────────────────────────────────────────────────────

def test_search_school():
    """Test: search for UCI."""
    send_query(
        label="Search for UCI school",
        query="""
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
        """,
        variables={"query": "UC Irvine"},
    )


def test_search_teachers():
    """Test: search for teachers at UCI."""
    send_query(
        label="Search teachers at UCI (Computer Science department)",
        query="""
query SearchTeachers($query: TeacherSearchQuery!, $after: String) {
  newSearch {
    teachers(query: $query, first: 10, after: $after) {
      edges {
        cursor
        node {
          id
          legacyId
          firstName
          lastName
          department
          avgRating
          avgDifficulty
          numRatings
          wouldTakeAgainPercent
          school {
            id
            legacyId
            name
          }
        }
      }
      pageInfo {
        hasNextPage
        endCursor
      }
    }
  }
}
        """,
        variables={
            "query": {
                "text": "",
                "schoolID": UCI_SCHOOL_NODE_ID,
                "departmentID": "RGVwYXJ0bWVudC0xMQ==",
            }
        },
    )


def test_search_teachers_alt():
    """Test: try alternate field names for teacher search."""
    # Sometimes the field might be "schoolId" or "school" instead of "schoolID"
    for field_name in ["schoolID", "schoolId", "school"]:
        send_query(
            label=f"Search teachers — trying field name '{field_name}'",
            query="""
query SearchTeachers($query: TeacherSearchQuery!) {
  newSearch {
    teachers(query: $query, first: 3) {
      edges {
        node {
          id
          firstName
          lastName
          department
          school { name }
        }
      }
    }
  }
}
            """,
            variables={
                "query": {
                    "text": "pattis",
                    field_name: UCI_SCHOOL_NODE_ID,
                }
            },
        )


def test_teacher_ratings():
    """Test: get ratings for a specific teacher by node ID."""
    # First, find a professor
    print("\n>>> First, searching for professor 'Pattis' at UCI...")
    data = send_query(
        label="Find Pattis",
        query="""
query SearchTeachers($query: TeacherSearchQuery!) {
  newSearch {
    teachers(query: $query, first: 3) {
      edges {
        node {
          id
          legacyId
          firstName
          lastName
          department
          numRatings
        }
      }
    }
  }
}
        """,
        variables={
            "query": {
                "text": "pattis",
                "schoolID": UCI_SCHOOL_NODE_ID,
            }
        },
    )

    # Try to extract a teacher ID
    teacher_id = None
    if data and "data" in data:
        edges = (
            data.get("data", {})
            .get("newSearch", {})
            .get("teachers", {})
            .get("edges", [])
        )
        if edges:
            teacher_id = edges[0]["node"]["id"]
            print(f"\n>>> Found teacher ID: {teacher_id}")
    
    # Also try from top-level
    if not teacher_id and data:
        edges = (
            data.get("newSearch", {})
            .get("teachers", {})
            .get("edges", [])
        )
        if edges:
            teacher_id = edges[0]["node"]["id"]
            print(f"\n>>> Found teacher ID: {teacher_id}")

    if not teacher_id:
        # Fallback: manually encoded Pattis ID
        # Teacher-XXXXXX base64 encoded
        print("\n>>> Could not find teacher ID from search. Using fallback.")
        print(">>> Try running --test introspect to check schema.")
        return

    # Now fetch ratings
    send_query(
        label=f"Get ratings for teacher {teacher_id}",
        query="""
query TeacherRatings($id: ID!) {
  node(id: $id) {
    ... on Teacher {
      id
      firstName
      lastName
      department
      ratings(first: 5) {
        edges {
          node {
            id
            comment
            class
            date
            difficultyRating
            helpfulRating
            clarityRating
            ratingTags
            wouldTakeAgain
            grade
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
        """,
        variables={"id": teacher_id},
    )


def test_introspect():
    """Test: introspect the schema to discover available types and fields."""

    # 1. Check what's on the School type
    send_query(
        label="Introspect School type",
        query="""
{
  __type(name: "School") {
    name
    fields {
      name
      type {
        name
        kind
        ofType { name kind }
      }
    }
  }
}
        """,
    )

    # 2. Check TeacherSearchQuery input type
    send_query(
        label="Introspect TeacherSearchQuery input type",
        query="""
{
  __type(name: "TeacherSearchQuery") {
    name
    inputFields {
      name
      type {
        name
        kind
        ofType { name kind }
      }
    }
  }
}
        """,
    )

    # 3. Check Teacher type fields
    send_query(
        label="Introspect Teacher type",
        query="""
{
  __type(name: "Teacher") {
    name
    fields {
      name
      type {
        name
        kind
        ofType { name kind }
      }
    }
  }
}
        """,
    )

    # 4. Check Rating type fields
    send_query(
        label="Introspect Rating type",
        query="""
{
  __type(name: "Rating") {
    name
    fields {
      name
      type {
        name
        kind
        ofType { name kind }
      }
    }
  }
}
        """,
    )

    # 5. Check root query type
    send_query(
        label="Introspect root Query type",
        query="""
{
  __type(name: "Query") {
    name
    fields {
      name
      type {
        name
        kind
        ofType { name kind }
      }
    }
  }
}
        """,
    )


def test_custom():
    """Interactive mode: enter your own query."""
    print("\n" + "=" * 70)
    print("CUSTOM QUERY MODE")
    print("=" * 70)
    print("Paste your GraphQL query below. Enter a blank line when done.")
    print("Tip: for variables, you'll be prompted after the query.\n")

    lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        lines.append(line)

    query = "\n".join(lines)

    var_input = input("\nVariables (JSON, or press Enter for none): ").strip()
    variables = json.loads(var_input) if var_input else None

    send_query(label="Custom query", query=query, variables=variables)


# ─── CLI ─────────────────────────────────────────────────────────────────────

TESTS = {
    "search": test_search_school,
    "teachers": test_search_teachers,
    "teachers_alt": test_search_teachers_alt,
    "ratings": test_teacher_ratings,
    "introspect": test_introspect,
}

def main():
    parser = argparse.ArgumentParser(description="Test RMP GraphQL queries.")
    parser.add_argument(
        "--test", "-t",
        choices=list(TESTS.keys()) + ["all"],
        default="all",
        help="Which test to run (default: all).",
    )
    parser.add_argument(
        "--custom", "-c",
        action="store_true",
        help="Enter a custom query interactively.",
    )
    args = parser.parse_args()

    print(f"RMP GraphQL Tester")
    print(f"Endpoint: {RMP_GRAPHQL_URL}")
    print(f"UCI School Node ID: {UCI_SCHOOL_NODE_ID}")

    if args.custom:
        test_custom()
    elif args.test == "all":
        for name, fn in TESTS.items():
            fn()
    else:
        TESTS[args.test]()


if __name__ == "__main__":
    main()