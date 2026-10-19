"""Check curriculum structure, prerequisites, lab references, and local links."""
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'labs')]
from content.course import MODULES,PATHS
from run import NAMES
errors=[]
def check(condition,message):
    if not condition: errors.append(message)
catalog=json.loads((ROOT/'catalog.json').read_text())
check(len(catalog['modules'])==24,'Unexpected module count')
ids=set();seen=set();lesson_ids=set()
for m in catalog['modules']:
    check(m['id'] not in ids,'Duplicate module '+m['id']);ids.add(m['id'])
    check(set(m['prereqs'])<=seen,'Missing/forward prerequisite '+m['id']);seen.add(m['id'])
    check(m['lab'] in NAMES,'Missing lab '+m['lab'])
    check(len(m['lessons'])==3,'Expected three lessons in '+m['id'])
    q=m['quiz'];check(0<=q['answer']<len(q['options']),'Invalid quiz '+m['id'])
    for l in m['lessons']:
        check(l['id'] not in lesson_ids,'Duplicate lesson '+l['id']);lesson_ids.add(l['id'])
        check((ROOT/l['path']).is_file(),'Missing lesson '+l['path'])
        for field in ['title','explanation','relationship','example','pitfall','exercise','solution']:
            check(isinstance(l.get(field),str) and bool(l[field].strip()),'Missing '+field+' in '+l['id'])
for key,path in catalog['paths'].items():
    visited=set()
    for id in path['modules']:
        m=next((m for m in catalog['modules'] if m['id']==id),None)
        check(m is not None,'Unknown path module '+id)
        if m: check(set(m['prereqs'])<=visited,key+' misses prerequisites for '+id)
        visited.add(id)
check(len(lesson_ids)==72,'Unexpected lesson count')
check(len(set(m['lab'] for m in catalog['modules']))==24,'Labs are not unique per module')
for p in ROOT.rglob('*.md'):
    if any(part in {'.git','.agents','.codex','node_modules'} for part in p.parts): continue
    for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',p.read_text()):
        if target.startswith(('http://','https://','#','mailto:')): continue
        file=unquote(target.split('#')[0].split('?')[0])
        check((p.parent/file).exists(),f'Broken local link {p.relative_to(ROOT)}: {target}')
for file in ['figures.js','fonts/fonts.css','vendor/hairline/index.js','vendor/hairline/LICENSE','style.css','app.js','simulators.js','data.js','icon.svg','docs/scope.md','docs/lab-guide.md']:
    check((ROOT/'site'/file).is_file(),'Missing site asset '+file)
if errors:
    print('\n'.join(errors));sys.exit(1)
print(f'PASS: {len(ids)} modules, {len(lesson_ids)} lessons, prerequisite closure, 24 labs, quizzes, Markdown links, and static assets.')
