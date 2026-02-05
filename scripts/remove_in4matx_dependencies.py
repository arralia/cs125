import json

# Load ICSCoursesStripped.json
with open('../data/ICSCoursesStripped.json', 'r') as f:
    data = json.load(f)

# Process each course
total_removed = 0
updated_courses = 0

for course in data["data"]:
    if "dependencies" in course and isinstance(course["dependencies"], list):
        original_count = len(course["dependencies"])
        
        # Filter out IN4MATX dependencies
        course["dependencies"] = [
            dep for dep in course["dependencies"]
            if not dep.get("id", "").startswith("IN4MATX")
        ]
        
        removed = original_count - len(course["dependencies"])
        if removed > 0:
            total_removed += removed
            updated_courses += 1

# Save the updated data
with open('../data/ICSCoursesStripped.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"Removed {total_removed} IN4MATX dependencies from {updated_courses} courses")
print("Done!")
