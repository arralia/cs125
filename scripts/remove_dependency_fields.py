import json

# Load ICSCoursesStripped.json
with open('../data/ICSCoursesStripped.json', 'r') as f:
    data = json.load(f)

# Process each course
total_removed = 0
updated_courses = 0

for course in data["data"]:
    if "dependencies" in course and isinstance(course["dependencies"], list):
        for dependency in course["dependencies"]:
            if "department" in dependency:
                del dependency["department"]
                total_removed += 1
            if "courseNumber" in dependency:
                del dependency["courseNumber"]
                total_removed += 1
        
        if len(course["dependencies"]) > 0:
            updated_courses += 1

# Save the updated data
with open('../data/ICSCoursesStripped.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"Removed {total_removed} fields (department and courseNumber) from dependencies in {updated_courses} courses")
print("Done!")
