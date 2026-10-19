# A tiny processor you understand

Build an executable instruction model, then use it as a reference for a small RTL datapath.

Prerequisite modules: 08-architecture, 16-fpga, 18-verification.

## Build in stages

1. Specify register width, instruction semantics, and program termination.
2. Implement immediate load, add, and halt instructions.
3. Test wraparound, illegal instructions, and instruction limits.
4. Extend the model and implement the same contract in RTL.

## Acceptance criteria

- The demonstration adds 7 and 5 and halts with result 12.
- Eight-bit addition wraps modulo 256.
- Unsupported opcodes and missing termination raise explicit errors.
- Do not call the teaching ISA a compliant RISC-V implementation.

## Executable reference

```bash
python3 projects/reference.py tiny-cpu
python3 -m unittest discover -s tests -v
```

Study `projects/reference.py` after making a prediction. Create your own implementation in a separate learner directory. The tests validate the supplied reference; adapt their imports to grade your own implementation.

## Extension

Replace the teaching ISA with a documented RV32I subset, including decode and exception behavior. Add differential tests before expanding instruction coverage.

## Submission

Include requirements, interface contract, source, test command, observed output, limitations, and a short reflection on one failed approach. Score each of correctness, test evidence, explanation, and reproducibility from 0–3. Require at least 2 in every category before calling the project complete.
