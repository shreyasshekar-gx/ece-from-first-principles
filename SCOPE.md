# Scope and expansion map

Edition 0.1 provides a continuous beginner-to-specialization **survey**: 72 concise lessons with worked examples, exercises, solutions, module checkpoints, and 24 runnable numerical models. It is suitable as a guided first pass and a repository foundation. It does not replace the depth of an ECE degree, a specialist textbook, laboratory supervision, or production design review.

## What “complete” means in this edition

Every listed lesson is written and linked; every module has a runnable numerical experiment and a checkpoint. All five project briefs include executable reference behavior and acceptance tests. There are no empty lesson pages advertised as completed content. The sequence is complete at survey depth; an exhaustive professional A–Z treatment remains a much larger publishing project.

The baseline is simulation-first. It includes no manufactured PCB, taped-out ASIC, flashed board, measured RF link, or physical robot. It does not claim vendor certification, engineering licensure, or guaranteed employment outcomes.

## Specialist expansion backlog

These are **additional depth topics, not completed lessons**. Each should become a separate derivation, implementation, assessment, and evidence package before being added to the catalog.

| Discipline | Covered in the survey | Depth still to author and validate |
|---|---|---|
| Mathematics | Phasors, linear equations, Euler integration | Calculus sequence; probability and random processes; optimization; numerical conditioning; transforms and differential-equation proofs |
| Circuits | KCL/KVL, Thévenin, first-order RC, impedance | Dependent sources; RLC poles and damping; two-port networks; sensitivity; SPICE comparisons and convergence |
| Devices/analog | Junction models, BJT/MOS behavior, feedback, ADC/noise | Semiconductor transport; bias circuits; differential pairs; current mirrors; compensation; oscillator and PLL design; precision references; DAC architectures |
| Digital/C | Boolean functions, registers/FSMs, masks, memory | Logic minimization; arithmetic architectures; ABI and linker scripts; startup assembly; memory models; MISRA-style reviews; fixed-point libraries |
| Architecture | Datapath, CPI, hazards, cache basics | Full ISA interpreter; branch prediction; out-of-order execution; virtual memory/TLBs; coherence protocols; multicore; formal ISA refinement |
| Embedded/RTOS | GPIO/timers, UART/SPI/I²C, interrupts/DMA, scheduling | Board-specific drivers; real interrupt vectors; CAN, USB, Ethernet; RTOS ports; response-time analysis; low-power measurement; bootloader and OTA implementation |
| DSP/communications | Sampling, FIR/DFT, BPSK, noise/capacity, link budget | Z/Laplace-transform derivations; IIR design; FFT implementation; multirate DSP; QAM/OFDM; synchronization; equalization; channel coding; information theory; SDR measurements |
| EM/RF | Wavelength, reflection, matching, S-parameters | Maxwell boundary-value problems; waveguides; microwave networks; Smith charts; antenna design; LNA/mixer/PA design; VNA calibration; optical and satellite links |
| Control/robotics | Feedback, PID concepts, states, kinematics, odometry, grid planning | Frequency-domain stability proofs; discrete controller implementation; LQR/MPC; EKF; trajectory generation; dynamics; SLAM; ROS 2 packages; real actuator testing |
| FPGA | RTL semantics, counter testbench, handshakes/CDC concepts | Board constraints; FPGA BRAM/DSP use; asynchronous FIFO RTL; AXI streaming; timing closure; formal CDC review; hardware debug |
| VLSI/verification | CMOS gates, power, parasitics, scoreboards/assertions | Cell characterization; analog layout; UVM environment; constrained random coverage; formal tool exercises; DFT/scan/ATPG; low-power intent |
| ASIC/SoC | Synthesis/STA/flow concepts, register maps, boot/coherence | Pinned PDK and tool flow; actual RTL-to-GDS artifact; multicorner timing; IR/EM analysis; DRC/LVS qualification; APB/AXI implementation; DDR/PCIe; chiplet interconnect |
| Linux/product | Driver/device-tree concepts, bounded framing, PCB/power/reliability | Kernel module and driver labs; Buildroot/Yocto images; secure update implementation; PCB fabrication/bring-up; EMC measurements; environmental and production testing |
| Edge intelligence | Quantization and deployment budgets | Dataset and trained model; target deployment; accuracy/latency/energy benchmarking; drift and fallback behavior |

## Hardware progression

1. Complete the laptop models and calculations.
2. Use a current-limited isolated low-voltage bench for component experiments, with appropriate instruction on instruments and ratings.
3. Select a specific board and pin toolchain versions before writing a board lab. Pin muxes and voltage compatibility are board-specific.
4. For FPGA/ASIC work, retain simulator, synthesis tool, library/PDK, constraints, and reports. A successful model or GDS export is not manufacturing sign-off.
5. For robotics and power work, establish actuator limits and fault behavior before energizing mechanisms. The course does not contain mains-power experiments.

## Reading and version status

Primary reference destinations were checked during authoring on 20 October 2026. ROS documentation returned an access-denied page in the research environment, and the Feedback Systems homepage did not load through the retrieval tool; these links are further-reading destinations, not claims of fully verified page contents. FreeRTOS returned no extractable body in that tool. The core lessons use stable, explicitly stated models rather than undocumented current APIs.

All original lessons need ongoing subject-matter review, especially before adoption in formal teaching. Automated tests establish selected numerical and software properties, not comprehensive pedagogical or hardware correctness.
