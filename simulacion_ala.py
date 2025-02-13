import pygame
import numpy as np

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulación Aerodinámica con Límites y Nubes")

WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
RED = (255, 50, 50)

plane_img = pygame.image.load("plane.png")
plane_img = pygame.transform.scale(plane_img, (100, 50))
cloud_img = pygame.image.load("nube.png")
cloud_img = pygame.transform.scale(cloud_img, (200, 120))

x, y = 100, 300
speed = 5
angle = 0

alpha = 5
lift = 10
drag = 5

cov_matrix = np.array([[1.0, 0.7, 0.5], [0.7, 1.0, 0.3], [0.5, 0.3, 1.0]])

def update_aerodynamics():
    global lift, drag, alpha
    delta = np.random.multivariate_normal([0, 0, 0], cov_matrix)
    lift = max(5, lift + delta[0])
    drag = max(1, drag + delta[1])
    alpha = max(-10, min(10, alpha + delta[2]))

clouds = [[np.random.randint(0, WIDTH), np.random.randint(0, HEIGHT)] for _ in range(5)]

running = True
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    update_aerodynamics()

    # Movimiento vertical
    y -= lift * 0.05
    y += drag * 0.02
    angle = alpha * -3

    # Limitar avión dentro de la ventana
    if y < 50:
        y = 50
    if y > HEIGHT - 50:
        y = HEIGHT - 50

    # Limitar posición horizontal al centro de la pantalla
    x = min(WIDTH // 2, x + speed)

    # Mover nubes simulando avance
    for cloud in clouds:
        cloud[0] -= speed * 0.5
        if cloud[0] < -200:
            cloud[0] = WIDTH
            cloud[1] = np.random.randint(0, HEIGHT)

    for cloud in clouds:
        screen.blit(cloud_img, cloud)

    rotated_plane = pygame.transform.rotate(plane_img, angle)
    rect = rotated_plane.get_rect(center=(x, y))
    screen.blit(rotated_plane, rect.topleft)

    font = pygame.font.Font(None, 24)
    lift_text = font.render(f"Sustentación: {lift:.2f}", True, BLUE)
    drag_text = font.render(f"Resistencia: {drag:.2f}", True, RED)
    alpha_text = font.render(f"Ángulo de ataque: {alpha:.2f}", True, (0, 0, 0))

    screen.blit(lift_text, (10, 10))
    screen.blit(drag_text, (10, 40))
    screen.blit(alpha_text, (10, 70))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
