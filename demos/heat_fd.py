#!/usr/bin/env python3
"""
Finite-difference solver for the 1D heat equation:
    ∂_t u = α ∂_{xx} u
Dirichlet boundaries, spike initial condition, explicit Euler time stepping.
"""

import numpy as np
import matplotlib.pyplot as plt

def build_laplacian_1d(N: int, dx: float) -> np.ndarray:
    L = np.zeros((N, N), dtype=np.float64)
    for i in range(1, N - 1):
        L[i, i - 1] = 1.0
        L[i, i]     = -2.0
        L[i, i + 1] = 1.0
    return L / (dx ** 2)

def main():
    # Parameters
    alpha = 0.1
    Nx = 50
    Lx = 1.0
    dx = Lx / (Nx - 1)

    # Explicit Euler stability (rough guide): dt <= dx^2 / (2α)
    dt = min(0.5 * (dx ** 2) / alpha, 0.001)
    steps = 200

    # Laplacian and initial condition
    L = build_laplacian_1d(Nx, dx)
    u = np.zeros(Nx, dtype=np.float64)
    u[Nx // 2] = 1.0  # spike

    traj = [u.copy()]
    for _ in range(steps):
        u = u + dt * alpha * (L @ u)
        # Dirichlet boundaries
        u[0] = 0.0
        u[-1] = 0.0
        traj.append(u.copy())

    x = np.linspace(0.0, Lx, Nx)
    plt.plot(x, traj[0], label="t=0")
    plt.plot(x, traj[-1], label=f"t={steps * dt:.4f}")
    plt.legend()
    plt.title("1D heat diffusion (finite difference)")
    plt.xlabel("x")
    plt.ylabel("u(x,t)")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()