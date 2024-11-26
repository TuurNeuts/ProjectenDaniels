import serial
import pygame
import random
import threading

# Initialiseer Pygame
pygame.init()

# Instellingen voor het spel
WIDTH, HEIGHT = 800, 600
FPS = 30
MOLE_SIZE = 100
MOLE_TIME = 1000  # Milliseconds

# Kleuren
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Initialiseer het scherm
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Whack the Mole")

# Mole locaties
mole_positions = [
    (WIDTH // 4 - MOLE_SIZE // 2, HEIGHT // 2 - MOLE_SIZE // 2),
    (WIDTH // 2 - MOLE_SIZE // 2, HEIGHT // 2 - MOLE_SIZE // 2),
    (3 * WIDTH // 4 - MOLE_SIZE // 2, HEIGHT // 2 - MOLE_SIZE // 2)
]

# Actieve mol positie
active_mole_index = random.randint(0, 2)
last_mole_time = pygame.time.get_ticks()

# Seriële poort instellen (aanpassen naar de juiste poort)
try:
    ser = serial.Serial('COM46', 115200, timeout=1)  # Pas 'COM3' aan naar de juiste poort voor Windows
except serial.SerialException as e:
    print(f"Fout bij het openen van de seriële poort: {e}")
    ser = None

# Variabele voor het bijhouden van punten
score = 0

# Functie om de seriële poort in te lezen
def read_serial():
    global active_mole_index, score
    if ser is not None:
        while True:
            if ser.in_waiting > 0:
                data = ser.readline().decode('utf-8').strip()
                if data == 'links' and active_mole_index == 0:
                    score += 1
                    print("Raak! Score:", score)
                elif data == 'B' and active_mole_index == 1:
                    score += 1
                    print("Raak! Score:", score)
                elif data == 'rechts' and active_mole_index == 2:
                    score += 1
                    print("Raak! Score:", score)

# Start een thread om de seriële poort te lezen
if ser is not None:
    thread = threading.Thread(target=read_serial)
    thread.daemon = True
    thread.start()

# Hoofdlus van het spel
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update het spel
    current_time = pygame.time.get_ticks()
    if current_time - last_mole_time > MOLE_TIME:
        active_mole_index = random.randint(0, 2)
        last_mole_time = current_time

    # Teken alles
    screen.fill(WHITE)
    for i, pos in enumerate(mole_positions):
        color = RED if i == active_mole_index else WHITE
        pygame.draw.rect(screen, color, (*pos, MOLE_SIZE, MOLE_SIZE))

    pygame.display.flip()
    clock.tick(FPS)

# Sluit de seriële poort en Pygame
if ser is not None:
    ser.close()
pygame.quit()
