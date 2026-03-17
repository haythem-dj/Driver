# Driver

## Overview

This project is a documented simulation and design of DC Motor Driver

## Objectives

- Model the motor mathematically
- Simulate the model response
- Design a MOSFET based driver
- Validate swiching behavior using simulation
- Integrate the 2 systems
- (Optional) Implement and simulate speed control

## How to run

### Python simulation

Before you run the simulation, you need to setup a virtual envirement with all the needed libraries.
You only need to do this once.

```bash
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Then cou can run the simulation.

```bash
python simulation.py
```

## LICENSE

This project is licensed under the [MIT License](LICENSE).
