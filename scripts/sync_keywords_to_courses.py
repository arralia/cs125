import json
import os

# Get the directory of this script
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', 'data')

# Load Keywords.json to build the mapping (source of truth)
keywords_file = os.path.join(data_dir, 'Keywords.json')
with open(keywords_file, 'r', encoding='utf-8') as f:
    keywords_data = json.load(f)

# Build mapping of course IDs to keywords from Keywords.json
course_to_keywords = {}

for keyword_obj in keywords_data['keywords']:
    keyword = keyword_obj['keyword']
    
    # Add all courses (merged field)
    for course in keyword_obj.get('courses', []):
        course_id = course['id']
        if course_id not in course_to_keywords:
            course_to_keywords[course_id] = []
        course_to_keywords[course_id].append(keyword)

print(f"Built mapping from Keywords.json: {len(course_to_keywords)} courses")

# Process ICSCoursesStripped.json
ics_file = os.path.join(data_dir, 'ICSCoursesStripped.json')
with open(ics_file, 'r', encoding='utf-8') as f:
    ics_data = json.load(f)

ics_updated = 0
ics_changes = []
for course in ics_data['data']:
    course_id = course.get('id')
    old_keywords = set(course.get('keywords', []))
    
    if course_id in course_to_keywords:
        new_keywords = sorted(list(set(course_to_keywords[course_id])))
        if set(new_keywords) != old_keywords:
            course['keywords'] = new_keywords
            ics_updated += 1
            ics_changes.append((course_id, old_keywords, set(new_keywords)))

with open(ics_file, 'w', encoding='utf-8') as f:
    json.dump(ics_data, f, indent=2)

print(f"Updated {ics_updated} ICS courses with keywords")
if ics_changes:
    print("ICS courses changed:")
    for course_id, old_kw, new_kw in ics_changes:
        print(f"  {course_id}:")
        if old_kw - new_kw:
            print(f"    Removed: {old_kw - new_kw}")
        if new_kw - old_kw:
            print(f"    Added: {new_kw - old_kw}")

# Process CSUpperDivStripped.json
cs_file = os.path.join(data_dir, 'CSUpperDivStripped.json')
with open(cs_file, 'r', encoding='utf-8') as f:
    cs_data = json.load(f)

cs_updated = 0
cs_changes = []
for course in cs_data['data']:
    course_id = course.get('id')
    old_keywords = set(course.get('keywords', []))
    
    if course_id in course_to_keywords:
        new_keywords = sorted(list(set(course_to_keywords[course_id])))
        if set(new_keywords) != old_keywords:
            course['keywords'] = new_keywords
            cs_updated += 1
            cs_changes.append((course_id, old_keywords, set(new_keywords)))

with open(cs_file, 'w', encoding='utf-8') as f:
    json.dump(cs_data, f, indent=2)

print(f"Updated {cs_updated} CS Upper Div courses with keywords")
if cs_changes:
    print("CS Upper Div courses changed:")
    for course_id, old_kw, new_kw in cs_changes:
        print(f"  {course_id}:")
        if old_kw - new_kw:
            print(f"    Removed: {old_kw - new_kw}")
        if new_kw - old_kw:
            print(f"    Added: {new_kw - old_kw}")

print(f"\nTotal courses synced: {ics_updated + cs_updated}")
