import numpy as np
import matplotlib.pyplot as plt

# Parameters
alpha = 0.1
Nx = 50
dx = 1.0 / (Nx-1)
dt = 0.001
steps = 200

# Build Laplacian
L = np.zeros((Nx, Nx))
for i in range(1, Nx-1):
    L[i,i-1] = 1
    L[i,i]   = -2
    L[i,i+1] = 1
L /= dx**2

# Initial condition: spike in center
u = np.zeros(Nx)
u[Nx//2] = 1.0

traj = [u.copy()]
for _ in range(steps):
    u = u + dt * alpha * (L @ u)
    traj.append(u.copy())

# Plot
plt.plot(np.linspace(0,1,Nx), traj[0], label="t=0")
plt.plot(np.linspace(0,1,Nx), traj[-1], label=f"t={steps*dt}")
plt.legend(); plt.title("Finite Difference Heat Diffusion")
plt.show()