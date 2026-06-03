import numpy as np

# --- Subnet Operations ---
def subnet_operations(a: set, b: set) -> dict:
    """Return union, intersection, and differences of two subnets."""
    return {
        "union": a.union(b),
        "intersection": a.intersection(b),
        "difference_a_b": a.difference(b),
        "difference_b_a": b.difference(a),
    }

# --- Replay Transform ---
def filter_events(events, actor="all"):
    """Filter replay events by actor."""
    if actor == "all":
        return events
    return [e for e in events if e["actor"] == actor]

# --- Phase Space Forces ---
def attractor_force(pos, attractors):
    """Compute force vectors pulling agents toward attractors."""
    f = np.zeros_like(pos)
    for a in attractors.values():
        delta = a["center"] - pos
        dist = np.linalg.norm(delta, axis=1, keepdims=True) + 1e-6
        f += a["k"] * (delta / dist)
    return f

def hamiltonian_energy(v):
    """Semantic energy ~ 0.5 * ||v||^2."""
    return 0.5 * np.sum(v**2, axis=1)

def lagrangian_action(force_mag, dt):
    """Discrete action ~ sum(|F|) * dt."""
    return force_mag * dt

# --- Integrator ---
def simulate_agents(num_agents, steps, dt, noise_amp, attractors, rng=None):
    """Simulate agent trajectories under attractor forces."""
    if rng is None:
        rng = np.random.default_rng(42)

    positions = rng.uniform(-1.0, 1.0, size=(num_agents, 2))
    velocities = np.zeros_like(positions)
    traj = [positions.copy()]
    energy_series, action_series = [], []

    for _ in range(steps):
        F = attractor_force(positions, attractors)
        noise = noise_amp * rng.normal(0, 1, size=positions.shape)
        velocities = velocities + (F * dt)
        positions = positions + velocities * dt + noise
        traj.append(positions.copy())

        energy_series.append(hamiltonian_energy(velocities))
        action_series.append(np.linalg.norm(F, axis=1) * dt)

    return traj, np.array(energy_series), np.array(action_series)