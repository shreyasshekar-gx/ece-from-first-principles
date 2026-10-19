# A robot that can explain its motion

Simulate differential-drive motion and compare integration with a closed-form constant-turn trajectory.

Prerequisite modules: 14-control, 15-robotics.

## Build in stages

1. Define body/world frames and units.
2. Integrate wheel velocities using an explicit time step.
3. Compare straight and circular trajectories with analytic predictions.
4. Add saturation, delayed sensing, and a stop-on-stale-command state.

## Acceptance criteria

- Equal wheel velocities produce zero heading change.
- Opposite wheel velocities rotate the robot without translating in the ideal model.
- Constant-turn position error is below 0.01 m at the supplied 1 ms time step.
- Record how error changes when the step is halved.

## Executable reference

```bash
python3 projects/reference.py robot-controller
python3 -m unittest discover -s tests -v
```

Study `projects/reference.py` after making a prediction. Create your own implementation in a separate learner directory. The tests validate the supplied reference; adapt their imports to grade your own implementation.

## Extension

Add obstacle inflation and a planner before considering a physical chassis. Physical collision avoidance and actuator limits require separate validation.

## Submission

Include requirements, interface contract, source, test command, observed output, limitations, and a short reflection on one failed approach. Score each of correctness, test evidence, explanation, and reproducibility from 0–3. Require at least 2 in every category before calling the project complete.
