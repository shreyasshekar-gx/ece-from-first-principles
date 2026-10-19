# Numerical laboratory

Python 3.10+; standard library only. Run from the repository root:

```bash
python3 labs/run.py all
python3 labs/run.py rc
python3 labs/run.py rc --sweep 2
python3 -m unittest discover -s tests -v
```

Every output is a simplified model with explicit units. Before running, predict the direction and approximate size of the change. Save both JSON outputs, explain any discrepancy, and identify one omitted physical effect. Running a reference script is practice, not automatic proof of mastery.

| Lab | What `--sweep S` changes | Experiment / expected invariant |
|---|---|---|
| measurement | Meter resistance becomes 1 MΩ / S | More loading lowers the measured divider voltage. |
| math | Euler step becomes 0.1 / S | Smaller steps approach the analytic decay at the reported time. |
| divider | Load becomes 10 kΩ × S | Larger load resistance approaches the 2.5 V unloaded output. |
| rc | Resistance becomes 1 kΩ × S | Larger R slows charging; initial voltage remains zero. |
| diode | Ideality factor becomes S | Compare exponential sensitivity; this is not a full device model. |
| adc | Input becomes 1.65 V × S | Output clamps to 0–4095; resolution is unchanged. |
| logic | No change; exhaustive input table | Recombine sum+2×carry and compare with a+b+carry-in. |
| bits | Initial byte becomes integer(0x11 × S), masked to 8 bits | Bit 3 is set and bit 0 cleared regardless of other bits. |
| cache | Number of sets becomes integer(4 × S), minimum 1 | At S=2 the conflict between addresses 0 and 16 disappears. |
| uart | Baud becomes 9600 × S | A 50-byte 8N1 frame time scales inversely with baud. |
| schedule | Both execution times scale by S | Ideal EDF utilization exceeds one at S>20/7. |
| fir | Both coefficients scale by S | Output amplitude scales; full convolution length stays fixed. |
| bpsk | Gaussian noise sigma becomes 0.5 × S | Compare seeded empirical BER with erfc prediction. |
| reflection | Load becomes 50 Ω × S | S=1 matches; S=2 gives Γ=1/3. |
| control | Proportional gain becomes 2 × S | Equilibrium approaches K/(1+K); there is no saturation or delay. |
| robot | Second joint angle becomes π/2 × S | Verify reach remains at most two metres. |
| counter | Width becomes integer(3 × S), clamped to 1–16 | Wrap modulus changes to 2^width. |
| power | Supply voltage becomes S volts | Dynamic power scales with S² at fixed activity, C, and f. |
| fifo | Depth becomes integer(4 × S), minimum 1 | One excess push is rejected without corrupting FIFO order. |
| timing | Logic delay becomes 5 × S ns | With a fixed 8 ns requirement, slack decreases as delay grows. |
| soc | No change; boundary test | Base and last byte decode; adjacent outside bytes do not. |
| packet | Payload repetitions scale with S, bounded to 170 | Length prefix agrees with payload; parser round-trips. |
| thermal | Current becomes 0.2 × S A | Predicted temperature rise scales with current in this LDO model. |
| quantize | Scale becomes 0.1 × S | Larger range trades against coarser steps; clipping remains explicit. |

Very small or extreme multipliers can exceed a model’s numerical domain; the CLI reports an error. Use S=0.5, 1, and 2 for the baseline study. `logic` and `soc` deliberately enumerate cases rather than use a numerical sweep.

## C exercise

```bash
gcc -std=c11 -Wall -Wextra -Werror labs/c/ring_buffer.c -o /tmp/ece-ring
/tmp/ece-ring
```

The ring buffer is single-threaded. Make the capacity eight and re-run; then write down why interrupts would require a different synchronization design. Do not disable assertions while using this teaching test harness.

## SystemVerilog exercise

Requires Icarus Verilog with SystemVerilog support:

```bash
iverilog -g2012 -s counter_tb -o /tmp/ece-counter labs/rtl/counter.sv labs/rtl/counter_tb.sv
vvp /tmp/ece-counter
```

Change the implementation to saturate instead of wrap and confirm the test fails. Restore the specified behavior. This testbench is provided as an optional EDA exercise; installation of the simulator is separate from the Python course.
