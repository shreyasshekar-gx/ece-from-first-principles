# A trustworthy sensor node

Build a sampled sensor pipeline that quantizes, filters, frames, and validates measurements.

Prerequisite modules: 05-analog, 09-mcu, 10-rtos, 22-product.

## Build in stages

1. Predict ADC codes and quantify clipping.
2. Implement an eight-sample moving average with an explicit startup policy.
3. Encode samples into bounded frames and reject malformed input.
4. Add an acquisition/processing latency budget and a sensor-disconnection state.

## Acceptance criteria

- Midscale input produces code 2048 in the stated 12-bit model.
- Constant input settles to the same constant after eight samples.
- Payload round-trips exactly; truncated and oversized frames are rejected.
- Retain the sampling assumptions and a table of simulated versus measured claims.

## Executable reference

```bash
python3 projects/reference.py sensor-node
python3 -m unittest discover -s tests -v
```

Study `projects/reference.py` after making a prediction. Create your own implementation in a separate learner directory. The tests validate the supplied reference; adapt their imports to grade your own implementation.

## Extension

Port acquisition to a microcontroller timer and DMA. Capture timestamps and dropped-sample counts on hardware. The Python model does not validate board timing.

## Submission

Include requirements, interface contract, source, test command, observed output, limitations, and a short reflection on one failed approach. Score each of correctness, test evidence, explanation, and reproducibility from 0–3. Require at least 2 in every category before calling the project complete.
