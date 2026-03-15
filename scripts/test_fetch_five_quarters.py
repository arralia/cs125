import http.client
import json


def fetch_five_most_recent_quarters_direct(timeout: int = 10):
    """Standalone tester that queries AnteaterAPI for recent WebSOC terms.

    Returns a list of (Year, Season) tuples for up to five most recent quarters.
    """
    conn = http.client.HTTPSConnection("anteaterapi.com", timeout=timeout)
    conn.request("GET", "/v2/rest/websoc/terms")
    res = conn.getresponse()
    data = res.read()
    response_data = json.loads(data.decode("utf-8"))
    recent_quarters = []
    if response_data.get("ok"):
        items = response_data.get("data", [])
        for i in range(min(5, len(items))):
            most_recent_quarter = items[i].get("shortName")
            if most_recent_quarter:
                recent_quarters.append(tuple(most_recent_quarter.split()))
        return recent_quarters
    raise Exception("Failed to fetch most recent term information from AnteaterAPI")


if __name__ == "__main__":
    try:
        terms = fetch_five_most_recent_quarters_direct()
        print("Five most recent quarters:")
        for t in terms:
            print(f"- {t[1]} {t[0]}")
    except Exception as e:
        print("Error fetching terms:", e)