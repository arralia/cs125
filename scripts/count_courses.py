import json

with open('../data/CSUpperDivStripped.json', 'r') as f:
    data = json.load(f)

courses = data.get('data', [])
print(f'Total courses in CSUpperDivStripped.json: {len(courses)}')

# List all course IDs
print('\nCourse IDs:')
for course in courses:
    print(f"  {course.get('id')}")
