import json
import re
import sys
from pathlib import Path


def is_compsci_200_ref(obj):
    if not isinstance(obj, dict):
        return False
    # department + courseNumber object refs
    dept = obj.get('department')
    cn = obj.get('courseNumber')
    if isinstance(dept, str) and dept == 'COMPSCI' and isinstance(cn, str):
        # match 200-299 (three digits starting with '2')
        if re.match(r'^2\d{2}$', cn):
            return True
    # id like 'COMPSCI222'
    idv = obj.get('id')
    if isinstance(idv, str) and re.match(r'^COMPSCI2\d{2}$', idv):
        return True
    # courseId strings inside prerequisite trees like 'COMPSCI 222'
    courseId = obj.get('courseId')
    if isinstance(courseId, str) and re.search(r'COMPSCI\s*2\d{2}', courseId):
        return True
    return False


def clean_value(value, removed_count):
    # Recursively clean lists and dicts, removing COMPSCI 200-level references
    if isinstance(value, list):
        new_list = []
        for el in value:
            if is_compsci_200_ref(el):
                removed_count[0] += 1
                continue
            cleaned = clean_value(el, removed_count)
            # If cleaned is None and original was a dict that became empty, keep it
            new_list.append(cleaned)
        return new_list
    if isinstance(value, dict):
        # If this dict itself is a direct ref, signal to caller by returning the dict (caller list filter handles removal)
        new = {}
        for k, v in value.items():
            new[k] = clean_value(v, removed_count)
        return new
    return value


def main():
    if len(sys.argv) < 3:
        print("Usage: remove_200_courses.py input.json output.json")
        sys.exit(2)

    inp = Path(sys.argv[1])
    out = Path(sys.argv[2])

    data = json.loads(inp.read_text(encoding='utf-8'))

    removed_count = [0]

    if isinstance(data, dict) and isinstance(data.get('data'), list):
        for i, course in enumerate(data['data']):
            # Clean fields within each top-level course object
            data['data'][i] = clean_value(course, removed_count)
            # Additionally, remove any list elements inside the course that are direct refs
            for k, v in list(data['data'][i].items()):
                if isinstance(v, list):
                    filtered = []
                    for el in v:
                        if is_compsci_200_ref(el):
                            removed_count[0] += 1
                            continue
                        filtered.append(el)
                    data['data'][i][k] = filtered
    else:
        print('Unexpected JSON structure; expected dict with "data" list')
        sys.exit(1)

    out.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"Removed {removed_count[0]} COMPSCI 200-level references. Wrote: {out}")


if __name__ == '__main__':
    main()
