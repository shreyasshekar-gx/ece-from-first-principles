# A reproducible digital radio link

Simulate BPSK over Gaussian noise and compare measured bit errors with the analytic synchronized-channel model.

Prerequisite modules: 11-dsp, 12-communications, 13-rf.

## Build in stages

1. State symbol energy and noise conventions.
2. Map seeded random bits to unit BPSK symbols.
3. Inject Gaussian noise, detect symbols, and count errors.
4. Sweep noise and add timing offset as a separate impairment.

## Acceptance criteria

- A noiseless channel returns all bits correctly.
- At sigma=0.5, empirical BER is within 0.01 of the analytic value for 10000 seeded bits.
- Store the random seed and sample count with results.
- Explain why this model is not a complete RF modem.

## Executable reference

```bash
python3 projects/reference.py digital-link
python3 -m unittest discover -s tests -v
```

Study `projects/reference.py` after making a prediction. Create your own implementation in a separate learner directory. The tests validate the supplied reference; adapt their imports to grade your own implementation.

## Extension

Add pulse shaping, timing recovery, and a measured or simulated channel. Keep RF transmission as a separate equipment- and jurisdiction-dependent exercise.

## Submission

Include requirements, interface contract, source, test command, observed output, limitations, and a short reflection on one failed approach. Score each of correctness, test evidence, explanation, and reproducibility from 0–3. Require at least 2 in every category before calling the project complete.
