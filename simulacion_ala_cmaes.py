import pygame
import numpy as np
from cmaes import CMA
import threading

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulación Aerodinámica con CMA-ES")

# Colores
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
RED = (255, 50, 50)

# Cargar imágenes
plane_img = pygame.image.load("plane.png")
plane_img = pygame.transform.scale(plane_img, (100, 50))
cloud_img = pygame.image.load("nube.png")
cloud_img = pygame.transform.scale(cloud_img, (200, 120))

# Posición inicial del avión
x, y = 100, 300
speed = 5.0

# Parámetros iniciales
initial_params = np.array([10.0, 5.0, 0.0])  # [sustentación, resistencia, ángulo de ataque]
bounds = np.array([[5.0, 20.0], [1.0, 10.0], [-10.0, 10.0]])  # Límites para [sustentación, resistencia, ángulo de ataque]

# Configuración del optimizador CMA-ES con regularización
class RegularizedCMA(CMA):
    def _eigen_decomposition(self):
        try:
            return super()._eigen_decomposition()
        except np.linalg.LinAlgError:
            # Agregar regularización a la matriz de covarianza
            self._C += np.eye(self._dim) * 1e-8
            return super()._eigen_decomposition()

optimizer = RegularizedCMA(mean=initial_params, sigma=0.5, bounds=bounds, population_size=4)

# Generar posiciones iniciales de las nubes
clouds = [[float(np.random.randint(0, WIDTH)), float(np.random.randint(0, HEIGHT))] for _ in range(5)]

# Reloj para controlar la velocidad de actualización
clock = pygame.time.Clock()

# Variables compartidas
best_params = initial_params
target_y = 300.0
running = True

# Función del optimizador CMA-ES ejecutándose en segundo plano
def run_cmaes():
    global best_params, running
    while running:
        solutions = []
        for _ in range(optimizer.population_size):
            try:
                params = optimizer.ask()
                # Asegurarse de que los parámetros estén dentro de los límites
                params = np.clip(params, bounds[:, 0], bounds[:, 1])
                lift, drag, alpha = params
                # Evaluar la aptitud (fitness) de los parámetros actuales
                fitness = -abs((y - target_y) * 0.01 + drag * 0.5)  # Fitness optimizado
                solutions.append((params.astype(float), float(fitness)))
            except np.linalg.LinAlgError:
                # Reiniciar el optimizador en caso de error de descomposición
                optimizer = RegularizedCMA(mean=initial_params, sigma=0.5, bounds=bounds, population_size=4)
                break
        else:
            optimizer.tell(solutions)
            best_params = optimizer.mean  # Obtener la mejor solución actual

# Iniciar hilo para CMA-ES
cma_thread = threading.Thread(target=run_cmaes)
cma_thread.start()

# Pre-cachear rotaciones del avión
cached_rotations = {angle: pygame.transform.rotate(plane_img, angle) for angle in range(-30, 31)}

# Bucle principal de Pygame
while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    lift, drag, alpha = best_params
    y -= lift * 0.05
    y += drag * 0.02
    angle = int(alpha * -3.0)

    y = max(50.0, min(y, HEIGHT - 50.0))
    x = min(WIDTH // 2, x + speed)

    for cloud in clouds:
        cloud[0] -= speed * 0.5
        if cloud[0] < -200.0:
            cloud[0] = float(WIDTH)
            cloud[1] = float(np.random.randint(0, HEIGHT))

    for cloud in clouds:
        screen.blit(cloud_img, cloud)

    rotated_plane = cached_rotations.get(angle, pygame.transform.rotate(plane_img, angle))
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
    clock.tick(60)

# Finalizar el hilo del optimizador
running = False
cma_thread.join()
pygame.quit()
