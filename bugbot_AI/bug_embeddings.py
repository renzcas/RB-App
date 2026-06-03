#bug_embeddings.py — Bug uses fear/safety embeddings to choose actions
import pygame
import numpy as np
import math

pygame.init()

WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.setCaption("Bug Under Bridge – Embedding Agent")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BUG_COLOR = (200, 50, 50)
HAND_COLOR = (50, 50, 200)
BRIDGE_COLOR = (100, 100, 100)

bug_x = WIDTH // 2
bug_y = HEIGHT // 2
bug_speed = 3
bug_radius = 12

hand_x = WIDTH // 2
hand_y = 50
hand_radius = 20

bridge_y = HEIGHT // 2
bridge_height = 40

# Tiny semantic space
embeddings = {
    "threat": np.array([1.0, 0.2]),
    "safety": np.array([-1.0, -0.2]),
    "hide": np.array([0.0, -1.0]),
    "escape_left": np.array([-1.0, 1.0]),
    "escape_right": np.array([1.0, 1.0]),
}

def encode_state(hx, hy, bx, by):
    # Normalize positions to [0,1]
    nx_h = hx / WIDTH
    nx_b = bx / WIDTH
    ny_h = hy / HEIGHT
    ny_b = by / HEIGHT

    horiz_threat = 1.0 - abs(nx_h - nx_b)
    vert_threat = 1.0 - abs(ny_h - ny_b)
    threat_level = max(horiz_threat, vert_threat)

    return np.array([threat_level, 0.5])

def choose_action(state_vec):
    best = None
    best_score = -999
    for action, vec in embeddings.items():
        num = np.dot(state_vec, vec)
        den = np.linalg.norm(state_vec) * np.linalg.norm(vec) + 1e-8
        score = num / den
        if score > best_score:
            best_score = score
            best = action
    return best

def step_bug(bx, by, hx, hy):
    state = encode_state(hx, hy, bx, by)
    action = choose_action(state)

    # Interpret semantic action
    if action == "escape_left":
        bx -= bug_speed
    elif action == "escape_right":
        bx += bug_speed
    elif action == "hide":
        # Move toward bridge vertically
        if by > bridge_y + bridge_height / 2:
            by -= bug_speed
        else:
            by += bug_speed

    # Boundaries
    bx = max(bug_radius, min(WIDTH - bug_radius, bx))
    by = max(bug_radius, min(HEIGHT - bug_radius, by))
    return bx, by, action

def check_tag(bx, by, hx, hy):
    return math.hypot(bx - hx, by - hy) < (bug_radius + hand_radius)

font = pygame.font.SysFont(None, 24)
last_action = "none"
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mx, my = pygame.mouse.get_pos()
    hand_x += (mx - hand_x) * 0.2
    hand_y += (my - hand_y) * 0.2

    bug_x, bug_y, last_action = step_bug(bug_x, bug_y, hand_x, hand_y)

    if check_tag(bug_x, bug_y, hand_x, hand_y):
        print("You tagged the semantic bug!")
        running = False

    screen.fill(WHITE)
    pygame.draw.rect(screen, BRIDGE_COLOR, (0, bridge_y, WIDTH, bridge_height))
    pygame.draw.circle(screen, BUG_COLOR, (int(bug_x), int(bug_y)), bug_radius)
    pygame.draw.circle(screen, HAND_COLOR, (int(hand_x), int(hand_y)), hand_radius)

    text = font.render(f"Action: {last_action}", True, (0, 0, 0))
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()