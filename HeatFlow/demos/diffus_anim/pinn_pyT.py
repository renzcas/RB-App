import torch
import torch.nn as nn

# Neural net: maps (x,t) → u(x,t)
class PINN(nn.Module):
    def __init__(self, hidden=64):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(2, hidden), nn.Tanh(),
            nn.Linear(hidden, hidden), nn.Tanh(),
            nn.Linear(hidden, 1)
        )
    def forward(self, x, t):
        inp = torch.cat([x, t], dim=1)
        return self.net(inp)

# Physics-informed loss
def pinn_loss(model, alpha, n_samples=1000):
    x = torch.rand(n_samples,1)
    t = torch.rand(n_samples,1)
    u = model(x,t)

    # Autograd for PDE residual
    grads = torch.autograd.grad(u, [x,t], grad_outputs=torch.ones_like(u),
                                create_graph=True)
    u_x, u_t = grads
    u_xx = torch.autograd.grad(u_x, x, grad_outputs=torch.ones_like(u_x),
                               create_graph=True)[0]

    # PDE residual: u_t - alpha u_xx = 0
    pde_res = u_t - alpha * u_xx

    # Boundary conditions: u(0,t)=0, u(1,t)=0
    bc_left = model(torch.zeros_like(t), t)
    bc_right = model(torch.ones_like(t), t)

    # Initial condition: Gaussian spike at center
    ic = model(x, torch.zeros_like(x))
    ic_target = torch.exp(-100*(x-0.5)**2)

    loss = (pde_res**2).mean() + (bc_left**2).mean() + (bc_right**2).mean() + ((ic-ic_target)**2).mean()
    return loss

# Train PINN
model = PINN()
opt = torch.optim.Adam(model.parameters(), lr=1e-3)

for epoch in range(2000):
    loss = pinn_loss(model, alpha)
    opt.zero_grad(); loss.backward(); opt.step()
    if epoch % 200 == 0:
        print(f"Epoch {epoch}: loss={loss.item():.6f}")