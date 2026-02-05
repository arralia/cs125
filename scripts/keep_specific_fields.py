import json

# Fields to keep for each course
FIELDS_TO_KEEP = ["id", "title", "description", "prerequisiteTree", "dependencies", "keywords"]

# Load ICSCoursesStripped.json
with open('../data/ICSCoursesStripped.json', 'r') as f:
    data = json.load(f)

# Process each course
cleaned_count = 0
for course in data["data"]:
    # Get the fields we want to keep
    cleaned_course = {}
    for field in FIELDS_TO_KEEP:
        if field in course:
            cleaned_course[field] = course[field]
    
    # Replace the course with the cleaned version
    course_index = data["data"].index(course)
    data["data"][course_index] = cleaned_course
    cleaned_count += 1

# Save the updated data
with open('../data/ICSCoursesStripped.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"Cleaned {cleaned_count} courses in ICSCoursesStripped.json")
print(f"Kept only: {', '.join(FIELDS_TO_KEEP)}")
