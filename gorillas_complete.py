import pygame
import math

# Initialiseer pygame
pygame.init()

# Scherm instellingen
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Gorillas')

# Kleuren
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255,0,0)

# Gorillas instellingen
gorilla_size = 30
gorilla1_pos = (100, height - gorilla_size)
gorilla2_pos = (width - 100, height - gorilla_size)


# Functie om gorillas te tekenen
def draw_gorillas():
    pygame.draw.rect(screen, BLACK, (*gorilla1_pos, gorilla_size, gorilla_size))
    pygame.draw.rect(screen, BLACK, (*gorilla2_pos, gorilla_size, gorilla_size))


# Functie om een banaan te gooien
def throw_banana(start_pos, angle, speed, target_gorilla_pos, flip_direction=False):
    angle = math.radians(angle)
    banana_pos = list(start_pos)
    banana_radius = 5
    gravity = 0.5
    direction = -1 if flip_direction else 1
    velocity_x = direction * speed * math.cos(angle)
    velocity_y = -speed * math.sin(angle)

    while banana_pos[0] > 0 and banana_pos[0] < width and banana_pos[1] < height:
        banana_pos[0] += velocity_x
        banana_pos[1] += velocity_y
        velocity_y += gravity

        # Achtergrond en gorillas opnieuw tekenen
        screen.fill(WHITE)
        draw_gorillas()

        # Banaan tekenen
        pygame.draw.circle(screen, RED, (int(banana_pos[0]), int(banana_pos[1])), banana_radius)

        # Update het scherm
        pygame.display.flip()
        pygame.time.delay(30)

        # Controleer op botsingen
        if check_collision(banana_pos, target_gorilla_pos, gorilla_size):
            print("Gorilla geraakt!")
            return True
    return False


# Functie om botsingen te controleren
def check_collision(banana_pos, gorilla_pos, gorilla_size):
    if (gorilla_pos[0] <= banana_pos[0] <= gorilla_pos[0] + gorilla_size and
            gorilla_pos[1] <= banana_pos[1] <= gorilla_pos[1] + gorilla_size):
        return True
    return False


# Functie om de hoek en kracht van de speler te krijgen
def get_player_input(player):
    font = pygame.font.Font(None, 36)
    input_box = pygame.Rect(10, 10, 200, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None, None
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill(WHITE)
        draw_gorillas()
        instruction_text = font.render(f'Speler {player} - Voer hoek en kracht in (hoek,snelheid):', True,
                                       BLACK)
        screen.blit(instruction_text, (10, 50))
        txt_surface = font.render(text, True, color)
        width_surface = max(200, txt_surface.get_width() + 10)
        input_box.w = width_surface
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)
        pygame.display.flip()

    try:
        angle, speed = map(float, text.split(','))
        return angle, speed
    except ValueError:
        return None, None


# Hoofdlus
running = True
player_turn = 1
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Achtergrond
    screen.fill(WHITE)

    # Gorillas tekenen
    draw_gorillas()

    # Update het scherm
    pygame.display.flip()

    # Vraag invoer van de huidige speler
    angle, speed = get_player_input(player_turn)

    if angle is not None and speed is not None:
        # Gooi de banaan
        if player_turn == 1:
            start_pos = gorilla1_pos
            target_pos = gorilla2_pos
            hit = throw_banana(start_pos, angle, speed, target_pos)
        else:
            start_pos = gorilla2_pos
            target_pos = gorilla1_pos
            hit = throw_banana(start_pos, angle, speed, target_pos, flip_direction=True)

        if hit:
            print(f"Speler {player_turn} wint!")
            running = False

        # Wissel van beurt
        player_turn = 1 if player_turn == 2 else 2

# Sluit pygame af
pygame.quit()
