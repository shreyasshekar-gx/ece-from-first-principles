# Validation

## Required local checks

```bash
npm ci --ignore-scripts
npm run build
python3 scripts/audit.py
python3 -m unittest discover -s tests -v
node tests/test_simulators.cjs
gcc -std=c11 -Wall -Wextra -Werror labs/c/ring_buffer.c -o /tmp/ece-ring
/tmp/ece-ring
```

The Python suite tests 23 groups of behavior: model boundary conditions, independent analytic results, FIFO ordering/rejection, parsing limits, quantization, seeded channel statistics, and integrated capstone contracts. The JavaScript suite checks 13 numerical properties of the browser models. The C harness checks empty/full handling, wraparound, and ordering.

## Browser checks

Use a local server on port 8073. With Playwright available:

```bash
node tests/browser.cjs
```

If Playwright is installed outside this repository, set `PLAYWRIGHT_PATH` to its package directory. Set `ECE_URL` for another preview address. Set `ECE_CDP` to an explicitly launched isolated Chromium debugging endpoint to reuse that browser; otherwise the test launches Playwright’s installed Chromium. The test creates and closes its own browser context.

Tests cover repeated Hairline carousel mounts, route remounting, reduced-motion rendering, theme persistence, menu dismissal, search-button focus, home navigation, search and empty results, track filtering, notes across reload, completion/undo, wrong and correct quiz answers, all six workbench models, progress export and valid/invalid import, project briefs, missing lesson routes, and horizontal overflow on seven mobile views. JavaScript runtime errors fail the run. Desktop and mobile screenshots are written to `artifacts/`.

## Observed results on 20 October 2026

- Python 3.14.7: all 23 test cases passed.
- Node.js 26.8.1: all 13 simulator assertions passed.
- GCC C11 with warnings as errors: ring-buffer harness passed.
- Chromium 152 through Playwright: interaction and mobile checks passed; no page JavaScript errors observed.
- Curriculum audit and deterministic rebuild: passed.
- SystemVerilog counter/testbench: provided, but **not executed locally** because Icarus Verilog was not installed. See `labs/README.md` for the command.
- No physical hardware, RF measurements, PCB fabrication, ASIC flow, or full ISA compliance checks were performed.
- GitHub Actions and Pages workflows are provided but have not run on a remote repository.

Passing these checks does not constitute full expert review of the curriculum or hardware qualification. They test the supplied models and selected site behavior; they do not automatically grade an unrelated learner implementation.
