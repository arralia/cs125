import json

KW_PATH = '../data/Keywords.json'

with open(KW_PATH, 'r', encoding='utf-8') as f:
    kw = json.load(f)

ics_map = {}
for k in kw.get('keywords', []):
    name = k.get('keyword')
    for p in k.get('prerequisites', []):
        pid = p.get('id')
        if not pid: continue
        if pid.upper().startswith('I&CSCI') or pid.upper().startswith('I& SCI') or 'I&CSCI' in pid:
            ics_map.setdefault(pid, []).append(name)

print(f"Found {len(ics_map)} unique ICS prerequisite entries:\n")
for pid in sorted(ics_map.keys()):
    print(pid + ':')
    for cat in ics_map[pid]:
        print('  - ' + cat)
    print()
