#!/usr/bin/env python3
"""
Physics-Informed Neural Network (PINN) for 1D heat equation:
    ∂_t u = α ∂_{xx} u
Loss = PDE residual + boundary conditions + initial condition.
"""

import torch
import torch.nn as nn

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

def pinn_loss(model: nn.Module, alpha: float, n_samples: int = 1024, device: str = "cpu") -> torch.Tensor:
    # Sample interior points and enable autograd on inputs
    x = torch.rand(n_samples, 1, device=device, requires_grad=True)
    t = torch.rand(n_samples, 1, device=device, requires_grad=True)

    u = model(x, t)

    # First-order derivatives
    grads = torch.autograd.grad(
        u, [x, t],
        grad_outputs=torch.ones_like(u),
        create_graph=True
    )
    u_x, u_t = grads

    # Second spatial derivative
    u_xx = torch.autograd.grad(
        u_x, x,
        grad_outputs=torch.ones_like(u_x),
        create_graph=True
    )[0]

    # PDE residual: u_t - α u_xx = 0
    pde_res = u_t - alpha * u_xx

    # Boundary conditions: Dirichlet u(0,t)=0, u(1,t)=0
    t_bc = torch.rand(n_samples, 1, device=device)
    bc_left = model(torch.zeros_like(t_bc), t_bc)
    bc_right = model(torch.ones_like(t_bc), t_bc)

    # Initial condition: Gaussian spike at center, t=0
    x_ic = torch.rand(n_samples, 1, device=device)
    ic_pred = model(x_ic, torch.zeros_like(x_ic))
    ic_target = torch.exp(-100.0 * (x_ic - 0.5) ** 2)

    loss = (
        (pde_res ** 2).mean() +
        (bc_left ** 2).mean() +
        (bc_right ** 2).mean() +
        ((ic_pred - ic_target) ** 2).mean()
    )
    return loss

def train_pinn(alpha: float = 0.1, epochs: int = 2000, lr: float = 1e-3, device: str = "cpu", save_path: str = "pinn_heat.pt"):
    model = PINN().to(device)
    opt = torch.optim.Adam(model.parameters(), lr=lr)

    for epoch in range(1, epochs + 1):
        loss = pinn_loss(model, alpha, device=device)
        opt.zero_grad()
        loss.backward()
        opt.step()

        if epoch % 200 == 0:
            print(f"Epoch {epoch:4d} | loss={loss.item():.6f}")

    torch.save(model.state_dict(), save_path)
    print(f"Saved PINN checkpoint to {save_path}")
    return model

if __name__ == "__main__":
    # Simple run
    train_pinn()