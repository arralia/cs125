import json
import re

KW_PATH = '../data/Keywords.json'

with open(KW_PATH, 'r', encoding='utf-8') as f:
    keywords = json.load(f)

# Find 'Other CS Upper Division' entry
other_idx = None
for i, kw in enumerate(keywords.get('keywords', [])):
    if kw.get('keyword', '').strip().lower() == 'other cs upper division':
        other_idx = i
        break

if other_idx is None:
    print("'Other CS Upper Division' entry not found. Exiting.")
    raise SystemExit(1)

other_courses = keywords['keywords'][other_idx].get('upperDivisionCourses', [])
if not other_courses:
    print('No courses found in Other CS Upper Division. Nothing to do.')
    raise SystemExit(0)

# Remove the Other entry
keywords['keywords'].pop(other_idx)

# Classification rules
rules = [
    (re.compile(r'project|capstone|individual study|project in', re.I), 'Projects & Capstone'),
    (re.compile(r'embedded|embedded software|embedded software laboratory', re.I), 'Embedded & Real-Time Systems'),
    (re.compile(r'internet of things|iot', re.I), 'IoT & Edge Computing'),
    (re.compile(r'neural|deep learning|neural networks|machine learning|artificial intelligence', re.I), 'AI & Machine Learning'),
    (re.compile(r'bioinformatics|computational biology|biology', re.I), 'Bioinformatics & Computational Biology'),
    (re.compile(r'quantum', re.I), 'Quantum & Emerging Technologies'),
    (re.compile(r'crypt|cryptography', re.I), 'Security & Cryptography'),
    (re.compile(r'graph|graph algorithms', re.I), 'Algorithms & Data Structures'),
    (re.compile(r'formal languages|automata|languages', re.I), 'Programming Languages & Compilers'),
    (re.compile(r'network|network optimization|computer networks|networking', re.I), 'Systems & Architecture')
]

assigned = {}
for c in other_courses:
    title = c.get('title', '')
    placed = False
    for pattern, cat in rules:
        if pattern.search(title):
            assigned.setdefault(cat, []).append({'id': c['id'], 'title': c['title']})
            placed = True
            break
    if not placed:
        assigned.setdefault('Special Topics & Research', []).append({'id': c['id'], 'title': c['title']})

# Helper to find existing keyword entry by name
def find_keyword(name):
    for kw in keywords['keywords']:
        if kw.get('keyword', '').strip().lower() == name.strip().lower():
            return kw
    return None

# Append or merge categories into keywords
for cat, courses in assigned.items():
    existing = find_keyword(cat)
    if existing is not None:
        existing_courses = existing.get('upperDivisionCourses', [])
        # avoid duplicates
        existing_ids = set(x['id'] for x in existing_courses)
        for course in courses:
            if course['id'] not in existing_ids:
                existing_courses.append(course)
        existing['upperDivisionCourses'] = sorted(existing_courses, key=lambda x: x['id'])
    else:
        new_kw = {
            'keyword': cat,
            'description': f'Auto-generated category for {cat}.',
            'upperDivisionCourses': sorted(courses, key=lambda x: x['id']),
            'prerequisites': []
        }
        keywords['keywords'].append(new_kw)

# Save updated Keywords.json
with open(KW_PATH, 'w', encoding='utf-8') as f:
    json.dump(keywords, f, indent=2, ensure_ascii=False)

# Print a summary
print(f'Removed "Other CS Upper Division" and created/merged {len(assigned)} categories:')
for k, v in assigned.items():
    print(f'  {k}: {len(v)} courses')

print('\nKeywords.json updated.')
