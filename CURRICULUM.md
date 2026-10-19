# Curriculum

An original, concise survey course. Each module contains three lessons, a numerical lab, and a checkpoint. Specialist depth and hardware qualification are described in [SCOPE.md](SCOPE.md).

## 00 · The engineering bench

Measure, predict, and keep evidence before building hardware.

- [A reproducible engineering notebook](lessons/00-bench/01.md)
- [Uncertainty and significant figures](lessons/00-bench/02.md)
- [Loading and safe low-voltage experiments](lessons/00-bench/03.md)

## 01 · Mathematics and computation

Use complex numbers, linear systems, and numerical models as engineering tools.

- [Complex numbers describe phase](lessons/01-math/01.md)
- [Linear algebra for networks](lessons/01-math/02.md)
- [Differential equations and numerical steps](lessons/01-math/03.md)

## 02 · DC circuits and networks

Derive voltages and currents from conservation laws.

- [Ohm’s law and power](lessons/02-dc/01.md)
- [Kirchhoff’s laws and nodal analysis](lessons/02-dc/02.md)
- [Thévenin equivalents and loading](lessons/02-dc/03.md)

## 03 · Transients and AC circuits

Understand stored energy, settling time, resonance, and frequency response.

- [Capacitors, inductors, and state](lessons/03-dynamics/01.md)
- [The RC step response](lessons/03-dynamics/02.md)
- [Impedance, filters, and resonance](lessons/03-dynamics/03.md)

## 04 · Semiconductors and devices

Connect junction physics to practical diode and transistor models.

- [Diodes and junctions](lessons/04-devices/01.md)
- [BJTs and small-signal reasoning](lessons/04-devices/02.md)
- [MOSFET operation and switching](lessons/04-devices/03.md)

## 05 · Analog and mixed-signal design

Design gain, acquisition, and noise budgets around real component limits.

- [Feedback and operational amplifiers](lessons/05-analog/01.md)
- [Sampling and quantization](lessons/05-analog/02.md)
- [Noise and dynamic range](lessons/05-analog/03.md)

## 06 · Digital logic and state machines

Build combinational functions and reason about clocked state.

- [Boolean logic and combinational circuits](lessons/06-digital/01.md)
- [Registers, setup, and hold](lessons/06-digital/02.md)
- [Finite-state machines](lessons/06-digital/03.md)

## 07 · C and systems programming

Understand representations, memory ownership, and register operations.

- [Integers and bit operations](lessons/07-c/01.md)
- [Pointers, arrays, and lifetimes](lessons/07-c/02.md)
- [Memory-mapped I/O and concurrency](lessons/07-c/03.md)

## 08 · Computer architecture

Follow instructions through a datapath, pipeline, and memory hierarchy.

- [Instructions and datapaths](lessons/08-architecture/01.md)
- [Pipelines and hazards](lessons/08-architecture/02.md)
- [Caches and locality](lessons/08-architecture/03.md)

## 09 · Microcontrollers and peripherals

Connect firmware to timers, serial links, interrupts, and sensors.

- [GPIO, timers, and PWM](lessons/09-mcu/01.md)
- [UART, SPI, and I²C](lessons/09-mcu/02.md)
- [Interrupts, DMA, and latency](lessons/09-mcu/03.md)

## 10 · Real-time systems

Design for deadlines, bounded queues, and predictable failure recovery.

- [Deadlines and schedulability](lessons/10-rtos/01.md)
- [Synchronization and priority inversion](lessons/10-rtos/02.md)
- [Watchdogs and fault recovery](lessons/10-rtos/03.md)

## 11 · Signals and digital signal processing

Move between samples, spectra, filters, and fixed-point arithmetic.

- [Sampling and aliasing](lessons/11-dsp/01.md)
- [Convolution and FIR filters](lessons/11-dsp/02.md)
- [Spectra, windows, and fixed-point limits](lessons/11-dsp/03.md)

## 12 · Communication systems

Build a link from bits through modulation, noise, and detection.

- [Modulation and complex baseband](lessons/12-communications/01.md)
- [Noise, bandwidth, and capacity](lessons/12-communications/02.md)
- [Error detection and link budgets](lessons/12-communications/03.md)

## 13 · Electromagnetics and RF

Know when wires become transmission lines and radiation matters.

- [Fields, waves, and wavelength](lessons/13-rf/01.md)
- [Transmission lines and reflections](lessons/13-rf/02.md)
- [Antennas, matching, and S-parameters](lessons/13-rf/03.md)

## 14 · Control systems

Model dynamics, close feedback loops, and examine stability.

- [Models, feedback, and poles](lessons/14-control/01.md)
- [PID and saturation](lessons/14-control/02.md)
- [State-space models and observers](lessons/14-control/03.md)

## 15 · Robotics and autonomy

Connect geometry, estimation, planning, and actuator behavior.

- [Frames and forward kinematics](lessons/15-robotics/01.md)
- [Odometry and sensor fusion](lessons/15-robotics/02.md)
- [Planning and robot software](lessons/15-robotics/03.md)

## 16 · HDL and FPGA design

Describe hardware, simulate it, and respect synchronous interfaces.

- [RTL describes concurrent hardware](lessons/16-fpga/01.md)
- [Simulation and self-checking testbenches](lessons/16-fpga/02.md)
- [Clock domains and handshakes](lessons/16-fpga/03.md)

## 17 · CMOS and VLSI fundamentals

Reason about transistor networks, delay, energy, and scaling.

- [CMOS gates from transistor networks](lessons/17-vlsi/01.md)
- [Dynamic power and delay](lessons/17-vlsi/02.md)
- [Layout, parasitics, and variability](lessons/17-vlsi/03.md)

## 18 · Digital verification

Turn requirements into tests, assertions, coverage, and counterexamples.

- [Specifications and scoreboards](lessons/18-verification/01.md)
- [Assertions and formal reasoning](lessons/18-verification/02.md)
- [Coverage, reset, and sign-off evidence](lessons/18-verification/03.md)

## 19 · ASIC implementation and timing

Follow RTL through synthesis, placement, clocks, routing, and checks.

- [From RTL to gates](lessons/19-physical/01.md)
- [Static timing analysis](lessons/19-physical/02.md)
- [Physical implementation and sign-off](lessons/19-physical/03.md)

## 20 · System-on-chip integration

Integrate processors, memory, buses, peripherals, clocks, and boot flows.

- [Memory maps and bus transactions](lessons/20-soc/01.md)
- [Interrupts, DMA, and coherence](lessons/20-soc/02.md)
- [Boot, reset, and power domains](lessons/20-soc/03.md)

## 21 · Embedded Linux, networks, and security

Connect devices to operating systems and reliable remote interfaces.

- [Processes, drivers, and device descriptions](lessons/21-linux/01.md)
- [Packets, framing, and resilient protocols](lessons/21-linux/02.md)
- [Threat models and update design](lessons/21-linux/03.md)

## 22 · PCB, power, and product reliability

Turn a schematic into a measurable, maintainable physical system.

- [Schematic capture and PCB return paths](lessons/22-product/01.md)
- [Power conversion and thermal budgets](lessons/22-product/02.md)
- [Reliability, EMC, and test strategy](lessons/22-product/03.md)

## 23 · Edge intelligence and engineering capstones

Integrate disciplines and defend results with reproducible evidence.

- [Edge inference and resource budgets](lessons/23-capstones/01.md)
- [Architecture tradeoffs and verification plans](lessons/23-capstones/02.md)
- [Evidence, review, and portfolio delivery](lessons/23-capstones/03.md)

