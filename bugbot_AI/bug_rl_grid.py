#bug_rl_grid.py — Simple RL survival in a gridworld
#This one is not graphical; it’s a tiny RL core: the bug learns to avoid the top row (hand) and survive longer.
import numpy as np
import random

GRID_W, GRID_H = 5, 5
ACTIONS = ["left", "right", "up", "down"]

def step(state, action):
    x, y = state
    if action == "left":
        x = max(0, x - 1)
    elif action == "right":
        x = min(GRID_W - 1, x + 1)
    elif action == "up":
        y = max(0, y - 1)
    elif action == "down":
        y = min(GRID_H - 1, y + 1)

    reward = -0.01
    done = False

    # "Hand" at top row: y == 0 is dangerous
    if y == 0:
        reward = -1.0
        done = True

    return (x, y), reward, done

Q = np.zeros((GRID_W, GRID_H, len(ACTIONS)))
alpha = 0.1
gamma = 0.99
epsilon = 0.2

def choose_action(state):
    if random.random() < epsilon:
        return random.randrange(len(ACTIONS))
    x, y = state
    return np.argmax(Q[x, y])

episodes = 2000

for ep in range(episodes):
    state = (GRID_W // 2, GRID_H - 1)
    done = False
    steps = 0
    while not done and steps < 50:
        a_idx = choose_action(state)
        action = ACTIONS[a_idx]
        next_state, reward, done = step(state, action)

        x, y = state
        nx, ny = next_state
        best_next = np.max(Q[nx, ny])
        Q[x, y, a_idx] += alpha * (reward + gamma * best_next - Q[x, y, a_idx])

        state = next_state
        steps += 1

    if (ep + 1) % 200 == 0:
        print(f"Episode {ep+1}, survived {steps} steps")

print("Learned Q-values slice for middle row (y=2):")
print(Q[:, 2, :])