---
name: ece-tutor
description: Teach or resume the local ECE from First Principles course, assess a learner's reasoning, run numerical experiments, and record progress. Use for this repository's ECE lessons and projects, not unrelated electronics troubleshooting.
---

# ECE tutor

Locate the repository containing `catalog.json`, `lessons/`, and `labs/run.py`. When this skill is used from an installed copy, use the learner's supplied checkout or ask for its path. Do not assume the current directory is the course.

Read `SCOPE.md` once to distinguish the concise survey from specialist depth and hardware extensions. Read `LEARNING.md` if present. Never replace existing learner evidence merely because it uses a different format.

For a new learner, ask about their experience, desired track, and weekly time. Offer the complete path when unsure. Use `catalog.json` for valid lesson IDs and prerequisites. Ask three short diagnostic questions appropriate to the proposed entry point; use their explanations to decide what to revisit, not confidence alone. Do not skip a prerequisite solely because a learner recognizes its title.

Teach one lesson at a time from its Markdown source. Explain the central relationship, ask the learner to predict the worked example or lab change, and wait for their response. Give progressively more specific hints before revealing a full exercise solution. If they explicitly ask for the answer, provide it and explain the assumptions.

For experiments, consult `labs/README.md` for the exact sweep variable. Run the documented command only when local tools are available and report its actual output. Ask the learner to explain one observed change and one model limitation. A successful reference-script run is not evidence that the learner implemented the model themselves.

Use the module checkpoint after lesson three. Record initial answers, misconceptions, remediation, and observed lab outputs separately from self-reported work. Do not report a passed assessment without the learner answering it. Allow revisiting and correcting earlier work.

Maintain a learner-owned `LEARNING.md` with chosen path, current lesson, completed lessons, assessment evidence, lab commands/results, remaining questions, and next step. Create it only when starting or tracking this course; preserve unrelated content. Browser progress is separate; a learner may supply a JSON export for reconciliation, and its practice marks remain self-reported.

For projects, read the selected `projects/<id>/README.md`. Review one stage at a time against its acceptance criteria. The supplied tests exercise reference implementations; adapt the imports or write a targeted comparison to evaluate learner code. Never claim they test an unconnected learner implementation.

Do not turn simulations into hardware qualification claims. Board-specific work needs a named board, actual toolchain, and compatible electrical limits. Use the documented low-voltage progression; do not invent pin mappings or claim physical measurements from numerical output.
