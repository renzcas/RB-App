#!/usr/bin/env python3
"""
Side-by-side animation:
Left: 2D heat diffusion via Kronecker-sum Laplacian (explicit Euler).
Right: CNN surrogate applying local transformation each step.
"""

import torch
import torch.nn as nn
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def laplacian_1d(N: int, dx: float, bc: str = "dirichlet", device: str = "cpu") -> torch.Tensor:
    L = torch.zeros((N, N), device=device)
    L += torch.diag(-2.0 * torch.ones(N, device=device))
    L += torch.diag(torch.ones(N - 1, device=device), 1)
    L += torch.diag(torch.ones(N - 1, device=device), -1)
    if bc == "neumann":
        L[0, 0] = -1.0; L[0, 1] = 1.0
        L[-1, -1] = -1.0; L[-1, -2] = 1.0
    return L / (dx ** 2)

class SmallCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(1, 8, kernel_size=3, padding=1),
            nn.Tanh(),
            nn.Conv2d(8, 1, kernel_size=3, padding=1)
        )
    def forward(self, U: torch.Tensor) -> torch.Tensor:
        return self.conv(U.unsqueeze(0).unsqueeze(0)).squeeze(0).squeeze(0)

def main():
    # Grid and physics
    Hx, Hy = 32, 32
    dx = dy = 1.0
    alpha = 0.15
    dt = 0.05
    steps = 100
    device = "cpu"

    # Build 2D Laplacian (Kronecker sum)
    Lx = laplacian_1d(Hx, dx, bc="dirichlet", device=device)
    Ly = laplacian_1d(Hy, dy, bc="dirichlet", device=device)
    Ix = torch.eye(Hx, device=device)
    Iy = torch.eye(Hy, device=device)
    L2D = torch.kron(Iy, Lx) + torch.kron(Ly, Ix)  # (Hy*Hx) x (Hy*Hx)

    # Initial condition: spike
    U = torch.zeros(Hy, Hx, device=device)
    U[Hy // 2, Hx // 2] = 1.0
    U_nn = U.clone()

    # CNN surrogate (untrained demo)
    cnn = SmallCNN().to(device)
    cnn.eval()

    def step_heat(U: torch.Tensor) -> torch.Tensor:
        u_vec = U.reshape(-1)
        u_next = u_vec + dt * alpha * (L2D @ u_vec)
        U_new = u_next.reshape(Hy, Hx)
        # Dirichlet boundaries
        U_new[0, :] = 0.0; U_new[-1, :] = 0.0
        U_new[:, 0] = 0.0; U_new[:, -1] = 0.0
        return U_new

    def step_cnn(U: torch.Tensor) -> torch.Tensor:
        with torch.no_grad():
            return cnn(U)

    # Animation setup
    fig, axes = plt.subplots(1, 2, figsize=(8, 4))
    im1 = axes[0].imshow(U.cpu().numpy(), cmap="inferno", vmin=0, vmax=1)
    axes[0].set_title("Heat diffusion")
    im2 = axes[1].imshow(U_nn.cpu().numpy(), cmap="viridis", vmin=0, vmax=1)
    axes[1].set_title("CNN transformation")
    plt.tight_layout()

    def update(frame: int):
        nonlocal U, U_nn
        U = step_heat(U)
        U_nn = step_cnn(U_nn)
        im1.set_data(U.detach().cpu().numpy())
        im2.set_data(U_nn.detach().cpu().numpy())
        axes[0].set_title(f"Heat diffusion — step {frame}")
        axes[1].set_title(f"CNN transform — step {frame}")
        return im1, im2

    ani = FuncAnimation(fig, update, frames=steps, interval=100, blit=False)
    plt.show()

if __name__ == "__main__":
    main()