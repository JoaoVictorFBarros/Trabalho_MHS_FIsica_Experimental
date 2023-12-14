import pygame
import math

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

num_pendulums = int(input("Digite a quantidade de pêndulos: "))
length_difference = float(input("Digite a diferença de comprimento entre os pêndulos: "))
initial_angle = float(input("Digite o ângulo inicial em graus: "))

pendulums = []
for i in range(num_pendulums):
    pendulums.append({
        'length': 100 + i * length_difference,
        'angle': math.radians(initial_angle),
        'angular_velocity': 0.0,
        'angular_acceleration': 0.0,
        'color': ((255 - i * 20) % 256, (i * 20) % 256, 0),
        'x': 0,
        'y': 0
    })

gravity = 9.8

base_width = 20
base_height = 10
base_x = 600 - base_width // 2
base_y = 50
base_velocity = 0.0
angular_acceleration_base = 0.0

width, height = 1200, 900
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Simulação de Pêndulos")

font = pygame.font.Font(None, 26)
clock = pygame.time.Clock()

def update_pendulums(dt):
    global angular_acceleration_base

    angular_acceleration_base = -100 * gravity / pendulums[0]['length'] * math.sin(pendulums[0]['angle'])

    for pendulum in pendulums:

        pendulum['angular_acceleration'] = -100 * gravity / pendulum['length'] * math.sin(pendulum['angle'])
        pendulum['angular_velocity'] += pendulum['angular_acceleration'] * dt
        pendulum['angle'] += pendulum['angular_velocity'] * dt

def draw_pendulums():
    global base_x, base_y

    pygame.draw.rect(screen, WHITE, (base_x, base_y, base_width, base_height))

    for i, pendulum in enumerate(pendulums):
        pendulum['x'] = base_x + base_width // 2 + int(pendulum['length'] * math.sin(pendulum['angle']))
        pendulum['y'] = base_y + int(pendulum['length'] * math.cos(pendulum['angle']))
        pygame.draw.line(screen, pendulum['color'], (base_x + base_width // 2, base_y), (pendulum['x'], pendulum['y']), 2)
        pygame.draw.circle(screen, pendulum['color'], (pendulum['x'], pendulum['y']), 10)

def format_time(milliseconds):
    seconds = milliseconds // 1000
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes:02}:{seconds:02}"

def main():
    global pendulums, base_x, base_y, base_velocity

    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        dt = 1 / 60

        update_pendulums(dt)

        screen.fill(BLACK)
        draw_pendulums()


        for i, pendulum in enumerate(pendulums):
            period = 2 * math.pi * math.sqrt(pendulum['length'] / (100 * gravity))
            text = font.render(f"Pêndulo {i + 1}: Período {round(period, 3)} Segs", True, WHITE)
            screen.blit(text, (10, 900 - (i + 1) * 30))
        

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
