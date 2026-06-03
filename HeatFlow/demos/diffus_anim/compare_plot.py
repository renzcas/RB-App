# Sample PINN at final time
Nx = 50
x_torch = torch.linspace(0,1,Nx).unsqueeze(1)
t_final = torch.full_like(x_torch, steps*dt)
with torch.no_grad():
    u_pinn = model(x_torch, t_final).squeeze().numpy()

# Plot comparison
plt.plot(np.linspace(0,1,Nx), traj[-1], label="Finite Difference", lw=2)
plt.plot(np.linspace(0,1,Nx), u_pinn, label="PINN Prediction", lw=2, linestyle="--")
plt.legend()
plt.title(f"Heat Equation at t={steps*dt:.3f}")
plt.xlabel("x"); plt.ylabel("u(x,t)")
plt.show()