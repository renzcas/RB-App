# bug_base.py — Pure survival bug with bridge


import pygame
import math

pygame.init()

WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bug Under Bridge – Base Agent")

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

running = True

def bug_ai(bx, by, hx, hy):
    dx = bx - hx
    dy = by - hy

    # If hand is above bug and within vertical threat range → move toward bridge (hide)
    if hy < by and abs(dy) < 200:
        # Move toward bridge zone
        if bridge_y <= by <= bridge_y + bridge_height:
            pass  # already under bridge
        else:
            if by > bridge_y:
                by -= bug_speed
            else:
                by += bug_speed

    # Horizontal escape logic: if hand is close horizontally, run away
    if abs(dx) < 150:
        if hx < bx:
            bx += bug_speed  # hand left → bug runs right
        else:
            bx -= bug_speed  # hand right → bug runs left

    bx = max(bug_radius, min(WIDTH - bug_radius, bx))
    by = max(bug_radius, min(HEIGHT - bug_radius, by))
    return bx, by

def check_tag(bx, by, hx, hy):
    dist = math.hypot(bx - hx, by - hy)
    return dist < (bug_radius + hand_radius)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mx, my = pygame.mouse.get_pos()
    hand_x += (mx - hand_x) * 0.2
    hand_y += (my - hand_y) * 0.2

    bug_x, bug_y = bug_ai(bug_x, bug_y, hand_x, hand_y)

    if check_tag(bug_x, bug_y, hand_x, hand_y):
        print("You tagged the bug!")
        running = False

    screen.fill(WHITE)
    pygame.draw.rect(screen, BRIDGE_COLOR, (0, bridge_y, WIDTH, bridge_height))
    pygame.draw.circle(screen, BUG_COLOR, (int(bug_x), int(bug_y)), bug_radius)
    pygame.draw.circle(screen, HAND_COLOR, (int(hand_x), int(hand_y)), hand_radius)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()