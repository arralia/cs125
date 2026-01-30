import json
import sys
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        inp = Path("cs125/data/COMPSCIUpperDiv.json")
        outp = Path("cs125/data/COMPSCIUpperDivStripped.json")
    else:
        inp = Path(sys.argv[1])
        outp = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(str(inp).replace(".json", "Stripped.json"))

    # Load the input JSON
    data = json.loads(inp.read_text(encoding='utf-8'))

    if not isinstance(data, dict) or not isinstance(data.get('data'), list):
        print("Error: Expected JSON structure with 'data' array")
        sys.exit(1)

    # Extract stripped courses
    stripped = []
    for course in data['data']:
        stripped_course = {
            "id": course.get("id"),
            "title": course.get("title"),
            "description": course.get("description"),
            "prerequisiteTree": course.get("prerequisiteTree", {})
        }
        stripped.append(stripped_course)

    # Write output
    result = {"ok": True, "data": stripped}
    outp.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"Extracted {len(stripped)} courses. Wrote: {outp}")


if __name__ == '__main__':
    main()
