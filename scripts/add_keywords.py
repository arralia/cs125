import json
import os

# Get the directory of this script
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', 'data')

# Load Keywords.json to build the mapping
keywords_file = os.path.join(data_dir, 'Keywords.json')
with open(keywords_file, 'r', encoding='utf-8') as f:
    keywords_data = json.load(f)

# Build mapping of course IDs to keywords
course_to_keywords = {}

for keyword_obj in keywords_data['keywords']:
    keyword = keyword_obj['keyword']
    
    # Add upper division courses
    for course in keyword_obj['upperDivisionCourses']:
        course_id = course['id']
        if course_id not in course_to_keywords:
            course_to_keywords[course_id] = []
        course_to_keywords[course_id].append(keyword)
    
    # Add prerequisites
    for course in keyword_obj['prerequisites']:
        course_id = course['id']
        if course_id not in course_to_keywords:
            course_to_keywords[course_id] = []
        course_to_keywords[course_id].append(keyword)

print(f"Created mapping with {len(course_to_keywords)} courses")

# Process ICSCoursesStripped.json
ics_file = os.path.join(data_dir, 'ICSCoursesStripped.json')
with open(ics_file, 'r', encoding='utf-8') as f:
    ics_data = json.load(f)

ics_updated = 0
for course in ics_data['data']:
    course_id = course.get('id')
    if course_id in course_to_keywords:
        course['keywords'] = sorted(list(set(course_to_keywords[course_id])))
        ics_updated += 1

with open(ics_file, 'w', encoding='utf-8') as f:
    json.dump(ics_data, f, indent=2)

print(f"Updated {ics_updated} ICS courses with keywords")

# Process CSUpperDivStripped.json
cs_file = os.path.join(data_dir, 'CSUpperDivStripped.json')
with open(cs_file, 'r', encoding='utf-8') as f:
    cs_data = json.load(f)

cs_updated = 0
for course in cs_data['data']:
    course_id = course.get('id')
    if course_id in course_to_keywords:
        course['keywords'] = sorted(list(set(course_to_keywords[course_id])))
        cs_updated += 1

with open(cs_file, 'w', encoding='utf-8') as f:
    json.dump(cs_data, f, indent=2)

print(f"Updated {cs_updated} CS upper division courses with keywords")
print("\nProcessing complete!")
