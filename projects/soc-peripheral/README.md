# A well-specified SoC peripheral

Integrate a bounded FIFO with an address-decoded register interface and a testable reset contract.

Prerequisite modules: 18-verification, 19-physical, 20-soc.

## Build in stages

1. Write the address map and access permissions.
2. Implement data, occupancy, and reset registers.
3. Test full, empty, invalid address, and reset-with-data behavior.
4. Translate the contract to RTL with a specified bus handshake.

## Acceptance criteria

- Accepted writes emerge in FIFO order.
- A full write returns failure without dropping old data.
- Unaligned or unmapped accesses fail explicitly.
- Reset clears occupancy and prevents stale valid reads.

## Executable reference

```bash
python3 projects/reference.py soc-peripheral
python3 -m unittest discover -s tests -v
```

Study `projects/reference.py` after making a prediction. Create your own implementation in a separate learner directory. The tests validate the supplied reference; adapt their imports to grade your own implementation.

## Extension

Add a real APB or AXI-Lite wrapper, protocol assertions, CDC review, and synthesis constraints. The Python reference is transaction-level only.

## Submission

Include requirements, interface contract, source, test command, observed output, limitations, and a short reflection on one failed approach. Score each of correctness, test evidence, explanation, and reproducibility from 0–3. Require at least 2 in every category before calling the project complete.
