import json
import re
from collections import Counter

KW_PATH = '../data/Keywords.json'
CS_PATH = '../data/CSUpperDivStripped.json'

with open(KW_PATH, 'r', encoding='utf-8') as f:
    kw = json.load(f)

with open(CS_PATH, 'r', encoding='utf-8') as f:
    cs = json.load(f)

# build set of course ids already in keywords
existing = set()
for k in kw.get('keywords', []):
    for c in k.get('upperDivisionCourses', []):
        existing.add(c['id'])

# map cs id -> title
cs_map = {c['id']: c.get('title','') for c in cs['data']}
missing = [cid for cid in cs_map.keys() if cid not in existing]
print(f'Missing courses: {len(missing)}')
if not missing:
    print('No action required.')
    raise SystemExit(0)

# Prepare category tokens
categories = kw.get('keywords', [])
cat_tokens = []
for cat in categories:
    name = cat.get('keyword','')
    desc = cat.get('description','')
    text = (name + ' ' + desc).lower()
    tokens = re.findall(r"[a-z0-9]+", text)
    cat_tokens.append((cat, set(tokens)))

# find special topics category
def find_category_by_name(name):
    for c in categories:
        if c.get('keyword','').strip().lower() == name.strip().lower():
            return c
    return None

special_cat = find_category_by_name('Special Topics & Research')
if special_cat is None:
    # create it if missing
    special_cat = {'keyword':'Special Topics & Research','description':'Catch-all for special topics.','upperDivisionCourses':[],'prerequisites':[]}
    categories.append(special_cat)

# classify missing
assignments = {}
for cid in missing:
    title = cs_map[cid].lower()
    tokens = re.findall(r"[a-z0-9]+", title)
    scores = []
    for cat, ctoks in cat_tokens:
        score = sum(1 for t in tokens if t in ctoks)
        scores.append((score, cat))
    # choose best score
    best_score, best_cat = max(scores, key=lambda x: x[0])
    if best_score > 0:
        target = best_cat
    else:
        target = special_cat
    assignments.setdefault(target['keyword'], []).append({'id':cid, 'title': cs_map[cid]})

# apply assignments (avoid duplicates)
for cat in categories:
    name = cat['keyword']
    add = assignments.get(name, [])
    if not add:
        continue
    existing_ids = set(c['id'] for c in cat.get('upperDivisionCourses', []))
    merged = cat.get('upperDivisionCourses', [])[:]
    for course in add:
        if course['id'] not in existing_ids:
            merged.append(course)
    # sort by id
    merged = sorted(merged, key=lambda x: x['id'])
    cat['upperDivisionCourses'] = merged

# Save updated keywords
with open(KW_PATH, 'w', encoding='utf-8') as f:
    json.dump(kw, f, indent=2, ensure_ascii=False)

print('Assigned missing courses into categories:')
for k, v in assignments.items():
    print(f'  {k}: {len(v)}')
print('Keywords.json updated.')
