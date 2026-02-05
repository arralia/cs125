import json

# Load ICSCoursesStripped.json
with open('../data/ICSCoursesStripped.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Filter dependencies to only keep COMPSCI, I&CSCI, or IN4MATX
total_removed = 0
courses_modified = 0

for course in data['data']:
    if 'dependencies' in course and course['dependencies']:
        original_count = len(course['dependencies'])
        
        filtered = [dep for dep in course['dependencies'] 
                   if dep.get('id', '').startswith(('COMPSCI1', 'I&CSCI', 'IN4MATX'))]
        
        removed_count = original_count - len(filtered)
        if removed_count > 0:
            course['dependencies'] = filtered
            total_removed += removed_count
            courses_modified += 1
            print(f"{course.get('id')}: Removed {removed_count} dependencies")

# Save the file
with open('../data/ICSCoursesStripped.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\nTotal: Removed {total_removed} dependencies from {courses_modified} courses")
