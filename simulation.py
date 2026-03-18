import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt


def rpm2rad(s):
    return s * (np.pi / 30)


def rad2rpm(s):
    return s * (30 / np.pi)


def model(t, X, U, params):
    R = params["R"]
    L = params["L"]
    b = params["b"]
    J = params["J"]
    Kv = params["Kv"]
    Kt = params["Kt"]

    V = U[0]

    i = X[0]
    w = X[1]

    di = (1 / L) * V - (R / L) * i - (Kv / L) * w
    dw = (Kt / J) * i - (b / J) * w

    return [di, dw]


params = {
    "R": 2.68,
    "L": 0.514e-3,
    "b": 1.11e-4,
    "J": 21.2e-7,
    "Kv": 1 / rpm2rad(223),
    "Kt": 42.9e-3,
}

tstart = 0
tfinish = 0.5
tspan = np.linspace(tstart, tfinish, 500)
X0 = [0, 0]
U = [24]

sol = solve_ivp(model, (tstart, tfinish), X0, args=(U, params))


t = np.array(sol.t)
i = np.array(sol.y[0])
w = rad2rpm(np.array(sol.y[1]))
V = np.full(len(i), U[0])
T = params["Kt"] * i * 1e3
Pe = V * i
Pm = T * rpm2rad(w) * 1e-3

sols = [
    {"name": "Voltage", "unit": "V", "title": "Input Voltage", "data": V},
    {"name": "Current", "unit": "A", "title": "Motor Current", "data": i},
    {"name": "Speed", "unit": "rpm", "title": "Motor Speed", "data": w},
    {"name": "Torque", "unit": "mNm", "title": "Motor Torue", "data": T},
    {"name": "Power", "unit": "W", "title": "Elecrical Power", "data": Pe},
    {"name": "Power", "unit": "W", "title": "Mechanical Power", "data": Pm},
]


fig, axes = plt.subplots(2, 3, sharex=True)
axes = axes.flatten()

for i in range(len(sols)):
    plot = sols[i]
    ax = axes[i]

    print(
        f"{plot['title']}:\n\tmoy: {plot['data'][-1]} {plot['unit']}\n\tmax: {max(plot['data'])} {plot['unit']}"
    )

    ax.plot(t, plot["data"])
    ax.set_ylabel(f"{plot["name"]}({plot["unit"]})")
    ax.set_xlabel("Time(s)")
    ax.grid(True)

plt.tight_layout()
plt.show()
