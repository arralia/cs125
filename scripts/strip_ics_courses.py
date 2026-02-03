import json
import os

# Get the directory of this script
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', 'data')

# Load the full ICS courses data
input_file = os.path.join(data_dir, 'ICSFullResponse.json')
output_file = os.path.join(data_dir, 'ICSCoursesStripped.json')

print(f"Reading from: {input_file}")
print(f"Writing to: {output_file}")

with open(input_file, 'r', encoding='utf-8') as f:
    full_data = json.load(f)

# Fields to keep
fields_to_keep = {
    'id',
    'department',
    'courseNumber',
    'courseNumeric',
    'title',
    'description',
    'instructors',
    'prerequisites',
    'prerequisiteText',
    'overlap',
    'dependencies'
}

# Strip each course to keep only specified fields
stripped_data = {
    'data': []
}

for course in full_data['data']:
    stripped_course = {key: course[key] for key in fields_to_keep if key in course}
    
    # Condense instructors to just names
    if 'instructors' in stripped_course and isinstance(stripped_course['instructors'], list):
        stripped_course['instructors'] = [inst.get('name', '') for inst in stripped_course['instructors'] if isinstance(inst, dict)]
    
    stripped_data['data'].append(stripped_course)

# Write to stripped output file
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(stripped_data, f, indent=2)

print(f"Successfully stripped ICS courses data. Total courses: {len(stripped_data['data'])}")
print(f"Output written to: {output_file}")
