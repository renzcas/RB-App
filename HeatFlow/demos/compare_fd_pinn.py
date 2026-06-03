#!/usr/bin/env python3
"""
Compare finite-difference solution vs PINN prediction at the same time slice.
"""

import numpy as np
import torch
import torch.nn as nn
import matplotlib.pyplot as plt

# --- PINN definition (must match heat_pinn.PINN) ---
class PINN(nn.Module):
    def __init__(self, hidden: int = 64):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(2, hidden), nn.Tanh(),
            nn.Linear(hidden, hidden), nn.Tanh(),
            nn.Linear(hidden, 1)
        )
    def forward(self, x: torch.Tensor, t: torch.Tensor) -> torch.Tensor:
        inp = torch.cat([x, t], dim=1)
        return self.net(inp)

def finite_difference_1d(alpha: float, Nx: int, steps: int, dt: float):
    Lx = 1.0
    dx = Lx / (Nx - 1)
    L = np.zeros((Nx, Nx), dtype=np.float64)
    for i in range(1, Nx - 1):
        L[i, i - 1] = 1.0
        L[i, i]     = -2.0
        L[i, i + 1] = 1.0
    L /= dx ** 2

    u = np.zeros(Nx, dtype=np.float64)
    u[Nx // 2] = 1.0

    traj = [u.copy()]
    for _ in range(steps):
        u = u + dt * alpha * (L @ u)
        u[0] = 0.0
        u[-1] = 0.0
        traj.append(u.copy())
    return np.linspace(0.0, Lx, Nx), traj

def main():
    # FD parameters
    alpha = 0.1
    Nx = 50
    Lx = 1.0
    dx = Lx / (Nx - 1)
    dt = min(0.5 * (dx ** 2) / alpha, 0.001)
    steps = 200

    x_fd, traj_fd = finite_difference_1d(alpha, Nx, steps, dt)

    # Load trained PINN (train first with heat_pinn.py)
    model = PINN()
    try:
        model.load_state_dict(torch.load("pinn_heat.pt", map_location="cpu"))
        print("Loaded PINN checkpoint pinn_heat.pt")
    except FileNotFoundError:
        print("Warning: pinn_heat.pt not found. Using untrained PINN; curves may not match.")

    model.eval()
    with torch.no_grad():
        x_t = torch.linspace(0.0, 1.0, Nx).unsqueeze(1)
        t_final = torch.full_like(x_t, steps * dt)
        u_pinn = model(x_t, t_final).squeeze().cpu().numpy()

    plt.plot(x_fd, traj_fd[-1], label="Finite Difference", lw=2)
    plt.plot(x_fd, u_pinn, label="PINN Prediction", lw=2, linestyle="--")
    plt.legend()
    plt.title(f"Heat equation at t={steps * dt:.4f} (FD vs PINN)")
    plt.xlabel("x")
    plt.ylabel("u(x,t)")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()