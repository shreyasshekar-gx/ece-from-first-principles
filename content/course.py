"""Original curriculum source. Build with python3 scripts/build.py."""
SOURCES = {
 'circuits': ('MIT • Circuits and Electronics', 'https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/'),
 'signals': ('MIT • Signals and Systems', 'https://ocw.mit.edu/courses/res-6-007-signals-and-systems-spring-2011/'),
 'em': ('MIT • Electromagnetics and Applications', 'https://ocw.mit.edu/courses/6-013-electromagnetics-and-applications-spring-2009/'),
 'isa': ('RISC-V • Ratified ISA specifications', 'https://docs.riscv.org/reference/isa/'),
 'ros': ('ROS 2 • Jazzy documentation', 'https://docs.ros.org/en/jazzy/'),
 'asic': ('OpenROAD • Flow tutorials', 'https://openroad-flow-scripts.readthedocs.io/en/latest/tutorials/TutorialHome.html'),
 'rtos': ('FreeRTOS • Documentation', 'https://www.freertos.org/Documentation/00-Overview'),
 'hdl': ('Yosys • Documentation', 'https://yosyshq.readthedocs.io/projects/yosys/en/latest/'),
 'pcb': ('KiCad • Documentation', 'https://docs.kicad.org/'),
 'linux': ('Linux kernel • Documentation', 'https://docs.kernel.org/'),
 'control': ('Feedback Systems • Authors’ open textbook', 'https://fbsbook.org/'),
 'devices': ('MIT • Microelectronic Devices and Circuits', 'https://ocw.mit.edu/courses/6-012-microelectronic-devices-and-circuits-fall-2009/'),
}
# Lesson fields: title | explanation | relationship | worked example | misconception | exercise | solution.
MODULES = []
def module(slug, title, group, summary, prereqs, source, lab, rows):
    lessons=[]
    for row in rows.strip().split('\n\n'):
        fields=[x.strip() for x in row.split('\n')]
        assert len(fields)==7, (slug, fields)
        lessons.append(dict(zip(['title','explanation','relationship','example','pitfall','exercise','solution'], fields)))
    MODULES.append(dict(id=slug,title=title,group=group,summary=summary,prereqs=prereqs,sources=source,lab=lab,lessons=lessons))

module('00-bench', 'The engineering bench', 'Foundations', 'Measure, predict, and keep evidence before building hardware.', [], ['circuits'], 'measurement', '''
A reproducible engineering notebook
An engineering claim needs a condition, a measurement, and a criterion. “The sensor works” is incomplete; “at 25 °C, ten readings remain within 0.5 °C of the reference” can be checked. Keep raw observations separate from your interpretation. Record component values, units, instrument range, software version, and wiring revision. Repeating an experiment should mean repeating its conditions, not just pressing Run again. Begin with the Python simulation in this module; it requires no board or paid software.
error = measured value − reference value; relative error = error / reference value
A reference of 3.300 V and reading of 3.267 V give −0.033 V, or −1%. Repeating this reading consistently suggests bias; widely scattered readings suggest variability. These are different problems and require different interventions.
Extra decimal places are not evidence of accuracy. A simulation with perfect components does not validate a physical assembly.
Write an acceptance criterion for a 3.3 V rail with ±5% tolerance, and evaluate a reading of 3.10 V.
The acceptable interval is 3.135–3.465 V; 3.10 V fails. Record the range and measurement conditions along with the result.

Uncertainty and significant figures
Every measurement contains uncertainty from the instrument, environment, and method. A meter specified as a percentage of reading plus counts has two contributions. For independent small random errors, variance propagation estimates combined uncertainty; for guaranteed bounds, add worst-case magnitudes instead. State which interpretation you used. Systematic offset does not disappear by averaging many readings. Calibrate against a suitable reference and preserve the uncorrected data.
u_total = sqrt(u1² + u2²) for independent standard uncertainties
If two independent voltage uncertainty contributions are 0.03 V and 0.04 V, their combined standard uncertainty is 0.05 V. A conservative bound based only on their maximum magnitudes is instead 0.07 V. Neither number is automatically a 95% confidence interval.
Do not apply the root-sum-square rule to strongly correlated errors or call an uncertainty bound a standard deviation without justification.
For independent uncertainties of 0.006 V and 0.008 V, calculate the combined standard uncertainty and the conservative summed bound.
The combined standard uncertainty is 0.010 V; the summed bound is 0.014 V. The distinction belongs in the notebook.

Loading and safe low-voltage experiments
A measuring instrument becomes part of the circuit. A voltmeter has finite input resistance; a current meter inserts impedance in series. Connecting a current input across a supply can short it. Start with simulations, then use current-limited, isolated low-voltage supplies and check component ratings. Turn power off before moving connections. This course’s bench extensions use no mains wiring, high-voltage storage, or exposed lithium cells. Motors require a driver and a controlled mechanical workspace.
R_parallel = R1 R2 / (R1 + R2)
A 10 kΩ / 10 kΩ divider on 5 V produces 2.5 V unloaded. A 10 kΩ measuring load makes the lower leg 5 kΩ, reducing the reading to 1.667 V. The instrument changed the quantity being measured.
A grounded oscilloscope clip is not a floating reference. Know the instrument’s grounding before connecting it.
Calculate the loaded output of the same divider using a 1 MΩ meter.
The lower leg becomes about 9.901 kΩ; the output is about 2.488 V. Loading is small but not zero.
''')
module('01-math', 'Mathematics and computation', 'Foundations', 'Use complex numbers, linear systems, and numerical models as engineering tools.', ['00-bench'], ['signals'], 'math', '''
Complex numbers describe phase
A complex number combines two perpendicular components. In sinusoidal steady state, magnitude represents amplitude and angle represents phase relative to a chosen reference. Euler’s identity connects rotations to sine and cosine. Use a consistent peak or RMS convention throughout an analysis. A phasor describes one frequency after transients have decayed; it is not a complete representation of an arbitrary signal. Numerical code should expose units rather than silently treating degrees as radians.
z = a + jb = |z| exp(jφ); |z| = sqrt(a²+b²); φ = atan2(b,a)
For z = 3 + j4, the magnitude is 5 and phase is 53.13°. Multiplying by j rotates it by 90° to −4 + j3. Its magnitude remains 5 because a pure rotation changes direction, not length.
Adding magnitudes is generally not the same as taking the magnitude of a sum; phase can produce cancellation.
Find the magnitude and phase of 1 − j, and explain what happens when you add 1 + j.
The magnitude is √2 and phase is −45°. The sum is 2, with zero phase: the imaginary components cancel.

Linear algebra for networks
Circuit equations, coordinate transforms, and state estimators all produce linear systems. Write unknowns in a fixed order and align each equation to that order. Solving Ax=b is preferable to explicitly forming an inverse. A singular matrix often means the model lacks an independent constraint; an ill-conditioned matrix can magnify measurement errors. Units still matter: a conductance matrix multiplied by node voltages produces currents, not powers.
A x = b; the residual r = A x − b checks the computed solution
The equations 2x+y=5 and x−y=1 yield x=2 and y=1. Substitution returns zero residual in both equations. In a circuit, this corresponds to checking whether the proposed node voltages satisfy current conservation.
A small residual does not guarantee a small solution error for an ill-conditioned problem.
Solve 3x+y=7 and x+y=3, then calculate both residuals.
x=2 and y=1; both residuals are zero. Keep the variable ordering identical in the matrix and solution vector.

Differential equations and numerical steps
Dynamic systems relate a state to its rate of change. An initial condition selects one trajectory from many possible solutions. Forward Euler uses the present slope to predict the next state, introducing discretization error. Reducing the step can improve accuracy, but stability depends on the method and system. Always compare a numerical model against an analytic case or a convergence study before trusting a detailed simulation.
x[k+1] = x[k] + Δt f(x[k], t[k])
For dx/dt=−x and x(0)=1, Euler with Δt=0.1 gives x[1]=0.9 and x[2]=0.81. The exact value at t=0.2 is exp(−0.2)≈0.8187. The difference is numerical error, not a physical effect.
A plotted curve can look plausible while the time step makes the method unstable. For this decay equation Euler requires 0 < Δt < 2 for asymptotic stability.
Use Δt=0.5 for two steps of dx/dt=−x. Compare the result to exp(−1).
Euler gives 0.25 at t=1, versus about 0.3679 exactly. Halving the step reduces this discretization error.
''')
module('02-dc', 'DC circuits and networks', 'Foundations', 'Derive voltages and currents from conservation laws.', ['01-math'], ['circuits'], 'divider', '''
Ohm’s law and power
Voltage is energy per unit charge, and current is charge flow per unit time. An ideal resistor relates voltage to current with a constant resistance. Choose a reference direction before assigning signs; under the passive sign convention, positive power means the component absorbs energy. Real resistors have tolerance, temperature dependence, and power limits. A correct resistance value alone does not establish whether a part will survive a circuit.
V = IR; P = VI = I²R = V²/R
A 1 kΩ resistor across 5 V carries 5 mA and dissipates 25 mW. A 100 Ω resistor on the same source carries 50 mA and dissipates 250 mW. Reducing resistance by ten increased power by ten at fixed voltage.
Ohm’s law is a device model, not a universal law for every component; a diode is nonlinear.
Find current and power for 330 Ω across 3.3 V. State whether a 0.125 W rating exceeds the ideal dissipation.
Current is 10 mA and power is 33 mW. The nominal rating exceeds this value, though temperature derating and margin still need review.

Kirchhoff’s laws and nodal analysis
Charge conservation gives Kirchhoff’s current law at a node. Energy conservation in the lumped circuit approximation gives Kirchhoff’s voltage law around a loop. Choose ground as a reference, assign node voltages, and express branch currents using voltage differences. These equations do not require guessing the physical direction of each current; a negative answer simply reverses your chosen reference. At high frequencies, distributed electromagnetic effects can invalidate a simplistic lumped model.
Σ currents leaving a node = 0; branch current from a to b is (Va − Vb)/R
A node connected to 5 V through 1 kΩ and ground through 2 kΩ satisfies (V−5)/1000 + V/2000=0. Solving gives V=3.333 V. Both branch currents have magnitude 1.667 mA, so no charge accumulates at the node.
Ground is a selected reference in the equations; it is not necessarily protective earth or an infinite current sink.
A node is connected to 3 V through 1 kΩ and ground through 1 kΩ. Write and solve its node equation.
(V−3)/1000 + V/1000=0, giving V=1.5 V and a 1.5 mA branch current.

Thévenin equivalents and loading
A linear two-terminal network can be represented by a source voltage and series resistance as viewed by an external load. Find the open-circuit terminal voltage, then determine the resistance seen looking into the network with independent sources disabled. Dependent sources require a test-source method. This abstraction makes sensor interfaces and power delivery easier to reason about: the source has finite stiffness, so adding a load changes its output.
Vload = Vth Rload / (Rth + Rload)
A 5 V source with two 10 kΩ divider resistors has Vth=2.5 V and Rth=5 kΩ. Connecting a 5 kΩ load produces 1.25 V, half the open-circuit voltage. The equivalent predicts this without solving the full divider again.
Maximum power transfer at Rload=Rth wastes half the source power in Rth; it is not the objective for an efficient voltage supply.
A source has Vth=3 V and Rth=100 Ω. What voltage appears across a 900 Ω load?
The load voltage is 2.7 V and current is 3 mA. Internal source dissipation is 0.9 mW.
''')
module('03-dynamics', 'Transients and AC circuits', 'Foundations', 'Understand stored energy, settling time, resonance, and frequency response.', ['02-dc'], ['circuits','signals'], 'rc', '''
Capacitors, inductors, and state
Capacitors store energy in electric fields; inductors store energy in magnetic fields. Their ideal equations connect voltage and current through derivatives. A capacitor’s voltage and an inductor’s current cannot jump without an impulse in the corresponding driving quantity. Initial conditions therefore matter. Before a switching event, solve the previous steady state; immediately after the event, carry stored state across and solve the new network.
iC = C dv/dt; vL = L di/dt; EC = CV²/2; EL = LI²/2
A 10 µF capacitor charged to 5 V stores 125 µJ. A constant 1 mA current changes its voltage at 100 V/s, so an ideal 1 V change takes 10 ms. This statement assumes capacitance remains constant and ignores leakage.
An ideal inductor is a short at DC steady state, but not during every transient. Its current is the state that must remain continuous.
How much energy is stored in a 1 mH inductor carrying 0.2 A?
E = 0.5 × 0.001 × 0.2² = 20 µJ. Interrupting this current requires somewhere for the energy to go.

The RC step response
A resistor limits the rate at which a capacitor charges. Apply current conservation to derive a first-order differential equation; the solution approaches the final voltage exponentially. The time constant determines the scale of the response, not an abrupt completion time. Measurement probes, source resistance, and component tolerances alter the effective time constant. Compare simulated and measured curves using the same initial voltage.
τ = RC; v(t) = Vf + (V0 − Vf) exp(−t/τ)
With R=10 kΩ and C=10 µF, τ=0.1 s. Charging from 0 V toward 5 V reaches about 3.161 V after one time constant and 4.966 V after five. Exact settling to the final value takes infinite time in this model.
A response is not “finished” at one time constant; it has completed only about 63.2% of the transition.
For a 1 kΩ resistor and 1 µF capacitor charging to 3.3 V from zero, calculate voltage at 1 ms.
τ=1 ms, so v≈3.3(1−exp(−1))≈2.086 V.

Impedance, filters, and resonance
Phasor-domain impedances turn differential equations into algebra at a single frequency. Capacitive impedance decreases as frequency rises, while inductive impedance increases. A transfer function relates output to input and contains both gain and phase. Resonance occurs when reactive effects cancel in an appropriate topology, but resistance limits the response. Component parasitics become important as frequency increases.
ZC = 1/(jωC); ZL = jωL; HRC(jω) = 1/(1+jωRC)
An RC low-pass with R=1 kΩ and C=1 µF has fc≈159.15 Hz. At fc, its voltage gain is 1/√2 and phase is −45°. The gain in decibels is about −3.01 dB, using 20 log10 for an amplitude ratio.
The cutoff is not a brick wall. A first-order low-pass attenuates gradually, approaching −20 dB per decade far above cutoff.
Find the cutoff of R=10 kΩ and C=10 nF, and the ideal gain at ten times cutoff.
fc≈1591.55 Hz; gain=1/√101≈0.0995, or about −20.04 dB.
''')
module('04-devices', 'Semiconductors and devices', 'Electronics', 'Connect junction physics to practical diode and transistor models.', ['03-dynamics'], ['devices'], 'diode', '''
Diodes and junctions
Doping changes the available mobile carriers in a semiconductor. A p–n junction forms a depletion region and a built-in electric field. External bias changes the barrier, producing a strongly nonlinear current–voltage curve. The exponential diode model is useful over a limited range; series resistance, leakage, temperature, and breakdown require additional modeling. Choose the simplest model that answers the design question without hiding the important failure mode.
I = Is [exp(V/(n VT)) − 1]; VT≈25.9 mV at 300 K
With n=1, increasing forward voltage by roughly 60 mV multiplies the exponential current by about ten near room temperature. A fixed “0.7 V drop” approximation misses this sensitivity but may suffice for a rough resistor-sizing calculation.
A silicon diode does not switch on at one universal voltage. Forward voltage depends on current, device construction, and temperature.
Using a constant 2 V LED drop, choose resistance for 5 mA from a 5 V source.
R=(5−2)/0.005=600 Ω. A nearby larger standard resistance reduces current. The resistor dissipates about 15 mW at the ideal design point.

BJTs and small-signal reasoning
A bipolar transistor can control collector current through a base-emitter junction. In forward-active operation, collector current depends exponentially on base-emitter voltage. The current-gain model is convenient but β varies considerably. Biasing sets a DC operating point; small-signal parameters describe perturbations around it. A model linearized at one bias point should not be used blindly for large excursions or saturation.
gm = IC / VT; small-signal collector current ≈ gm vbe
At IC=1 mA and VT=25.9 mV, gm≈38.6 mS. A small 1 mV base-emitter perturbation gives approximately 38.6 µA of collector-current change. Larger perturbations make the linear approximation less accurate.
A BJT in saturation is not operating in the forward-active region assumed by the simple amplifier model.
Calculate gm at IC=0.5 mA and estimate the collector-current change for a 0.5 mV perturbation.
gm≈19.3 mS and Δic≈9.65 µA under the small-signal assumptions.

MOSFET operation and switching
A MOSFET’s gate controls a channel through an electric field. The gate draws little steady-state current, but its capacitances require charging current during transitions. Threshold voltage indicates the onset of conduction under specified conditions; it does not guarantee a low on-resistance. For switching, inspect the specified gate-drive voltage, resistance, current, thermal path, and transient limits. For analog design, use a suitable operating-region model.
Long-channel saturation model: ID≈(k/2)(VGS−Vth)²; conduction loss≈I² RDS(on)
A switch carrying 2 A with RDS(on)=0.05 Ω dissipates 0.2 W from conduction alone. Switching loss and gate-drive loss add to this. A part specified at 10 V gate drive may perform poorly at 3.3 V even if its threshold is below 3.3 V.
MOSFET “saturation” is an analog constant-current region; a low-resistance digital switch generally operates in the triode region when on.
Estimate conduction loss for 3 A through 20 mΩ, and explain why it does not determine junction temperature by itself.
Loss is 0.18 W. Temperature also depends on switching losses, ambient conditions, package, board copper, and thermal resistance.
''')
module('05-analog', 'Analog and mixed-signal design', 'Electronics', 'Design gain, acquisition, and noise budgets around real component limits.', ['04-devices'], ['circuits','devices'], 'adc', '''
Feedback and operational amplifiers
Negative feedback compares output with a desired relationship and drives the error smaller. For a high-gain op-amp in its linear operating range, feedback often makes the two input voltages nearly equal. That approximation depends on adequate loop gain and stable negative feedback. Check output swing, input common-mode range, slew rate, bandwidth, and loading before treating an amplifier as ideal.
Non-inverting closed-loop gain = 1 + Rf/Rg
With Rf=90 kΩ and Rg=10 kΩ, ideal gain is 10. A 0.2 V input asks for 2 V output. A 1 V input asks for 10 V; an amplifier powered from 3.3 V cannot deliver that, so the linear approximation fails.
A virtual short between inputs is not a physical connection and does not imply current flows between the terminals.
Design an ideal non-inverting gain of 6 using Rg=10 kΩ, then predict the output for 0.3 V input.
Rf=50 kΩ and Vout=1.8 V, provided input/output ranges and loop stability permit it.

Sampling and quantization
An ADC maps a continuous input to discrete codes at discrete times. Sampling limits which frequencies can be distinguished, while quantization limits amplitude resolution. These are separate effects. An anti-alias filter acts before sampling. Reference error, input acquisition time, source impedance, noise, and nonlinearity can dominate a converter’s nominal bit count. Declare the code convention when comparing calculations with hardware.
For an ideal unipolar N-bit converter, LSB = Vref / 2^N; code = clip(floor(Vin/LSB), 0, 2^N−1)
A 12-bit ADC with 3.3 V reference has a nominal step of about 0.806 mV. In the stated floor model, 1.65 V maps to code 2048. The maximum code is 4095; an input at the upper endpoint must be clamped.
Resolution is not accuracy. Twelve output bits do not guarantee twelve useful bits of measurement.
For an 8-bit, 2.56 V ADC in this model, calculate the code for 1.00 V and the maximum code.
The step is 0.01 V, so code is 100; the maximum code is 255.

Noise and dynamic range
Noise limits the smallest useful signal and can enter at every stage of a signal chain. Resistors generate thermal noise; amplifiers add voltage and current noise; interference may be coupled from clocks and power rails. Combine independent noise powers rather than amplitudes. Bandwidth matters: admitting frequencies that carry no desired information still admits noise. Calculate a budget before selecting gain and converter resolution.
Thermal noise voltage rms = sqrt(4 kB T R B) for a flat resistive source over bandwidth B
A 1 kΩ resistor at 300 K over 10 kHz contributes about 0.407 µV rms. Increasing bandwidth by a factor of four doubles rms noise. This model excludes flicker noise, amplifier noise, and interference.
Averaging cannot remove arbitrary systematic interference or recover frequencies already aliased into the signal band.
Two independent stages contribute 3 µV rms and 4 µV rms referred to the same point. Find their combined noise.
The combined value is 5 µV rms. Referring both sources to the same point is necessary before combining them.
''')
module('06-digital', 'Digital logic and state machines', 'Computing', 'Build combinational functions and reason about clocked state.', ['02-dc'], ['hdl'], 'logic', '''
Boolean logic and combinational circuits
Digital circuits interpret ranges of physical voltage as symbols. Boolean algebra describes functions of those symbols; it does not capture propagation delay or analog noise margins. A combinational circuit’s output depends on current inputs, with no intentional stored state. Write a truth table before simplifying an expression. Equivalent Boolean expressions can have different delay, area, and switching behavior when mapped to actual gates.
Half-adder: sum = a XOR b; carry = a AND b
Adding one-bit values 1 and 1 gives binary 10: sum=0 and carry=1. A full adder adds a carry-in as well, allowing several stages to implement wider addition. Carry propagation makes a wide ripple adder slower than a single stage.
Two expressions with equal truth tables need not have equal transient behavior; unequal path delays can produce glitches.
List the sum and carry for a full adder when a=1, b=0, and carry-in=1.
The numeric total is 2, so sum=0 and carry-out=1.

Registers, setup, and hold
Registers sample inputs around a clock edge and retain the result. Setup time requires data to arrive before the edge; hold time requires it to remain afterward. Violating either can cause metastability, an analog condition with uncertain resolution time. Timing constraints connect physical delays to the intended clock frequency. Synchronous design does not eliminate analog behavior; it organizes when that behavior must settle.
Tclock ≥ tCQ + tlogic + tsetup, before clock uncertainty and skew adjustments
If clock-to-Q is 0.2 ns, logic delay is 3 ns, and setup is 0.3 ns, the simplified minimum period is 3.5 ns. This corresponds to about 285.7 MHz before margin. A separate minimum-delay analysis checks hold timing.
Slowing the clock helps many setup failures but generally does not fix a hold violation.
Calculate a simplified minimum clock period using tCQ=0.4 ns, logic=5 ns, and setup=0.6 ns.
The minimum is 6 ns, corresponding to about 166.7 MHz before uncertainty and skew.

Finite-state machines
A finite-state machine separates remembered state from next-state and output functions. Define states by meaningful conditions, then specify every transition, including reset and invalid input. A Moore output depends on state; a Mealy output can depend on state and current input. State diagrams are useful only when their transition rules are precise enough to implement and test. Counters and protocol controllers are both state machines.
state[k+1] = f(state[k], input[k]); output[k] = g(state[k], input[k])
A debouncer can keep a candidate value and a stability count. When an input remains unchanged for three samples, accept it. For samples 0,1,0,1,1,1 the accepted value becomes 1 only at the final sample if reset starts at 0.
Adding a delay loop is not a robust debounce specification; behavior then depends on processor speed and other workload.
Design two states for a request/acknowledge exchange and describe what reset does.
IDLE waits for request; BUSY holds an outstanding transaction until acknowledge. Reset returns to IDLE and clears outstanding state; define how simultaneous request and acknowledge are handled.
''')
module('07-c', 'C and systems programming', 'Computing', 'Understand representations, memory ownership, and register operations.', ['06-digital'], ['isa'], 'bits', '''
Integers and bit operations
Embedded software often manipulates fields inside a fixed-width word. Masks select bits; shifts position fields. Distinguish logical values, signed interpretation, and stored bit patterns. Unsigned arithmetic in C wraps modulo its range, whereas signed overflow is undefined behavior. Use fixed-width unsigned types when representing hardware registers, and ensure shifts remain within the operand width. Python integers need explicit masks when modeling finite-width hardware.
Set bit k: x OR (1<<k); clear bit k: x AND NOT(1<<k)
For an 8-bit value 0b00110000, setting bit 0 gives 0b00110001. Clearing bit 4 then gives 0b00100001. Number bits from zero at the least significant position and state that convention in interfaces.
A bitwise operator is not a logical operator: ANDing masks differs from asking whether both expressions are nonzero.
Set bit 3 and clear bit 0 in the byte 0x11. Give the result in hexadecimal.
0x11 OR 0x08 is 0x19; clearing bit 0 gives 0x18.

Pointers, arrays, and lifetimes
A pointer identifies a memory location under the language’s rules; it does not automatically carry array length or ownership information. Keep buffer size with the buffer, define who may modify it, and prevent references from outliving their objects. Stack storage is tied to a function invocation; static storage persists; dynamically allocated storage requires explicit management. Embedded systems often avoid unbounded allocation in time-critical paths.
Valid array indices for N elements are 0 through N−1
A ring buffer with eight slots may reserve one slot to distinguish full from empty, leaving capacity seven. Reading slot eight is out of bounds even if the adjacent memory happens to be accessible. Testing must include empty, full, and wraparound cases.
A pointer to a local array becomes invalid after the function returns. Successful execution once does not make that lifetime safe.
For a buffer of 16 bytes, identify the last valid index and the number of bytes copied by a loop with i < 16.
The last valid index is 15; the loop visits 16 indices if it starts at zero. A condition i <= 16 would access one byte too far.

Memory-mapped I/O and concurrency
Peripherals expose control and status through addresses with device-specific semantics. A read can clear a status flag; writing one can clear a bit; reserved fields may require particular values. Read the register specification before using a generic read-modify-write pattern. The C volatile qualifier makes certain accesses observable to the compiler, but does not make compound operations atomic or provide general inter-thread synchronization.
Read-modify-write consists of separate read, compute, and write operations
If an interrupt sets bit 1 after foreground code reads a register but before it writes an updated bit 0, a naïve read-modify-write can lose the interrupt’s change. Hardware set/clear registers, critical sections, or suitable atomic primitives solve different versions of this problem.
Volatile is not a lock, a memory barrier for all purposes, or a substitute for understanding peripheral side effects.
Explain why reading a write-one-to-clear register and writing the same value back may lose events.
Every one bit written requests a clear. The write can clear all observed flags rather than only the event the code intended to acknowledge.
''')
module('08-architecture', 'Computer architecture', 'Computing', 'Follow instructions through a datapath, pipeline, and memory hierarchy.', ['07-c'], ['isa'], 'cache', '''
Instructions and datapaths
An instruction set specifies programmer-visible behavior; a microarchitecture implements that behavior. A basic processor fetches an instruction, decodes its fields, reads operands, computes a result, accesses memory if necessary, and updates architectural state. Start with an intentionally small instruction subset before attempting a complete ISA. Keep the specification distinct from implementation timing so two designs can execute the same program differently but correctly.
CPU time = instruction count × cycles per instruction / clock frequency
A program with one million instructions, average CPI=2, and a 100 MHz clock takes 20 ms. Doubling clock frequency helps only if instruction count and CPI remain comparable and the implementation can meet timing.
A RISC-V-inspired toy interpreter is not a compliant RISC-V core; compliance requires defined instruction, exception, and platform behavior.
Calculate execution time for 2 million instructions, CPI=1.5, at 200 MHz.
Time is 3 million cycles / 200 million cycles per second = 15 ms.

Pipelines and hazards
Pipelining overlaps instruction stages to improve throughput. It does not necessarily reduce the latency of one instruction. Data hazards arise when an instruction needs a result that is not yet available; control hazards arise when the next program counter is uncertain. Forwarding, stalls, and branch prediction address different hazards. Precise architectural state must remain correct when speculation is discarded or an exception occurs.
Ideal N instructions through K stages take N+K−1 cycles, without stalls
Five instructions in a five-stage ideal pipeline take nine cycles rather than twenty-five unpipelined stage cycles. A load-use dependency may add a bubble even with forwarding because the data arrives later than an ALU result.
A pipeline diagram without memory latency and branch behavior is a best-case model, not a performance guarantee.
How many cycles do ten instructions take in a four-stage ideal pipeline, and what happens if two stall cycles are added?
The ideal total is 13 cycles; with two additional stalls it becomes 15 cycles.

Caches and locality
Caches exploit temporal and spatial locality by storing recently used memory blocks close to the CPU. An address selects an offset, set, and tag. Misses can come from first use, limited capacity, or mapping conflicts. A direct-mapped cache has one possible slot per block; associativity provides alternatives at a hardware cost. Distinguish cache misses from virtual-memory translation and page faults.
AMAT = hit time + miss rate × additional miss penalty
A cache with 1 ns hit time, 5% miss rate, and 50 ns additional penalty has average access time 3.5 ns. Two addresses that map to the same direct-mapped set can repeatedly evict each other even if most other sets are empty.
A larger cache is not automatically faster: access time, energy, and workload behavior all matter.
Find AMAT for 2 ns hit time, 10% miss rate, and 40 ns additional miss penalty.
AMAT=2+0.1×40=6 ns. The penalty is additional to the initial cache lookup in this convention.
''')
module('09-mcu', 'Microcontrollers and peripherals', 'Embedded', 'Connect firmware to timers, serial links, interrupts, and sensors.', ['08-architecture'], ['rtos'], 'uart', '''
GPIO, timers, and PWM
A microcontroller combines a processor with peripherals that continue working while software runs. GPIO provides digital input and output, but pins have current, voltage, and alternate-function limits. Timers count clock ticks and generate events. PWM represents a control value through pulse width; the average voltage model assumes suitable filtering or load behavior. Use hardware timing when software execution jitter would be unacceptable.
fPWM = ftimer / [(prescaler+1)(period+1)] for a simple up-counter
With a 1 MHz timer clock, prescaler=0 and period=999, PWM frequency is 1 kHz. A compare setting corresponding to 250 high ticks gives about 25% duty, subject to the peripheral’s counting and polarity conventions.
A GPIO pin cannot directly drive an arbitrary motor or relay. Use an appropriate driver and account for inductive energy.
For a 1 MHz timer and 100 total ticks per cycle, calculate frequency and the high time at 30% duty.
Frequency is 10 kHz, period is 100 µs, and high time is 30 µs.

UART, SPI, and I²C
Serial interfaces trade pin count, topology, timing, and complexity. UART uses asynchronous framing and agreed baud rate. SPI commonly uses a controller-generated clock and chip selects. I²C uses addressed devices on shared open-drain lines with pull-ups. Understand electrical signaling as well as protocol bytes: a correct packet cannot compensate for incompatible voltage levels, insufficient rise time, or missing common reference.
UART 8N1 sends 1 start + 8 data + 1 stop = 10 bits per byte
At 115200 baud, an 8N1 stream carries at most 11520 payload bytes per second before application overhead. Sending 100 bytes takes about 8.68 ms. The baud-rate label alone does not equal useful application throughput.
I²C pull-ups are functional components, not optional decoration; bus capacitance and resistor value determine rising-edge behavior.
How long does a 50-byte UART 8N1 message take at 9600 baud, ignoring gaps?
It contains 500 transmitted bits, taking about 52.08 ms.

Interrupts, DMA, and latency
Interrupts let hardware notify software, while DMA transfers data without one CPU operation per byte. Both introduce concurrency and ownership questions. Keep interrupt handlers bounded; capture state, acknowledge the correct source, and defer longer work. Measure worst-case latency under competing load, not only average latency on an idle system. DMA buffers may require cache maintenance and explicit handoff on systems with caches.
Buffer time = buffer capacity / incoming byte rate
A 256-byte buffer receiving 10000 bytes per second holds 25.6 ms of data. If the consumer can be delayed for 30 ms, overflow is possible even when its average processing rate exceeds the input rate.
DMA does not remove the need for synchronization. The CPU and peripheral must agree on when a buffer is safe to reuse.
Find the minimum whole-byte capacity to absorb a 12 ms service delay at 20000 bytes per second, before margin.
At least 240 bytes are needed. Real designs add margin for arrival bursts, scheduling variation, and bookkeeping conventions.
''')
module('10-rtos', 'Real-time systems', 'Embedded', 'Design for deadlines, bounded queues, and predictable failure recovery.', ['09-mcu'], ['rtos'], 'schedule', '''
Deadlines and schedulability
Real-time correctness depends on both the result and its arrival time. Define each task’s worst-case execution time, period, and deadline. Utilization is a useful first check, but the scheduling policy and assumptions determine whether tasks meet deadlines. Interrupt interference, blocking, release jitter, and context-switch costs must be included for a real system. A model with ideal independent periodic tasks is only a starting point.
U = Σ Ci/Ti; ideal preemptive single-core EDF with independent tasks and deadlines equal to periods is feasible when U≤1
Tasks needing 1 ms every 5 ms and 2 ms every 10 ms use 40% of the processor. That leaves nominal utilization headroom, but a long non-preemptible section can still delay a critical job.
Average execution time cannot establish a worst-case deadline guarantee.
Compute utilization for tasks taking 2 ms every 10 ms and 3 ms every 20 ms.
U=0.2+0.15=0.35, or 35%. Schedulability still depends on the stated policy and nonideal effects.

Synchronization and priority inversion
Shared mutable state creates dependencies between tasks. Mutexes protect critical sections, queues transfer ownership, and semaphores signal availability. Priority inversion occurs when a high-priority task waits for a resource held by a lower-priority task while intermediate-priority work delays the holder. Priority inheritance can reduce this delay, but it does not make unbounded critical sections acceptable or eliminate deadlock.
A wait-for cycle is a warning sign for deadlock
Task A locks resource X then waits for Y; task B locks Y then waits for X. Neither can proceed. A consistent global lock order prevents this particular cycle. A queue-based design can sometimes eliminate the need to share both resources.
Disabling interrupts for a long critical section may protect data while making the overall system miss deadlines.
Describe a lock ordering rule that prevents the two-resource deadlock above.
Require every task to acquire X before Y, and release in a consistent manner. No task may hold Y while waiting to acquire X.

Watchdogs and fault recovery
A watchdog detects lack of expected progress, not arbitrary correctness. Feed it only after meaningful health conditions have been checked. A timer interrupt that always feeds the watchdog can conceal a dead main task. Define recovery behavior, persistent diagnostics, and safe outputs after reset. Fault injection tests whether the system actually enters the intended state when a task hangs or a queue overflows.
Detection delay is bounded by the watchdog timeout plus implementation and reset latency
If a control task must report progress every 20 ms and a watchdog expires after 100 ms, several missed reports may occur before reset. Whether that delay is acceptable depends on the plant and hazard analysis, not on firmware convenience.
A reset loop is not a recovery strategy. Repeated boot failures need a bounded fallback and evidence of the original fault.
A system feeds its watchdog only after all tasks advance. Explain what a permanently blocked task should cause.
Its progress condition fails, feeding stops, and timeout initiates the defined recovery path. Test the actual output state and retained diagnostics.
''')
module('11-dsp', 'Signals and digital signal processing', 'Signals', 'Move between samples, spectra, filters, and fixed-point arithmetic.', ['03-dynamics','07-c'], ['signals'], 'fir', '''
Sampling and aliasing
A sampled sinusoid is identified only up to frequency ambiguities created by the sample rate. For a bandlimited baseband signal, sampling above twice its highest frequency permits ideal reconstruction under ideal assumptions. Real systems need a transition band for the anti-alias filter. Once out-of-band energy aliases into the desired band, a digital filter cannot reliably separate it from a genuine in-band signal.
x[n] = sin(2π f n / fs); frequencies differing by integer multiples of fs have related sample sequences
Sampling a 900 Hz cosine at 1000 samples/s produces the same samples as a 100 Hz cosine. A plot of the samples therefore cannot establish which analog frequency was present. Filtering must occur before the ADC.
The Nyquist condition refers to the signal bandwidth and sampling arrangement, not a claim that any waveform below the sample rate is safe.
Find the apparent baseband frequency of a 700 Hz cosine sampled at 1000 samples/s.
It aliases to 300 Hz. For sine waves the representation can include a phase/sign change.

Convolution and FIR filters
An LTI system is described by its impulse response. Discrete convolution combines delayed, scaled copies of that response. A finite impulse response filter uses a fixed number of coefficients and has no feedback. Its frequency response follows from those coefficients, so time-domain smoothing and frequency-domain attenuation are two descriptions of the same operation. Boundary handling changes finite-record output and must be stated.
y[n] = Σ h[k] x[n−k]
For h=[0.5,0.5], the filter averages adjacent samples. Feeding an impulse [1,0,0] with zero extension gives [0.5,0.5,0,0] for full convolution. Constant input eventually passes unchanged because the coefficients sum to one.
A moving average is not an ideal low-pass and its sidelobes can pass unwanted frequencies.
Compute the full convolution of x=[1,2] and h=[1,−1].
The result is [1,1,−2]. Full convolution length is 2+2−1=3.

Spectra, windows, and fixed-point limits
The DFT represents a finite record as a sum of discrete complex sinusoids. Frequency resolution is tied to observation duration; zero padding adds interpolated bins without creating new information. A window reduces leakage at the cost of a wider main lobe and amplitude corrections. When implementing a filter on fixed-point hardware, coefficient scaling, rounding, accumulator width, and saturation become part of the algorithm.
DFT bin spacing = fs/N; Q-format values represent integer × 2^(−fractional_bits)
At fs=8000 Hz with N=800 samples, bin spacing is 10 Hz. In signed Q1.15 convention, the largest positive value is 32767/32768, slightly below one. Adding two large values requires a wider intermediate or explicit overflow handling.
FFT speed does not change the information content of the DFT. More plotted bins from zero padding do not resolve two arbitrarily close tones.
How many samples at 48 kHz give 10 Hz DFT bin spacing?
N=48000/10=4800 samples, representing 0.1 s of observation.
''')
module('12-communications', 'Communication systems', 'Signals', 'Build a link from bits through modulation, noise, and detection.', ['11-dsp'], ['signals'], 'bpsk', '''
Modulation and complex baseband
Modulation maps information onto a waveform suitable for a channel. Amplitude, frequency, and phase can all carry information. Complex baseband represents in-phase and quadrature components without explicitly simulating a high carrier frequency. A complete link also needs pulse shaping, synchronization, channel estimation, and detection. Start with an ideal synchronized channel so each later impairment can be introduced and measured separately.
BPSK mapping: bit 0 → −1, bit 1 → +1; detect 1 when received sample ≥ 0
The bit sequence [0,1,1,0] maps to [−1,+1,+1,−1]. Received samples [−0.7,+0.8,−0.1,−1.2] decode as [0,1,0,0], producing one error. The zero-threshold rule assumes equal priors and a symmetric channel model.
A constellation plot without synchronization assumptions is not a complete modem design.
Map bits [1,0,1] to BPSK and decode received values [0.2,−0.3,0.8].
The symbols are [+1,−1,+1], and all three received values decode correctly under the zero-threshold rule.

Noise, bandwidth, and capacity
A channel’s useful rate is constrained by bandwidth, noise, and coding assumptions. Distinguish signal-to-noise ratio over a bandwidth from energy per bit divided by noise spectral density. Capacity is a theoretical upper bound under a model, not a promise that a simple uncoded modem achieves it. Increasing transmit power has diminishing returns in the logarithmic expression and may be constrained by the application.
AWGN capacity C = B log2(1+S/N), with S/N in linear units
For B=1 MHz and S/N=10, capacity is about 3.459 Mbit/s under the ideal AWGN model. A 10 dB SNR equals a linear ratio of ten, not ten thousand. Protocol overhead and practical implementation reduce delivered payload throughput.
Do not put a decibel value directly into log2(1+S/N); convert the ratio first.
Calculate ideal capacity for B=100 kHz and linear SNR=3.
C=100000×log2(4)=200000 bit/s, or 200 kbit/s.

Error detection and link budgets
Error-detecting codes add redundancy to recognize corruption; error-correcting codes can recover some corrupted messages. A CRC is a polynomial-based detector with properties determined by its polynomial and frame length. It is not authentication. A link budget adds gains and losses in decibel units to estimate received power, then compares it with receiver requirements and margin. Separate deterministic losses from fading and interference allowances.
Pr(dBm) = Pt(dBm) + Gt(dBi) + Gr(dBi) − path loss(dB) − other losses(dB)
A 10 dBm transmitter, two 2 dBi antennas, 80 dB path loss, and 3 dB other losses yield −69 dBm received power. A receiver requiring −90 dBm has 21 dB nominal margin before additional impairments.
A passing CRC does not prove a sender is trusted, and a positive nominal link margin does not guarantee reliability in fading.
Find received power for 0 dBm transmit power, 0 dBi antennas, and 60 dB total loss.
Received power is −60 dBm. Compare it with sensitivity at the required bandwidth, data rate, and error probability.
''')
module('13-rf', 'Electromagnetics and RF', 'Signals', 'Know when wires become transmission lines and radiation matters.', ['03-dynamics','12-communications'], ['em'], 'reflection', '''
Fields, waves, and wavelength
Lumped circuits approximate fields when propagation delays and spatial variation are negligible for the problem. Maxwell’s equations connect charge, current, and changing electric and magnetic fields. A propagating wave carries energy through space or a guided structure. Wavelength depends on frequency and medium. Fast edge rise time can matter more than the clock’s repetition rate when deciding whether a PCB connection needs transmission-line treatment.
λ = v/f; in free space v≈3×10^8 m/s
A 100 MHz wave has a free-space wavelength near 3 m. In a medium with propagation speed 2×10^8 m/s, the wavelength is 2 m. A 10 cm trace then has a one-way delay of about 0.5 ns, which matters for sufficiently fast edges.
A 1 MHz digital clock can still produce transmission-line problems if its edges are very fast.
Estimate the free-space wavelength at 2.4 GHz.
λ≈0.125 m, or 12.5 cm. Guided wavelengths are shorter when propagation velocity is lower.

Transmission lines and reflections
A transmission line has distributed inductance and capacitance and a characteristic impedance. When a traveling wave reaches a mismatched load, part of it reflects. The source sees the reflection only after propagation delay. Matching can suppress reflections, but termination choice affects power, voltage swing, and topology. Use the appropriate line and source model instead of treating every interconnect as a single ideal wire.
ΓL = (ZL−Z0)/(ZL+Z0), for the voltage reflection coefficient
A 50 Ω line terminated in 100 Ω has Γ=1/3. An open circuit gives +1 and a short gives −1. The sign describes reflected voltage polarity; the total voltage at the load is the sum of incident and reflected waves.
Characteristic impedance is not the same as the DC resistance measured along a cable conductor.
Find Γ for a 50 Ω line terminated in 25 Ω.
Γ=(25−50)/(25+50)=−1/3. The reflected voltage is inverted and one-third of the incident amplitude.

Antennas, matching, and S-parameters
An antenna converts guided energy to radiation and vice versa. Gain includes directionality and efficiency; it does not create power. S-parameters characterize traveling waves at ports under specified reference impedances. S11 relates input reflection, while S21 describes forward transmission in a two-port network. Calibration and reference planes matter because cables and fixtures otherwise become part of the measured device.
Return loss = −20 log10(|Γ|); ideal isotropic free-space loss = 20 log10(4πd/λ)
A reflection magnitude of 0.1 corresponds to 20 dB return loss and 1% reflected power under the usual same-impedance wave normalization. A high return-loss number means a small reflection, which is easy to confuse with a negative S11 value in dB.
Good impedance matching does not guarantee good radiation efficiency or a suitable antenna pattern.
What return loss and reflected-power fraction correspond to |Γ|=0.5?
Return loss is about 6.02 dB and reflected-power fraction is 0.25, or 25%.
''')
module('14-control', 'Control systems', 'Robotics', 'Model dynamics, close feedback loops, and examine stability.', ['01-math','11-dsp'], ['control'], 'control', '''
Models, feedback, and poles
A plant model predicts how inputs influence outputs and internal state. Feedback measures an output and adjusts the input in response to error. Closed-loop behavior depends on both plant and controller, including delays and saturation. For continuous-time linear systems, poles in the left half-plane correspond to decaying modes; discrete-time stable poles lie inside the unit circle. These statements assume the appropriate finite-dimensional LTI model.
For negative feedback, closed-loop transfer T = PC/(1+PC)
A first-order plant P(s)=1/(s+1) with proportional controller C=K has closed-loop transfer K/(s+1+K). For positive K its pole moves left to −(1+K), but the DC gain K/(1+K) remains below one.
Increasing gain is not universally stabilizing; higher-order dynamics and delay can make large gain destabilize a loop.
For this plant with K=3, find the closed-loop pole and DC gain.
The pole is −4 and the DC gain is 3/4. A unit step has 25% steady-state error in this ideal model.

PID and saturation
A PID controller combines present error, accumulated error, and an estimate of error rate. Integral action can remove steady-state error but accumulates during actuator saturation unless controlled. Derivative action amplifies measurement noise and is often filtered or applied to the measured variable to reduce setpoint kick. Tune with a measured plant response, clear performance criteria, and actuator limits, not only a visually pleasing curve.
u = Kp e + Ki ∫e dt + Kd de/dt
If an actuator can command only 0–1 and the controller asks for 4, the plant receives 1. Continuing to integrate positive error can produce a large stored integral and overshoot after the error changes sign. Conditional integration or back-calculation addresses this windup.
An ideal derivative in a textbook equation is not directly implementable on noisy sampled data without design choices.
For proportional-only control with Kp=2 and error 0.8, calculate the command before and after a 0–1 actuator limit.
The requested command is 1.6; the applied command is 1.0. Log both values to expose saturation.

State-space models and observers
State-space models represent internal dynamics directly and support multivariable systems. Not every state is measured; an observer combines model predictions with measurements. Controllability asks whether inputs can influence all relevant states, while observability asks whether measurements can distinguish them. Noise, model mismatch, and sampling affect estimator performance. A mathematically valid observer can still be poorly tuned for real sensors.
x[k+1]=Ax[k]+Bu[k]; y[k]=Cx[k]+Du[k]
For constant velocity motion, state [position,velocity] advances with A=[[1,Δt],[0,1]]. A position measurement uses C=[1,0]. Consecutive positions carry information about velocity, but differentiating noisy measurements directly can be unstable in practice.
An estimator’s confidence is only as credible as its model and noise assumptions; covariance is not a guarantee of truth.
Advance position=2 m and velocity=3 m/s by 0.2 s in a constant-velocity model.
The next position is 2.6 m and velocity remains 3 m/s, before disturbances or measurement updates.
''')
module('15-robotics', 'Robotics and autonomy', 'Robotics', 'Connect geometry, estimation, planning, and actuator behavior.', ['14-control','10-rtos'], ['ros','control'], 'robot', '''
Frames and forward kinematics
Robotics requires explicit coordinate frames. A point’s coordinates change when the reference frame changes, even though the physical point does not. Rotations and translations compose in an order-sensitive way. Forward kinematics maps joint positions to end-effector pose; inverse kinematics finds joints for a desired pose and may have multiple or no solutions. Label frames and angle units on every transformation.
Planar two-link arm: x=L1 cosθ1+L2 cos(θ1+θ2); y=L1 sinθ1+L2 sin(θ1+θ2)
With both links 1 m long, θ1=0 and θ2=π/2 place the end effector at (1,1) m. Setting both angles to zero places it at (2,0) m. These checks catch many sign and frame-convention errors.
Adding rotations without considering their axes and order fails in three dimensions; matrix multiplication is generally not commutative.
For two 1 m links at θ1=π/2 and θ2=0, find the end-effector position.
The position is approximately (0,2) m, with tiny floating-point residuals possible in computed cosine values.

Odometry and sensor fusion
Wheel odometry integrates motion estimates from encoders. Errors accumulate because wheel radii, slip, and floor contact are imperfect. Independent measurements such as landmarks or inertial sensors can correct different aspects of the estimate, but their own biases and timing matter. Fusion requires compatible frames, timestamps, and uncertainty models. Treat a pose estimate as an evolving belief with failure cases, not a perfect ground truth.
v=(vR+vL)/2; angular velocity ω=(vR−vL)/wheelbase
A differential-drive robot with vR=0.6 m/s, vL=0.4 m/s, and wheelbase=0.5 m has forward speed 0.5 m/s and angular speed 0.4 rad/s. Straight motion occurs only when wheel speeds match under the ideal no-slip model.
Encoder agreement does not prove the robot moved as expected; both wheels can slip together.
Find v and ω for wheel speeds 0.2 and −0.2 m/s with a 0.4 m wheelbase.
v=0 and ω=1 rad/s when the right wheel is +0.2 m/s. The ideal robot rotates in place.

Planning and robot software
A planner chooses a route through a model of free space; a controller attempts to execute it. Occupancy grids discretize space, and graph algorithms search valid transitions. A real robot has finite size, so inflate obstacles or plan in configuration space. Robot middleware organizes communication between components, but does not replace timing, safety, or interface design. In ROS-style systems, distinguish streaming topics from request/response services and long-running actions.
For a four-connected grid, Manhattan heuristic h=|x−xgoal|+|y−ygoal| is admissible with unit step costs
From (0,0) to (3,2), an obstacle-free four-connected route needs at least five steps. If obstacles block the route, search must detour or report no path. A path for a point robot may be invalid for a wide chassis.
A planner returning a path is not proof of collision-free physical execution; localization and tracking error require margin.
Find the Manhattan lower bound from (2,1) to (5,5), and state when that heuristic needs reconsideration.
The bound is 7 steps. Different motion primitives or costs, such as diagonal unit-cost moves, change the appropriate heuristic.
''')
module('16-fpga', 'HDL and FPGA design', 'Silicon', 'Describe hardware, simulate it, and respect synchronous interfaces.', ['06-digital','08-architecture'], ['hdl'], 'counter', '''
RTL describes concurrent hardware
RTL expresses registers and combinational logic rather than a sequence of software operations on one processor. Separate combinational calculations from clocked state updates. In common Verilog practice, nonblocking assignments model clocked registers so right-hand sides use pre-edge state. Fully assign combinational outputs on every path to avoid unintended latches. Simulation semantics and synthesis interpretation both matter.
A synchronous counter computes next_count=(count+1) modulo 2^N on each enabled clock edge
A 4-bit counter advances from 14 to 15 to 0. Reset behavior must be specified: synchronous reset acts on a clock edge, while asynchronous reset can assert independently of the clock. Reset release also requires careful timing design.
HDL code that runs in a simulator is not necessarily synthesizable or suitable for an FPGA implementation.
Starting from 6, list four subsequent values of an enabled 3-bit counter.
The values are 7, 0, 1, 2. The wrap is modulo eight.

Simulation and self-checking testbenches
A testbench drives input sequences, advances simulation time, and compares outputs against a model or assertion. Good tests include reset, boundary values, disabled operations, and interaction between controls. A waveform helps diagnose a failure, but an automated pass/fail check prevents visual inspection from becoming the only verification method. Keep the reference model simpler and independently expressed when possible.
A scoreboard compares observed transactions with expected transactions
For a counter, test that reset clears it, enable=0 holds it, and overflow wraps exactly. If a test checks only the first increment after reset, an implementation that saturates at its maximum can incorrectly pass.
Code coverage and a green testbench do not prove the specification is complete or all corner cases were exercised.
Name a sequence that distinguishes a wrapping 2-bit counter from a saturating one.
Reset, then apply four enabled edges. A wrapping counter returns to zero; a saturating counter stays at three.

Clock domains and handshakes
Signals crossing unrelated clock domains can violate sampling timing. A two-flop synchronizer reduces the probability that a single-bit level’s metastability propagates; it does not guarantee capture of every narrow pulse. Multi-bit data needs a coherent transfer protocol, such as a handshake or asynchronous FIFO. Clock-domain crossing is a protocol and physical-design problem, not just inserting two registers everywhere.
A ready/valid transfer occurs on a clock edge where ready AND valid is true
If valid is asserted and ready is low, a producer must keep the payload stable until the transfer under the stated protocol. This prevents backpressure from silently dropping or changing data. Across clock domains, use a suitable CDC structure rather than directly sharing ready/valid signals.
Synchronizing each bit of a changing bus independently can produce a word that never existed at the source.
If valid stays high for three cycles and ready is [0,0,1], how many transfers occur?
One transfer occurs on the third edge, assuming a common clock and stable payload until acceptance.
''')
module('17-vlsi', 'CMOS and VLSI fundamentals', 'Silicon', 'Reason about transistor networks, delay, energy, and scaling.', ['04-devices','16-fpga'], ['devices'], 'power', '''
CMOS gates from transistor networks
Static CMOS pairs a pull-up network with a complementary pull-down network. For valid steady inputs, one network ideally connects the output to a rail while the other is off. A NAND gate uses series NMOS devices and parallel PMOS devices; a NOR gate reverses those network arrangements. Transistor sizing influences resistance, capacitance, rise/fall balance, and input loading. Logic equivalence alone does not capture these physical tradeoffs.
An inverter implements Y=NOT A with one PMOS pull-up and one NMOS pull-down
For input low, the PMOS conducts and the NMOS is off, pulling the output high. During a transition both may partially conduct, causing short-circuit current. Real devices also leak even when the ideal switch model says off.
Static CMOS does not consume literally zero power; leakage and switching currents remain.
How many transistors are in a basic two-input static CMOS NAND, and how are the NMOS devices arranged?
Four transistors: two series NMOS and two parallel PMOS, ignoring additional buffering or specialized cell features.

Dynamic power and delay
Charging capacitance consumes energy, and repeated switching produces dynamic power. Supply voltage has a squared effect in the simple capacitive power model, but reducing voltage also slows devices and can threaten timing. Activity factor must have a clear transition convention. Cell delay depends on input slew, load, voltage, temperature, and process; a single RC number is an intuition-building approximation.
Pdynamic=α C V² f, where α counts effective 0→1 charging events per cycle
With α=0.1, C=10 pF, V=1 V, and f=100 MHz, dynamic power is 0.1 mW. Doubling voltage multiplies this term by four if all other quantities remain unchanged. Leakage is a separate term.
Clock gating reduces switching activity; power gating targets leakage by disconnecting a power domain and requires state and isolation planning.
Find dynamic power for α=0.2, C=5 pF, V=1 V, f=200 MHz.
P=0.2 mW under the stated activity convention.

Layout, parasitics, and variability
A layout gives physical shapes to transistors and interconnect. Design rules constrain geometry, while extraction estimates parasitic resistance and capacitance. Layout-versus-schematic checks connectivity against the intended circuit. Process variation and operating conditions create a distribution of behavior, so designers examine corners and margins. A nominal simulation is evidence for one model and condition, not for every manufactured part.
A first-order interconnect delay estimate scales with effective R×C
Doubling a wire’s length can approximately double both resistance and capacitance, making an unbuffered distributed-wire delay grow roughly with length squared in a simplified model. This explains why placement and buffering can matter as much as gate count.
Passing design-rule checks does not prove functional correctness or timing closure.
Explain the distinct questions answered by DRC and LVS.
DRC checks geometric manufacturing rules. LVS checks whether extracted connectivity matches the reference netlist; both are needed and neither replaces timing or functional verification.
''')
module('18-verification', 'Digital verification', 'Silicon', 'Turn requirements into tests, assertions, coverage, and counterexamples.', ['16-fpga'], ['hdl'], 'fifo', '''
Specifications and scoreboards
Verification begins with an observable contract. Define what a block does for valid operations, invalid operations, simultaneous events, reset, and backpressure. A scoreboard tracks expected transactions independently from the implementation. Comparing final values alone can miss ordering errors or dropped intermediate data. Reproducible randomized tests supplement directed cases, and every random failure should preserve its seed and stimulus trace.
For a FIFO, output order must equal accepted input order
A four-entry FIFO may accept writes until full and reads until empty. The contract must state whether simultaneous read and write at full are allowed and how occupancy changes. Without that rule, two implementations can disagree while each appears reasonable.
A testbench copied line-for-line from the RTL can reproduce the same design mistake instead of detecting it.
List three boundary conditions for a FIFO test beyond an ordinary write followed by read.
Empty read, full write, pointer wraparound, reset with queued data, and simultaneous read/write are useful cases; define expected behavior for each.

Assertions and formal reasoning
Assertions express properties that should hold over states or time. Simulation checks them on visited traces; formal tools attempt to prove them under explicit assumptions or produce counterexamples. Bounded checking explores only a finite depth unless an induction argument or another complete method extends it. Assumptions constrain the environment and can accidentally exclude the very bug you wanted to find.
FIFO occupancy invariant: 0 ≤ count ≤ depth
A counterexample that reaches count=depth+1 points to an overflow or update-rule failure. A proof that assumes writes never occur at full cannot establish the design’s specified behavior for a write at full. The environment contract must be reviewed with the property.
A proof under contradictory assumptions is vacuous; a green result is not enough without checking reachability and assumption consistency.
Why is “if full, occupancy never increases” more informative than checking occupancy only at test completion?
It constrains every relevant transition and can catch transient overflow even if later reads bring the final count back into range.

Coverage, reset, and sign-off evidence
Coverage measures which structures or scenarios were exercised, not whether the design is correct. Functional coverage comes from requirements: every operation, boundary, and relevant interaction should have an observable witness. Reset behavior deserves dedicated tests because initialization bugs can disappear after a few cycles. A verification report should distinguish passing tests, untested scenarios, waived checks, and known limitations.
Coverage fraction = exercised defined scenarios / total defined scenarios
If ten specified scenarios exist and eight have been demonstrated, functional coverage is 80% for that model. Adding missing scenarios can lower the percentage while improving the verification plan. A percentage without the scenario definition has little meaning.
100% line coverage can coexist with a wrong protocol implementation or an omitted requirement.
A FIFO passes ordinary traffic but has no test for reset while full. What evidence is missing?
The reset-with-data requirement lacks a witness. Add a test that fills the FIFO, resets it, checks empty state, and verifies stale data is not returned as valid.
''')
module('19-physical', 'ASIC implementation and timing', 'Silicon', 'Follow RTL through synthesis, placement, clocks, routing, and checks.', ['17-vlsi','18-verification'], ['asic'], 'timing', '''
From RTL to gates
Synthesis maps a hardware description into a gate-level implementation using a target cell library and constraints. The same RTL can produce different area and timing depending on the library, clock target, and optimization choices. Constraints describe intended clocks and external timing relationships. Inspect reports and inferred hardware; an accidental latch or enormous mux may be legal synthesis output but a poor implementation of the intended architecture.
Area and timing are properties of the mapped implementation under specified constraints
A 32-way combinational selector may become a deep mux tree. Registering its output changes the interface latency but can improve timing partitioning. Such a change is architectural and must be reflected in the testbench and downstream protocol.
Successful synthesis does not mean the design meets timing or fits a particular FPGA or ASIC area budget.
Name three artifacts to retain after synthesis for a reproducible comparison.
Keep the RTL revision, constraint file, and mapped netlist/report set, along with tool version and library identity.

Static timing analysis
Static timing analysis checks timing paths without enumerating functional input sequences. Setup checks constrain maximum delay; hold checks constrain minimum delay. Clock relationships, uncertainty, exceptions, and input/output delays shape the result. False-path and multicycle exceptions must follow a real design argument, because they can hide failures. Slack is meaningful only when the path is correctly constrained.
Setup slack = required arrival time − actual arrival time
With a 10 ns requirement and 10.8 ns actual arrival, slack is −0.8 ns and the path fails setup. A positive slack at one process corner does not establish closure at every required corner. Hold timing requires its own minimum-delay analysis.
Lowering the clock frequency generally does not repair a hold failure; hold compares behavior around the same capture edge.
Find setup slack when required arrival is 8 ns and actual arrival is 7.4 ns.
Slack is +0.6 ns under the given timing model. Check uncertainty and corner assumptions before interpreting it as final margin.

Physical implementation and sign-off
Floorplanning allocates regions and power structure. Placement locates cells, clock-tree synthesis distributes the clock, and routing connects wires. Extraction updates parasitic models for timing and power analysis. Congestion, IR drop, electromigration, DRC, LVS, and testability all influence manufacturability. An educational open flow demonstrates these stages but does not establish foundry-qualified sign-off or production readiness on its own.
IR drop = current × effective supply-path resistance
A 0.5 A load through an effective 0.1 Ω supply path loses 50 mV. On a 1 V rail this is a 5% drop, potentially affecting cell delay and noise margin. Dynamic supply droop can require a richer model than this DC estimate.
A generated GDS file is an output artifact, not proof that a chip is ready to manufacture.
What changes between pre-route and post-route timing analysis?
Post-route analysis uses more realistic extracted interconnect parasitics. Paths can become slower or faster than estimated, requiring timing repair and renewed checks.
''')
module('20-soc', 'System-on-chip integration', 'Silicon', 'Integrate processors, memory, buses, peripherals, clocks, and boot flows.', ['19-physical','10-rtos'], ['isa','asic'], 'soc', '''
Memory maps and bus transactions
An SoC connects independently designed blocks through explicit interfaces. A memory map assigns address ranges to RAM, ROM, and peripherals. Address decoding must handle alignment, access width, permissions, and unmapped addresses. Bus protocols define when a request is accepted and how a response returns. A register specification becomes a contract shared by RTL, firmware, tests, and documentation.
A region with base B and size S contains addresses B ≤ address < B+S
A 4 KiB peripheral window at 0x40000000 ends at 0x40000FFF inclusive. Address 0x40001000 belongs outside it. Registers spaced four bytes apart typically require alignment checks for 32-bit word accesses, depending on the bus contract.
A successful bus handshake does not imply the addressed operation was valid; responses must distinguish success from defined error conditions.
Give the last included address of a 256-byte window starting at 0x1000.
The last address is 0x10FF. The half-open interval is [0x1000,0x1100).

Interrupts, DMA, and coherence
A peripheral may signal completion through an interrupt or transfer blocks through DMA. Memory coherence determines whether different agents observe consistent data. A CPU cache can contain a stale copy after DMA writes memory; a dirty cache line can later overwrite DMA data. The correct maintenance and ordering depend on the platform and memory attributes. Design buffer ownership as a state machine rather than an informal convention.
Buffer ownership transitions: CPU prepares → device owns → device completes → CPU consumes
Before a noncoherent device reads a CPU-produced buffer, dirty data may need to be cleaned to memory. After the device writes, stale CPU cache lines may need invalidation. Barriers and completion checks enforce ordering but must match the architecture’s specified semantics.
Volatile does not make a DMA buffer coherent or flush a CPU cache.
Why must the CPU avoid modifying a transmit buffer while a DMA engine owns it?
The device could observe a mixture of old and new bytes. A defined completion event must return ownership before reuse.

Boot, reset, and power domains
Boot begins from a defined reset state and establishes the environment required by later software. Typical stages configure clocks, memory, stacks, and device state before applications run. Multiple power and clock domains introduce sequencing, isolation, retention, and reset-crossing concerns. Secure boot verifies an image against an authenticated trust policy; it does not automatically solve rollback, key provisioning, or runtime compromise.
A boot chain is only as strong as the trust anchor and each authenticated transition
If immutable boot code verifies a second-stage image but the second stage loads an unchecked application, the chain stops protecting the later code. A recovery path must preserve the same trust rules while handling interrupted updates and corrupted images.
Resetting a processor does not necessarily reset every peripheral or erase retained state; inspect domain behavior.
Describe one test for a power failure during a firmware update.
Interrupt the update at several write boundaries, reboot, and verify that either the previous valid image or a fully verified new image runs, with a defined recovery path when neither is valid.
''')
module('21-linux', 'Embedded Linux, networks, and security', 'Embedded', 'Connect devices to operating systems and reliable remote interfaces.', ['20-soc'], ['linux'], 'packet', '''
Processes, drivers, and device descriptions
An operating system isolates processes and mediates access to hardware. A driver translates OS-facing operations into device-specific behavior. A device tree describes hardware topology and resources for platforms that use it; it is not executable driver code. Build configuration, kernel version, bootloader, root filesystem, and hardware description must agree. Start debugging from boot logs and the simplest observable interface.
User process → system call → kernel subsystem → driver → peripheral
A serial device can fail because its driver is absent, its clock is wrong, its pin mux is wrong, or its device description names the wrong address. Recompiling the application alone cannot fix these underlying integration errors.
A node in a device tree does not manufacture missing hardware or guarantee that a compatible driver is enabled.
Name evidence that distinguishes an application permission problem from a peripheral failing to probe.
Check whether the device exists and whether kernel logs show a successful probe, then inspect access permissions and the application’s actual error.

Packets, framing, and resilient protocols
A byte stream does not preserve application-message boundaries. Define framing, lengths, versioning, checksums, and timeouts explicitly. Network protocols differ in reliability and ordering guarantees, but applications still need limits and recovery behavior. Parse untrusted input defensively and reject oversized or malformed frames before allocating large buffers or changing state. A protocol should remain understandable after a dropped byte or interrupted connection.
A frame can use version + payload length + payload + integrity field
For a two-byte big-endian payload length, bytes 0x01 0x00 describe 256 bytes. A parser receiving only 100 bytes must wait or timeout; it must not treat missing bytes as valid data. Set an application maximum even if the field can encode more.
A TCP read returning 20 bytes does not prove that one complete 20-byte application message has arrived.
A frame declares 2000 bytes but your maximum is 512. What should the parser do before allocating payload storage?
Reject the frame or close/reset the parser according to the protocol. Do not trust the length merely because it fits the field width.

Threat models and update design
Security begins by identifying assets, attackers, trust boundaries, and plausible failure consequences. Debug ports, stored credentials, network parsers, and update mechanisms each expose different attack surfaces. Cryptographic verification requires correct key management and implementation; designing a novel cipher is not a useful shortcut. Treat fault recovery and secure updating as normal operating requirements, including interrupted writes and version rollback rules.
Authenticity answers who authorized data; integrity answers whether data changed
A CRC can detect many accidental transmission errors but an attacker can recompute it. A signature can authenticate an update under a trusted public key, while a version policy may be needed to reject an older but validly signed vulnerable image.
Encryption alone does not imply authenticity, and a signed image alone does not establish a complete secure lifecycle.
Why might a device reject a correctly signed firmware image with a lower version number?
A rollback policy can prevent reinstallation of known-vulnerable older software. The version state and recovery process also need protection.
''')
module('22-product', 'PCB, power, and product reliability', 'Electronics', 'Turn a schematic into a measurable, maintainable physical system.', ['05-analog','13-rf','21-linux'], ['pcb','em'], 'thermal', '''
Schematic capture and PCB return paths
A schematic records intended connectivity; a PCB implements that connectivity in a physical field environment. Placement, return-current paths, decoupling, connector pinouts, and assembly access influence behavior. Use electrical-rule checking and design-rule checking, then inspect assumptions the tools cannot know. Label test points and keep a bring-up plan so a manufactured board can be diagnosed rather than merely powered and hoped to work.
Loop inductance and return-path discontinuities can create noise even when net connectivity is correct
A high-frequency signal routed across a split reference plane forces return current around the gap, increasing loop area. Keeping an appropriate continuous return reference and locating decoupling close to supply pins can reduce unwanted impedance.
“Ground” is not a perfect equipotential surface at all frequencies. A correct net name does not guarantee a good return path.
List three checks before powering a newly assembled low-voltage board.
Inspect polarity and assembly, measure for shorts with power removed, and review a current-limited power-up sequence with expected rail values and accessible test points.

Power conversion and thermal budgets
Linear regulators dissipate the voltage difference as heat; switching converters trade additional circuit complexity and switching noise for potentially higher efficiency. Choose a regulator using load transients, dropout, stability requirements, layout, and thermal conditions, not only nominal current. Thermal resistance is a simplified steady-state model whose value depends strongly on the board and environment. Measure temperature after a controlled stabilization period.
PLDO=(Vin−Vout)I; approximate ΔT=P θJA under the specified thermal conditions
Dropping 5 V to 3.3 V at 0.2 A dissipates 0.34 W. If effective θJA is 100 °C/W, the estimated rise is 34 °C. At 40 °C ambient, the simplified junction estimate is 74 °C, before other heat sources and model uncertainty.
A package’s headline current rating is not a guarantee that it can dissipate the required power on your board.
Estimate LDO dissipation for 12 V to 5 V at 0.1 A and temperature rise at 80 °C/W.
Power is 0.7 W and estimated rise is 56 °C. This can motivate a different supply architecture.

Reliability, EMC, and test strategy
Reliability work asks how the product behaves across variation, aging, misuse, and failures. Define environmental limits and observable acceptance tests. EMI emission and susceptibility arise from current loops, coupling paths, and bandwidth; fixing them late can require board changes. Design-for-test adds access and diagnostics during development. A structured failure analysis prioritizes credible causes and mitigations without pretending a numerical score proves safety.
A test matrix crosses operating conditions with required behaviors
For a sensor board, test supply extremes, temperature range, cable attachment, reset during traffic, and sensor disconnection. Record the expected error report and recovery for each condition. An unexplained reboot is a failed diagnostic requirement even if the board later resumes output.
One working prototype is not evidence of production yield, compliance, or long-term reliability.
Define a measurable requirement for sensor disconnection rather than saying the firmware should handle it gracefully.
For example: detect disconnection within 100 ms, flag data invalid, report a specific fault, and resume only after a defined revalidation sequence. Choose timings appropriate to the application.
''')
module('23-capstones', 'Edge intelligence and engineering capstones', 'Integration', 'Integrate disciplines and defend results with reproducible evidence.', ['22-product','15-robotics'], ['isa','control','signals'], 'quantize', '''
Edge inference and resource budgets
An embedded ML model is one component of a sensing system. Data collection, preprocessing, memory, latency, energy, and failure behavior determine whether it is useful. Quantization represents values with fewer bits and introduces scale-dependent error. Evaluate the deployed arithmetic on representative held-out data, including unusual operating conditions. A smaller model is not automatically a better system if it loses the behavior the product needs.
Uniform affine quantization: q=clip(round(x/scale)+zero_point); reconstructed x=scale(q−zero_point)
With scale=0.1 and zero point=0, x=0.26 maps to q=3 and reconstructs as 0.3, an error of 0.04. Values outside the integer range saturate, creating a different error regime from small rounding noise.
Accuracy measured on training data does not establish generalization, and a desktop timing result does not establish target-device latency.
Quantize x=−0.37 with scale=0.1 and zero point=0, assuming an adequate signed integer range.
q=−4 and reconstructed x=−0.4; reconstruction error is −0.03 using reconstructed minus original.

Architecture tradeoffs and verification plans
A capstone should begin with requirements that can fail. Allocate timing, memory, power, and error budgets to subsystems, then identify the interfaces that carry assumptions between them. Compare alternatives using measured constraints rather than tool popularity. A verification plan connects each requirement to a test, retained artifact, and acceptance threshold. State which claims are simulation-only and which were demonstrated on hardware.
End-to-end latency includes acquisition + processing + queueing + communication + actuation
If acquisition takes 2 ms, processing 3 ms, queueing up to 4 ms, and actuation 1 ms, the budget is 10 ms. Ignoring queueing would understate the bound by 40%. Measurement must cover the same endpoints used by the requirement.
A collection of individually passing modules can still fail at integration because their assumptions disagree.
Allocate a 20 ms latency requirement among four stages and describe how you would test the total.
One possible allocation is 4, 6, 5, and 5 ms. Timestamp the defined input and output events under worst expected contention, and verify both stage and end-to-end limits.

Evidence, review, and portfolio delivery
An engineering portfolio should let another person reproduce a result and inspect its limits. Include the problem, architecture, interface contracts, implementation, tests, raw observations, and a discussion of failures. Separate a proposed feature from an implemented feature and a passing simulation from a measured board. Review is an opportunity to find incorrect assumptions before the artifact is reused. A polished demonstration is useful, but it does not replace the underlying evidence.
Requirement → test procedure → observed result → conclusion → known limitation
A sensor-to-decision capstone can retain a CSV trace, a latency histogram, a reproducible test command, and a fault-injection result. A CPU capstone can retain instruction traces, directed tests, and unsupported-instruction behavior. Each demonstrates a different claim and should be labeled accordingly.
A screenshot of a waveform alone is insufficient for another learner to reproduce the experiment or diagnose a regression.
Write one defensible completion statement for a simulated robot controller and one claim you cannot make without hardware evidence.
You can claim that specified simulated trajectories met their numerical error bounds. You cannot claim physical tracking accuracy, motor temperature, or real-world collision avoidance without corresponding validation.
''')

PATHS = {
 'complete': dict(title='Complete ECE journey', description='All 24 modules in prerequisite order. Begin with the bench and finish with an integrated portfolio.', modules=[m['id'] for m in MODULES]),
 'embedded': dict(title='Embedded & firmware', description='From bits and circuits to peripherals, real-time software, SoCs, and Linux.', modules=['00-bench','01-math','02-dc','03-dynamics','04-devices','05-analog','06-digital','07-c','08-architecture','09-mcu','10-rtos','16-fpga','17-vlsi','18-verification','19-physical','20-soc','21-linux']),
 'silicon': dict(title='VLSI, architecture & SoC', description='Logic, CPUs, RTL, verification, CMOS, physical implementation, and integration.', modules=['00-bench','01-math','02-dc','03-dynamics','04-devices','06-digital','07-c','08-architecture','09-mcu','10-rtos','16-fpga','17-vlsi','18-verification','19-physical','20-soc']),
 'robotics': dict(title='Robotics & control', description='Sensing, embedded timing, signals, feedback, geometry, and motion.', modules=['00-bench','01-math','02-dc','03-dynamics','06-digital','07-c','08-architecture','09-mcu','10-rtos','11-dsp','14-control','15-robotics']),
 'communications': dict(title='Signals, communications & RF', description='Analog foundations through sampling, modulation, fields, and transmission lines.', modules=['00-bench','01-math','02-dc','03-dynamics','04-devices','05-analog','06-digital','07-c','11-dsp','12-communications','13-rf']),
}
