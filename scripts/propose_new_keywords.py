import json
import re

with open('../data/Keywords.json', 'r', encoding='utf-8') as f:
    keywords = json.load(f)

with open('../data/CSUpperDivStripped.json', 'r', encoding='utf-8') as f:
    cs = json.load(f)

existing_ids = set()
for kw in keywords.get('keywords', []):
    for c in kw.get('upperDivisionCourses', []):
        existing_ids.add(c['id'])

cs_map = {c['id']: c['title'] for c in cs['data']}
missing = sorted([cid for cid in cs_map.keys() if cid not in existing_ids])

print(f"Found {len(missing)} missing upper-division courses")
for cid in missing:
    print(f"  {cid}: {cs_map[cid]}")

# Classification rules (simple heuristics based on title keywords)
rules = [
    (re.compile(r'project|capstone', re.I), 'Projects & Capstone'),
    (re.compile(r'embedded|real-?time|microcontroller|hardware|FPGA', re.I), 'Embedded & Real-Time Systems'),
    (re.compile(r'robot|autonom|motion|control', re.I), 'Robotics & Autonomous Systems'),
    (re.compile(r'high[- ]?performance|parallel|distributed|optimization', re.I), 'High-performance & Parallel Systems'),
    (re.compile(r'special|topics|seminar', re.I), 'Special Topics & Research'),
    (re.compile(r'vision|image|graphics|virtual reality|computer vision', re.I), 'Graphics & Vision'),
]

assigned = {}
for cid in missing:
    title = cs_map[cid]
    placed = False
    for pattern, category in rules:
        if pattern.search(title):
            assigned.setdefault(category, []).append({'id': cid, 'title': title})
            placed = True
            break
    if not placed:
        assigned.setdefault('Other CS Upper Division', []).append({'id': cid, 'title': title})

print('\nProposed new keyword groups and counts:')
for k, v in assigned.items():
    print(f"  {k}: {len(v)} courses")

# Append new keyword entries to Keywords.json
for cat, courses in assigned.items():
    new_kw = {
        'keyword': cat,
        'description': f"Auto-generated category for {cat}.",
        'upperDivisionCourses': courses,
        'prerequisites': []
    }
    keywords['keywords'].append(new_kw)

with open('../data/Keywords.json', 'w', encoding='utf-8') as f:
    json.dump(keywords, f, indent=2, ensure_ascii=False)

print('\nKeywords.json updated with new categories.')
print('Summary:')
print(f"  Total previous keywords: {len(keywords['keywords']) - len(assigned)}")
print(f"  New categories added: {len(assigned)}")
print(f"  Total keywords now: {len(keywords['keywords'])}")
