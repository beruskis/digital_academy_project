import json, os

path = 'ekc_data_prep_powerbi.ipynb'
with open(path, encoding='utf-8') as f:
    raw = f.read()

# Fix the one broken line: "yes" with ASCII double quotes inside a JSON string
raw = raw.replace(
    '+1 bod za každé „yes“ v těchto',
    '+1 bod za každé `yes` v těchto'
)

# Verify
try:
    nb = json.loads(raw)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(raw)
    print(f'OK: {len(nb["cells"])} cells, JSON valid, saved.')
except json.JSONDecodeError as e:
    print(f'Still broken: {e}')
    lines = raw.split('\n')
    for i in range(max(0, e.lineno-3), min(len(lines), e.lineno+2)):
        print(f'{i+1:4d}: {repr(lines[i][:100])}')
