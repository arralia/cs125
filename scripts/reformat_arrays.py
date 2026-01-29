import json
import sys

GROUP = 4
INDENT = 4

def dump(obj, level=0):
    indent = ' ' * (INDENT * level)
    if isinstance(obj, dict):
        if not obj:
            return '{}'
        parts = []
        for i, (k, v) in enumerate(obj.items()):
            parts.append(' ' * (INDENT * (level+1)) + json.dumps(k, ensure_ascii=False) + ': ' + dump(v, level+1))
        return '{\n' + ',\n'.join(parts) + '\n' + indent + '}'
    if isinstance(obj, list):
        if not obj:
            return '[]'
        prim = (str, int, float, bool, type(None))
        if all(isinstance(x, prim) for x in obj):
            elems = [json.dumps(x, ensure_ascii=False) for x in obj]
            lines = []
            for i in range(0, len(elems), GROUP):
                chunk = elems[i:i+GROUP]
                lines.append(' ' * (INDENT * (level+1)) + ', '.join(chunk))
            return '[\n' + ',\n'.join(lines) + '\n' + indent + ']'
        else:
            parts = []
            for x in obj:
                parts.append(' ' * (INDENT * (level+1)) + dump(x, level+1))
            return '[\n' + ',\n'.join(parts) + '\n' + indent + ']'
    return json.dumps(obj, ensure_ascii=False)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: reformat_arrays.py input.json output.json')
        sys.exit(2)
    inp = sys.argv[1]
    outp = sys.argv[2]
    with open(inp, 'r', encoding='utf-8') as f:
        data = json.load(f)
    text = dump(data, 0)
    with open(outp, 'w', encoding='utf-8') as f:
        f.write(text + '\n')
    print('Wrote', outp)
