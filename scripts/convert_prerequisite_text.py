import json
import re

# Load ICSCoursesStripped.json
with open('../data/ICSCoursesStripped.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def parse_prerequisite_text(text, prerequisites):
    """
    Parse prerequisiteText and build a prerequisiteTree structure.
    """
    if not text or not text.strip():
        return {}
    
    # Normalize text: replace " or " and " and " with lowercase versions
    text = text.replace(' or ', '|').replace(' and ', '&')
    
    # Build a map of course codes in prerequisites
    prereq_map = {}
    for prereq in prerequisites:
        # Normalize the course ID format for matching
        course_id = prereq.get('id', '')
        # Also handle variations like "I&C SCI 46" vs "I&CSCI46"
        normalized = course_id.replace(' ', '')
        prereq_map[normalized] = prereq
        prereq_map[course_id] = prereq
    
    def build_tree(expr):
        """Recursively build tree from expression."""
        expr = expr.strip()
        
        # Remove outer parentheses if they wrap the entire expression
        while expr.startswith('(') and expr.endswith(')'):
            # Check if these are matching parentheses for the whole expression
            count = 0
            for i, char in enumerate(expr):
                if char == '(':
                    count += 1
                elif char == ')':
                    count -= 1
                if count == 0 and i < len(expr) - 1:
                    break
            if i == len(expr) - 1:
                expr = expr[1:-1].strip()
            else:
                break
        
        # Split by & (AND) at the top level
        if '&' in expr:
            parts = split_at_level(expr, '&')
            if len(parts) > 1:
                return {
                    "AND": [build_tree(part) for part in parts]
                }
        
        # Split by | (OR) at the top level
        if '|' in expr:
            parts = split_at_level(expr, '|')
            if len(parts) > 1:
                return {
                    "OR": [build_tree(part) for part in parts]
                }
        
        # Base case: single course
        course_match = re.search(r'([A-Z&]+)\s*(\d+[A-Z]?)', expr)
        if course_match:
            dept = course_match.group(1)
            num = course_match.group(2)
            course_id = dept + num
            
            if course_id in prereq_map:
                return prereq_map[course_id]
            
            # Try with space
            course_id_space = f"{dept} {num}".replace('&', '& ')
            if course_id_space in prereq_map:
                return prereq_map[course_id_space]
            
            # If not found in prerequisites, create a minimal course object
            return {
                "id": course_id_space,
                "prereqType": "course",
                "coreq": False
            }
        
        return {}
    
    def split_at_level(expr, delimiter):
        """Split expression by delimiter at the top level only."""
        parts = []
        current = ""
        paren_level = 0
        
        for char in expr:
            if char == '(':
                paren_level += 1
            elif char == ')':
                paren_level -= 1
            elif char == delimiter and paren_level == 0:
                if current.strip():
                    parts.append(current.strip())
                current = ""
                continue
            current += char
        
        if current.strip():
            parts.append(current.strip())
        return parts
    
    tree = build_tree(text)
    return tree if tree else {}

# Process each course
updated_count = 0
for course in data['data']:
    prereq_text = course.get('prerequisiteText', '')
    prerequisites = course.get('prerequisites', [])
    
    if prereq_text and prerequisites:
        tree = parse_prerequisite_text(prereq_text, prerequisites)
        if tree:
            course['prerequisiteTree'] = tree
            updated_count += 1

# Save the file
with open('../data/ICSCoursesStripped.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Added prerequisiteTree to {updated_count} courses")
