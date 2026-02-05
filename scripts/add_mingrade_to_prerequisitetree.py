import json
import re

# Load ICSCoursesStripped.json
with open('../data/ICSCoursesStripped.json', 'r') as f:
    data = json.load(f)

def extract_grades_from_prerequisite_text(prerequisite_text):
    """
    Extract minimum grades associated with course IDs from prerequisiteText.
    Returns a dict mapping course patterns to their minimum grades.
    """
    grades = {}
    
    if not prerequisite_text:
        return grades
    
    # Pattern: Course ID followed by "with a minimum grade of X"
    pattern = r'([A-Z&\s]+\s+\d+[A-Z]*)\s+with\s+a\s+minimum\s+grade\s+of\s+([A-Z])'
    matches = re.finditer(pattern, prerequisite_text)
    
    for match in matches:
        course_pattern = match.group(1).strip()
        grade = match.group(2)
        grades[course_pattern] = grade
    
    return grades

def add_mingrade_to_tree(tree_node, grades_map):
    """
    Recursively add minGrade to course objects in the prerequisiteTree.
    """
    if isinstance(tree_node, dict):
        # If it has an "id" field, it's a course object
        if "id" in tree_node and "prereqType" in tree_node:
            # Find matching grade from the text
            course_id = tree_node.get("id", "")
            
            # Try to find a matching grade pattern
            for pattern, grade in grades_map.items():
                # Check if this course ID could match this pattern
                # Patterns in text might be incomplete (e.g., "I&C SCI 61" matches "SCI 61")
                if pattern in tree_node.get("title", "") or course_id.endswith(pattern.split()[-1]):
                    tree_node["minGrade"] = grade
                    break
            
            # If no minGrade was set, check if there's a general pattern match
            if "minGrade" not in tree_node:
                for pattern, grade in grades_map.items():
                    # Extract course number from pattern
                    pattern_parts = pattern.split()
                    if len(pattern_parts) > 0:
                        course_num = pattern_parts[-1]
                        # Check if course_id ends with this number
                        if course_id.endswith(course_num):
                            tree_node["minGrade"] = grade
                            break
        
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
        grades = extract_grades_from_prerequisite_text(prerequisite_text)
        
        if grades:
            # Add minGrade to tree
            add_mingrade_to_tree(prerequisite_tree, grades)
            updated_count += 1

# Save updated data
with open('../data/ICSCoursesStripped.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"Added minGrade fields to {updated_count} courses' prerequisiteTrees")
