import json
from util import fetch_five_most_recent_quarters, fetch_active_courses


def run_test():
    print("Calling fetch_five_most_recent_quarters()...")
    recent = fetch_five_most_recent_quarters()
    print("Recent terms (raw tuples):", recent)

    for tup in recent:
        year, season = tup
        print(f"Using term -> year: {year}, season: {season}")
        print("Calling fetch_active_courses()...")
        active = fetch_active_courses(season, year)
        print(f"Fetched {len(active)} active courses")
        sample = sorted(list(active))[:10]
        print("Sample courses:", json.dumps(sample, indent=2))


if __name__ == "__main__":
    try:
        run_test()
    except Exception as e:
        # Try to fetch and print the raw /terms response for debugging
        try:
            import http.client, json
            conn = http.client.HTTPSConnection("anteaterapi.com")
            conn.request("GET", "/v2/rest/websoc/terms")
            res = conn.getresponse()
            data = res.read()
            resp = json.loads(data.decode("utf-8"))
            print("Error during test:", e)
            print("Raw /terms[0]:", json.dumps(resp.get("data", [])[0] if resp.get("data") else resp, indent=2))
        except Exception:
            print("Error during test:", e)
