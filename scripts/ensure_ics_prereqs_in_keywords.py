import json
import re
from collections import defaultdict

KW_PATH = '../data/Keywords.json'
CS_PATH = '../data/CSUpperDivStripped.json'

def normalize_course_id(s):
    # Convert forms like 'I&C SCI 46' or 'I&C SCI H21' to 'I&CSCI46' or 'I&CSCIH21'
    if not s or not isinstance(s, str):
        return s
    return s.replace(' ', '').replace('I&CSCI', 'I&CSCI')

# Load files
with open(KW_PATH, 'r', encoding='utf-8') as f:
    keywords = json.load(f)

with open(CS_PATH, 'r', encoding='utf-8') as f:
    cs = json.load(f)

# Map upper course id -> list of keyword objects that include it
upper_to_keywords = defaultdict(list)
for kw in keywords.get('keywords', []):
    for c in kw.get('upperDivisionCourses', []):
        upper_to_keywords[c['id']].append(kw)

# Traverse prerequisiteTree recursively to collect courseIds and map to upper course
ics_prereq_to_uppers = defaultdict(set)

def extract_course_ids(node, upper_id):
    if isinstance(node, dict):
        # node may be { 'prereqType': 'course', 'courseId': 'I&C SCI 46' }
        if node.get('prereqType') == 'course' and 'courseId' in node:
            cid = node['courseId']
            if not cid:
                return
            norm = normalize_course_id(cid)
            # detect ICS by prefix 'I&CSCI' or 'I&C SCI' in original
            if 'I&CSCI' in norm or 'I&CSI' in cid or 'I&CSCI' in cid or 'I&C SCI' in cid:
                # normalize to Keywords.json style: remove spaces
                norm = cid.replace(' ', '')
                ics_prereq_to_uppers[norm].add(upper_id)
        else:
            for v in node.values():
                extract_course_ids(v, upper_id)
    elif isinstance(node, list):
        for item in node:
            extract_course_ids(item, upper_id)

for course in cs.get('data', []):
    upper_id = course.get('id')
    tree = course.get('prerequisiteTree') or course.get('prereqTree')
    if tree:
        extract_course_ids(tree, upper_id)

# Now check which ICS prereqs are present in keywords prerequisites
existing_prereq_ids = set()
for kw in keywords.get('keywords', []):
    for p in kw.get('prerequisites', []):
        existing_prereq_ids.add(p['id'])

missing = [cid for cid in ics_prereq_to_uppers.keys() if cid not in existing_prereq_ids]
print(f'Found {len(ics_prereq_to_uppers)} ICS prereqs referenced by upper-division courses')
print(f'{len(missing)} ICS prereqs missing from Keywords.json')

# For each missing, assign to keyword(s) of its dependent upper courses
added_count = 0
for ics_id in missing:
    uppers = ics_prereq_to_uppers[ics_id]
    target_keywords = set()
    for up in uppers:
        kws = upper_to_keywords.get(up, [])
        for k in kws:
            target_keywords.add(k['keyword'])
    if not target_keywords:
        # fallback to Special Topics & Research
        target_keywords = {'Special Topics & Research'}
    for kw_name in target_keywords:
        # find kw object
        kw_obj = None
        for k in keywords['keywords']:
            if k.get('keyword') == kw_name:
                kw_obj = k
                break
        if kw_obj is None:
            # create it
            kw_obj = {'keyword': kw_name, 'description': f'Auto-added prerequisites for {kw_name}', 'upperDivisionCourses': [], 'prerequisites': []}
            keywords['keywords'].append(kw_obj)
        # add if not exists
        prereqs = kw_obj.get('prerequisites', [])
        if all(p.get('id') != ics_id for p in prereqs):
            # need title for ics course; try to find in ICSCoursesStripped.json
            ics_title = ics_id
            try:
                with open('../data/ICSCoursesStripped.json', 'r', encoding='utf-8') as f:
                    ics_data = json.load(f)
                for c in ics_data.get('data', []):
                    if c.get('id') == ics_id:
                        ics_title = c.get('title', ics_id)
                        break
            except Exception:
                pass
            prereqs.append({'id': ics_id, 'title': ics_title})
            kw_obj['prerequisites'] = prereqs
            added_count += 1

# Save updated Keywords.json
with open(KW_PATH, 'w', encoding='utf-8') as f:
    json.dump(keywords, f, indent=2, ensure_ascii=False)

print(f'Added {added_count} ICS prerequisite entries to Keywords.json')
