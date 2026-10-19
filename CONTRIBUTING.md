# Contributing

Read SCOPE.md before expanding the course. Author original explanations and examples. Link primary sources; do not import third-party lesson prose without the necessary license and attribution.

A lesson needs a measurable aim, prerequisites, a coherent explanation, a model with units and assumptions, a worked example, a meaningful exercise, a reasoned solution, and an experiment or explicit connection to its module lab. Introduce specialist depth as real authored content, not title-only entries.

Edit `content/course.py` and the checkpoint/project source as appropriate. Keep prerequisites acyclic and included in every focused path. Add independent numerical checks or behavioral tests when a new model needs them. Avoid tests that merely repeat the implementation formula without boundary or reference checks.

Run `python3 scripts/build.py`, `python3 scripts/audit.py`, `python3 -m unittest discover -s tests -v`, and `node tests/test_simulators.cjs`. For UI changes, run the browser checks in TESTING.md and review desktop/mobile screenshots. Commit generated Markdown and data alongside their source.

For hardware-specific contributions, name the board revision, voltage limits, tool versions, exact procedure, expected observations, known failure modes, and what was actually measured. Mark unexecuted tool-dependent checks explicitly.
