import pygame
import math
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

pygame.init()

WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bug Under Bridge – Tiny Transformer Agent")

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

# Tiny GPT-2 for demo
tokenizer = AutoTokenizer.from_pretrained("sshleifer/tiny-gpt2")
model = AutoModelForCausalLM.from_pretrained("sshleifer/tiny-gpt2")
model.eval()

ACTIONS = ["escape_left", "escape_right", "hide", "wait"]

def generate_bug_action(hx, hy, bx, by):
    prompt = (
        f"Bug state:\n"
        f"hand_x: {hx / WIDTH:.2f}\n"
        f"hand_y: {hy / HEIGHT:.2f}\n"
        f"bug_x: {bx / WIDTH:.2f}\n"
        f"bug_y: {by / HEIGHT:.2f}\n\n"
        f"Next bug action (escape_left, escape_right, hide, wait): "
    )
    inputs = tokenizer(prompt, return_tensors="pt")
    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_length=inputs["input_ids"].shape[1] + 4,
            do_sample=True,
            top_k=20,
            top_p=0.9,
        )
    text = tokenizer.decode(output[0])
    for a in ACTIONS:
        if a in text:
            return a
    return "wait"

def step_bug(bx, by, hx, hy):
    action = generate_bug_action(hx, hy, bx, by)

    if action == "escape_left":
        bx -= bug_speed
    elif action == "escape_right":
        bx += bug_speed
    elif action == "hide":
        if by > bridge_y + bridge_height / 2:
            by -= bug_speed
        else:
            by += bug_speed

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
        print("You tagged the transformer bug!")
        running = False

    screen.fill(WHITE)
    pygame.draw.rect(screen, BRIDGE_COLOR, (0, bridge_y, WIDTH, bridge_height))
    pygame.draw.circle(screen, BUG_COLOR, (int(bug_x), int(bug_y)), bug_radius)
    pygame.draw.circle(screen, HAND_COLOR, (int(hand_x), int(hand_y)), hand_radius)
    txt = font.render(f"Action: {last_action}", True, (0, 0, 0))
    screen.blit(txt, (10, 10))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()