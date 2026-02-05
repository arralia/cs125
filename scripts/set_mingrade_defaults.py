import json
import re

# Load ICSCoursesStripped.json
with open('../data/ICSCoursesStripped.json', 'r') as f:
    data = json.load(f)

def extract_course_grades_from_text(prerequisite_text):
    """
    Extract minimum grades for all courses mentioned in prerequisiteText.
    Returns a dict mapping course IDs/patterns to their minimum grades.
    """
    grades = {}
    
    if not prerequisite_text:
        return grades
    
    # Pattern 1: Course with explicit minimum grade
    # e.g., "I&C SCI 32 with a minimum grade of C" or "EECS 40 with a minimum grade of C"
    pattern1 = r'([A-Z&\s]+\s+\d+[A-Z]*)\s+with\s+a\s+minimum\s+grade\s+of\s+([A-Z\-]+)'
    matches = re.finditer(pattern1, prerequisite_text)
    
    for match in matches:
        course_pattern = match.group(1).strip()
        grade = match.group(2)
        grades[course_pattern] = grade
    
    # Pattern 2: Courses without explicit grade (should default to D-)
    # Extract all course references like "I&C SCI 61", "GDIM 25", etc.
    pattern2 = r'([A-Z&\s]+\s+\d+[A-Z]*)'
    matches = re.finditer(pattern2, prerequisite_text)
    
    for match in matches:
        course_pattern = match.group(1).strip()
        if course_pattern not in grades:
            # Only set D- if no grade was already specified
            grades[course_pattern] = "D-"
    
    return grades

def normalize_course_id(course_id):
    """Normalize course ID for matching."""
    return course_id.upper().strip()

def find_matching_grade(tree_node, grades_map):
    """
    Find the appropriate minGrade for a course by checking the grades map.
    """
    course_id = tree_node.get("id", "")
    title = tree_node.get("title", "")
    
    # Try exact matches and pattern matches
    for pattern, grade in grades_map.items():
        pattern_normalized = normalize_course_id(pattern)
        
        # Check if the course_id ends with the pattern (e.g., "SCI 32" matches pattern "I&C SCI 32")
        pattern_parts = pattern_normalized.split()
        if len(pattern_parts) > 0:
            course_num = pattern_parts[-1]
            if course_id.endswith(course_num):
                return grade
        
        # Also try matching against full ID if available
        if course_id and pattern_normalized in course_id:
            return grade
    
    # Default
    return "D-"

def add_mingrade_to_tree(tree_node, grades_map):
    """
    Recursively add minGrade to course objects in the prerequisiteTree.
    """
    if isinstance(tree_node, dict):
        # If it has an "id" field and prereqType, it's a course object
        if "id" in tree_node and "prereqType" in tree_node:
            if "minGrade" not in tree_node:
                tree_node["minGrade"] = find_matching_grade(tree_node, grades_map)
        
        # Recursively process AND/OR operators
        if "AND" in tree_node:
            for item in tree_node["AND"]:
                if isinstance(item, dict):
                    add_mingrade_to_tree(item, grades_map)
        
        if "OR" in tree_node:
            for item in tree_node["OR"]:
                if isinstance(item, dict):
                    add_mingrade_to_tree(item, grades_map)
    
    return tree_node

# Process each course
updated_count = 0
for course in data["data"]:
    if "prerequisiteTree" in course and "prerequisiteText" in course:
        prerequisite_text = course["prerequisiteText"]
        prerequisite_tree = course["prerequisiteTree"]
        
        # Extract grades from text
        grades = extract_course_grades_from_text(prerequisite_text)
        
        # Add minGrade to tree
        add_mingrade_to_tree(prerequisite_tree, grades)
        updated_count += 1

# Save updated data
with open('../data/ICSCoursesStripped.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"Updated minGrade fields in {updated_count} courses' prerequisiteTrees")
print("All courses without explicit grade requirements now have minGrade: 'D-'")
print("Courses with 'with a minimum grade of C' in prerequisiteText have minGrade: 'C'")
