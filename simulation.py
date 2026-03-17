import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt


def model(t, X, U, params):
    R = params["R"]
    L = params["L"]
    b = params["b"]
    J = params["J"]
    Kv = params["Kv"]
    Kt = params["Kt"]
    Tl = params["Tl"]

    V = U[0]

    i = X[0]
    w = X[1]

    di = (1 / L) * V - (R / L) * i - (Kv / L) * w
    dw = (Kt / J) * i - (b / J) * w - Tl

    return [di, dw]


params = {
    "R": 2.68,
    "L": 0.514e-3,
    "b": 1.11e-4,
    "J": 21.2e-7,
    "Kv": 223 * (2 * np.pi / 60),
    "Kt": 42.9e-3,
    "Tl": 20.0e-3,
}

tstart = 0
tfinish = 1
tspan = np.linspace(tstart, tfinish, 500)
X0 = [0, 0]
U = [24]

sol = solve_ivp(model, (tstart, tfinish), X0, args=(U, params))


t = np.array(sol.t)
i = np.array(sol.y[0])
w = np.array(sol.y[1])
V = np.full(len(i), U[0])
T = params["Kt"] * i * 1e3
Pt = V * i
Pm = T * w

w = w * (60 / (2 * np.pi))

fig, axes = plt.subplots(2, 3, sharex=True)
axes = axes.flatten()

axes[0].plot(t, V)
axes[0].set_ylabel("Voltage(V)")
axes[0].set_title("Input Voltage")

axes[1].plot(t, i)
axes[1].set_ylabel("Current(A)")
axes[1].set_title("Motor Current")

axes[2].plot(t, w)
axes[2].set_ylabel("Speed(rpm)")
axes[2].set_title("Motor Speed")

axes[3].plot(t, T)
axes[3].set_ylabel("Torque(mNm)")
axes[3].set_title("Motor Torque")

axes[4].plot(t, Pt)
axes[4].set_ylabel("Power(W)")
axes[4].set_title("Input Power")

axes[5].plot(t, Pm)
axes[5].set_ylabel("Power(W)")
axes[5].set_title("Mechanical Power")

for ax in axes:
    ax.grid(True)

plt.xlabel("Time(s)")
plt.tight_layout()
plt.show()
