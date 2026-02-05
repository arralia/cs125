import json

def remove_coreq_from_tree(tree_node):
    """
    Recursively remove 'coreq' field from all objects in the prerequisiteTree.
    """
    if isinstance(tree_node, dict):
        # Remove coreq if it exists
        if "coreq" in tree_node:
            del tree_node["coreq"]
        if "prereqType" in tree_node:
            del tree_node["prereqType"]
        
        # Recursively process all nested objects
        for key, value in tree_node.items():
            if isinstance(value, dict):
                remove_coreq_from_tree(value)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        remove_coreq_from_tree(item)
    
    elif isinstance(tree_node, list):
        for item in tree_node:
            if isinstance(item, dict):
                remove_coreq_from_tree(item)

# Process ICSCoursesStripped.json
print("Processing ICSCoursesStripped.json...")
with open('../data/ICSCoursesStripped.json', 'r') as f:
    ics_data = json.load(f)

ics_count = 0
for course in ics_data.get("data", []):
    if "prerequisiteTree" in course:
        remove_coreq_from_tree(course["prerequisiteTree"])
        ics_count += 1

with open('../data/ICSCoursesStripped.json', 'w') as f:
    json.dump(ics_data, f, indent=2)

print(f"Removed 'coreq' fields from {ics_count} courses in ICSCoursesStripped.json")

# Process CSUpperDivStripped.json
print("Processing CSUpperDivStripped.json...")
with open('../data/CSUpperDivStripped.json', 'r') as f:
    cs_data = json.load(f)

cs_count = 0
for course in cs_data.get("data", []):
    if "prerequisiteTree" in course:
        remove_coreq_from_tree(course["prerequisiteTree"])
        cs_count += 1

with open('../data/CSUpperDivStripped.json', 'w') as f:
    json.dump(cs_data, f, indent=2)

print(f"Removed 'coreq' fields from {cs_count} courses in CSUpperDivStripped.json")
print("Done!")
