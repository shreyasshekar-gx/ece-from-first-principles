"""Build checked-in Markdown and browser data from the original course source."""
import json
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from content.course import MODULES, PATHS, SOURCES
from content.checkpoints import CHECKPOINTS
from content.projects import PROJECTS

def write(path,text):
    p=ROOT/path
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(text,encoding='utf-8')

def build():
    assert len(MODULES)==len(CHECKPOINTS)
    module_ids={m['id'] for m in MODULES}
    seen=set()
    index=['# Curriculum\n','An original, concise survey course. Each module contains three lessons, a numerical lab, and a checkpoint. Specialist depth and hardware qualification are described in [SCOPE.md](SCOPE.md).\n']
    for i,m in enumerate(MODULES):
        assert set(m['prereqs'])<=seen, f'Prerequisites must precede {m["id"]}'
        seen.add(m['id'])
        q,options,answer,explanation=CHECKPOINTS[i]
        m['quiz']=dict(question=q,options=options,answer=answer,explanation=explanation)
        m['number']=f'{i:02d}'
        index.append(f"## {i:02d} · {m['title']}\n\n{m['summary']}\n")
        refs='\n'.join(f'- [{SOURCES[s][0]}]({SOURCES[s][1]})' for s in m['sources'])
        for j,l in enumerate(m['lessons'],1):
            l['id']=f"{m['id']}/{j:02d}"
            l['path']=f"lessons/{m['id']}/{j:02d}.md"
            index.append(f"- [{l['title']}]({l['path']})")
            doc=f"""# {l['title']}

Module {i:02d} · {m['title']} · Lesson {j}/3

## Before you begin

Module prerequisites: {', '.join(m['prereqs']) or 'None; basic arithmetic is enough to begin.'}

Aim: explain the relationship below, reproduce the worked example, and solve the exercise without looking at its solution.

## Understand

{l['explanation']}

## The relationship

```text
{l['relationship']}
```

## Worked example

{l['example']}

## A common mistake

{l['pitfall']}

## Predict, run, change

Run the shared module experiment from the repository root:

```bash
python3 labs/run.py {m['lab']}
python3 labs/run.py {m['lab']} --sweep 2
```

Read [the lab guide](../../labs/README.md) to identify what the multiplier changes. Predict its effect before running. Record one baseline result, one changed result, and the model assumption that limits your conclusion. This numerical lab supports the module; it does not implement every system discussed in the three lessons.

## Exercise

{l['exercise']}

<details>
<summary>Compare your reasoning with the solution</summary>

{l['solution']}

</details>

## Keep the evidence

Save your prediction, calculation, observed output, and one remaining question in your own notebook. Completion means you can explain the result, not merely run the reference script.

## Further study

These are primary-source reading destinations, not copied lesson text. External software documentation may change; record the version used for any extension.

{refs}
"""
            if j==3:
                doc+=f"\n## Module checkpoint\n\n{q}\n\n"+'\n'.join(f'{k+1}. {option}' for k,option in enumerate(options))+f'\n\n<details><summary>Answer</summary>\n\n{answer+1}. {explanation}\n\n</details>\n'
            write(l['path'],doc)
        index.append('')
    for key,path in PATHS.items():
        assert set(path['modules'])<=module_ids
        visited=set()
        for id in path['modules']:
            m=next(m for m in MODULES if m['id']==id)
            assert set(m['prereqs'])<=visited, f'{key} misses prerequisites for {id}'
            visited.add(id)
    write('CURRICULUM.md','\n'.join(index)+'\n')
    data=dict(title='ECE from First Principles',version='0.1.0',modules=MODULES,paths=PATHS,sources=SOURCES,projects=PROJECTS)
    payload=json.dumps(data,ensure_ascii=False,indent=2)
    write('catalog.json',payload+'\n')
    for src, dest in [('labs/README.md','lab-guide.md'),('SCOPE.md','scope.md')]:
        write('site/docs/'+dest,(ROOT/src).read_text())
    write('site/data.js','window.ECE_COURSE = '+payload.replace('<','\\u003c')+';\n')
    for p in PROJECTS:
        write(f"projects/{p['id']}/README.md",f"# {p['title']}\n\n{p['brief']}\n\nPrerequisite modules: {', '.join(p['modules'])}.\n\n## Build in stages\n\n"+'\n'.join(f'{i+1}. {s}' for i,s in enumerate(p['stages']))+'\n\n## Acceptance criteria\n\n'+'\n'.join('- '+s for s in p['acceptance'])+f"\n\n## Executable reference\n\n```bash\npython3 projects/reference.py {p['id']}\npython3 -m unittest discover -s tests -v\n```\n\nStudy `projects/reference.py` after making a prediction. Create your own implementation in a separate learner directory. The tests validate the supplied reference; adapt their imports to grade your own implementation.\n\n## Extension\n\n{p['extension']}\n\n## Submission\n\nInclude requirements, interface contract, source, test command, observed output, limitations, and a short reflection on one failed approach. Score each of correctness, test evidence, explanation, and reproducibility from 0–3. Require at least 2 in every category before calling the project complete.\n")
    print(f'Built {len(MODULES)} modules, {sum(len(m["lessons"]) for m in MODULES)} lessons, {len(PROJECTS)} project briefs.')

if __name__=='__main__': build()
