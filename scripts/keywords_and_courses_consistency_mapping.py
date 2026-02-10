import json
from collections import defaultdict

KW_PATH = '../data/Keywords.json'
ICS_PATH = '../data/ICSCoursesStripped.json'
CS_PATH = '../data/CSUpperDivStripped.json'

# Load files
with open(KW_PATH, 'r', encoding='utf-8') as f:
    keywords = json.load(f)

with open(ICS_PATH, 'r', encoding='utf-8') as f:
    ics = json.load(f)

with open(CS_PATH, 'r', encoding='utf-8') as f:
    cs = json.load(f)

# Build set of existing prerequisite ids in keywords
existing_prereqs = set()
for k in keywords.get('keywords', []):
    for p in k.get('courses', []):
        existing_prereqs.add(p.get('id'))

# Map upper course id to keyword names
upper_to_kw = defaultdict(list)
for k in keywords.get('keywords', []):
    name = k.get('keyword')
    for c in k.get('courses', []):
        upper_to_kw[c.get('id')].append(name)

# Helper to find upper courses that list this ICS as prerequisite
def find_upper_dependents(ics_id):
    dependents = set()
    def walk(node, upper_id):
        if isinstance(node, dict):
            if node.get('prereqType') == 'course' and 'courseId' in node:
                cid = node['courseId'].replace(' ', '')
                if cid == ics_id:
                    dependents.add(upper_id)
            else:
                for v in node.values():
                    walk(v, upper_id)
        elif isinstance(node, list):
            for it in node:
                walk(it, upper_id)
    for course in cs.get('data', []):
        upid = course.get('id')
        tree = course.get('prerequisiteTree')
        if tree:
            walk(tree, upid)
    return dependents

# Collect ICS ids from ICSCoursesStripped
ics_ids = [c.get('id') for c in ics.get('data', [])]
missing_ics = [cid for cid in ics_ids if cid not in existing_prereqs]
print(f'Found {len(ics_ids)} ICS courses in ICSCoursesStripped.json; {len(missing_ics)} missing in Keywords.json')

# Collect CS Upper Div ids from CSUpperDivStripped
cs_ids = [c.get('id') for c in cs.get('data', [])]
missing_cs = [cid for cid in cs_ids if cid not in existing_prereqs]
print(f'Found {len(cs_ids)} CS Upper Div courses in CSUpperDivStripped.json; {len(missing_cs)} missing in Keywords.json')
if missing_cs:
    print('Missing CS courses:')
    for cid in missing_cs:
        print(f'  - {cid}')

added = []
# ensure special topics exists
special_kw = None
for k in keywords['keywords']:
    if k.get('keyword') == 'Special Topics & Research':
        special_kw = k
        break
if special_kw is None:
    special_kw = {'keyword':'Special Topics & Research', 'description':'Catch-all','upperDivisionCourses':[], 'prerequisites':[]}
    keywords['keywords'].append(special_kw)

for ics_id in missing_ics:
    dependents = find_upper_dependents(ics_id)
    target_kw_names = set()
    for up in dependents:
        for name in upper_to_kw.get(up, []):
            target_kw_names.add(name)
    if not target_kw_names:
        target_kw_names = {special_kw['keyword']}
    for name in target_kw_names:
        # find kw object
        kw_obj = next((k for k in keywords['keywords'] if k.get('keyword') == name), None)
        if kw_obj is None:
            kw_obj = {'keyword': name, 'description': f'Auto-added {name}', 'upperDivisionCourses': [], 'prerequisites': []}
            keywords['keywords'].append(kw_obj)
        # add prereq if missing
        if not any(p.get('id') == ics_id for p in kw_obj.get('prerequisites', [])):
            # get title from ICS file
            title = ics_id
            for c in ics.get('data', []):
                if c.get('id') == ics_id:
                    title = c.get('title', ics_id)
                    break
            kw_obj.setdefault('prerequisites', []).append({'id': ics_id, 'title': title})
            added.append((ics_id, name))

# Save
with open(KW_PATH, 'w', encoding='utf-8') as f:
    json.dump(keywords, f, indent=2, ensure_ascii=False)

print(f'Added {len(added)} prerequisite entries:')
for a in added:
    print(f'  {a[0]} -> {a[1]}')
