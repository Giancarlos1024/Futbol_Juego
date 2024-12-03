import pygame
import sys
import random
import math
import Dimensiones
from Dimensiones import draw_button
from Dimensiones import is_button_clicked
from Dimensiones import start_screen
from Dimensiones import second_screen
from Dimensiones import third_screen
from Dimensiones import tutorial_screen

# Inicializamos pygame
pygame.init()
# Crear la pantalla
screen = pygame.display.set_mode((Dimensiones.SCREEN_WIDTH, Dimensiones.SCREEN_HEIGHT))
pygame.display.set_caption("Juego de Fútbol")
# Inicializa el mixer de Pygame
pygame.mixer.init()
# Cargar el sonido del gol
gol_sound = pygame.mixer.Sound('videos/gol.mp3')

# Lista de canciones para cada nivel
level_music = {
    1: 'videos/nivel1.mp3',  # Música para el nivel 1
    2: 'videos/nivel2.mp3',  # Música para el nivel 2
    3: 'videos/nivel3.mp3'   # Música para el nivel 3
}
# Imágenes de los porteros enemigos
goalkeeper_enemy_images = {
    1: pygame.transform.scale(pygame.image.load('img/jugadores/Portero_barcelona.png'), (Dimensiones.goalkeeper_size, Dimensiones.goalkeeper_size)),
    2: pygame.transform.scale(pygame.image.load('img/jugadores/Portero_bayern.png'), (Dimensiones.goalkeeper_size, Dimensiones.goalkeeper_size)),
    3: pygame.transform.scale(pygame.image.load('img/jugadores/portero_juvents.png'), (Dimensiones.goalkeeper_size, Dimensiones.goalkeeper_size))
}
current_goalkeeper_enemy_image = goalkeeper_enemy_images[1]
def play_level_music(level):
    # Cargar la música correspondiente al nivel actual
    pygame.mixer.music.load(level_music[level])  
    pygame.mixer.music.play(-1, 0.0)  # Reproducir música en bucle
# Cargar la fuente personalizada
font_path = 'fonts/retropix.ttf'  # Ruta a tu archivo de fuente
font_size_large = 25  # Tamaño de la fuente grande
font_size_medium = 25  # Tamaño de la fuente mediana
custom_font_large = pygame.font.Font(font_path, font_size_large)
custom_font_medium = pygame.font.Font(font_path, font_size_medium)
# Jugador
player_size = 40
player_x = 50  # Posición inicial del jugador
player_y = Dimensiones.SCREEN_HEIGHT // 2
player_speed = 5
player_name = "Álvaro"  # Nombre del jugador
# Pelota
# ball_size = 20 // EN EL ARCHIVO Dimensiones.py  se usa
ball_x = Dimensiones.SCREEN_WIDTH // 2
ball_y = Dimensiones.SCREEN_HEIGHT // 2
ball_speed_x = 0
ball_speed_y = 0
ball_moving = False  # La pelota está en movimiento o no
ball_owned = False   # El jugador tiene la pelota
# Enemigos
enemies = []
# Imágenes de los equipos enemigos
enemy_images = {
    1: pygame.transform.scale(pygame.image.load('img/jugadores/barcelona.png'), (Dimensiones.enemy_size, Dimensiones.enemy_size)),
    2: pygame.transform.scale(pygame.image.load('img/jugadores/bayern.png'), (Dimensiones.enemy_size, Dimensiones.enemy_size)),
    3: pygame.transform.scale(pygame.image.load('img/jugadores/juvents.png'), (Dimensiones.enemy_size, Dimensiones.enemy_size))
}
# Crear enemigos en posiciones aleatorias
def create_enemies(num):
    enemies = []
    for i in range(num):
        enemy_x = random.randint(200, Dimensiones.SCREEN_WIDTH - Dimensiones.enemy_size)
        enemy_y = random.randint(0, Dimensiones.SCREEN_HEIGHT - Dimensiones.enemy_size)
        enemies.append([enemy_x, enemy_y])
    return enemies
enemies = create_enemies(Dimensiones.num_enemies)
# Área de gol (meta) en la parte derecha de la pantalla
goal_area_right = pygame.Rect(Dimensiones.SCREEN_WIDTH - 50, Dimensiones.SCREEN_HEIGHT // 2 - 100, 50, 200)
goal_area_left = pygame.Rect(0, Dimensiones.SCREEN_HEIGHT // 2 - 100, 50, 200)
# Compañero en el arco
partner_goalkeeper_x = Dimensiones.SCREEN_WIDTH - 790  # Posición del compañero
partner_goalkeeper_y = Dimensiones.SCREEN_HEIGHT // 2 - Dimensiones.goalkeeper_size // 2
partner_name = "Martín"  # Nombre del compañero
# Niveles
level = 1
max_level = 3
goals_player = 0
goals_enemy = 0

# Modificar los goles necesarios para pasar al siguiente nivel según el nivel actual
def set_goals_to_win(level):
    if level == 1:
        return 3  # Goles necesarios para pasar al nivel 2
    elif level == 2:
        return 4  # Goles necesarios para pasar al nivel 3
    elif level == 3:
        return 5  # Goles necesarios para ganar el juego

goals_to_win = set_goals_to_win(level)
# Tiempo por nivel
time_limit = 80  # 60 segundos por nivel
start_time = pygame.time.get_ticks()  # Guardar el tiempo de inicio
# Puntaje total
total_score = 0
# Función para reiniciar los goles al pasar al siguiente nivel
def reset_goals():
    global goals_player, goals_enemy
    goals_player = 0
    goals_enemy = 0
# Función para mover al jugador
def move_player(keys, x, y, speed):
    if keys[pygame.K_LEFT]:
        x -= speed
    if keys[pygame.K_RIGHT]:
        x += speed
    if keys[pygame.K_UP]:
        y -= speed
    if keys[pygame.K_DOWN]:
        y += speed
    # Limitar movimiento dentro de la pantalla
    x = max(0, min(Dimensiones.SCREEN_WIDTH - player_size, x))
    y = max(0, min(Dimensiones.SCREEN_HEIGHT - player_size, y))
    return x, y
    
# Función para mover enemigos hacia el jugador
def move_enemies(player_x, player_y, enemies, speed):
    for enemy in enemies:
        direction_x = player_x - enemy[0]
        direction_y = player_y - enemy[1]
        distance = math.sqrt(direction_x ** 2 + direction_y ** 2)
        if distance > 0:
            enemy[0] += (direction_x / distance) * speed
            enemy[1] += (direction_y / distance) * speed
    avoid_enemy_collisions(enemies)
# Función para evitar colisiones entre enemigos
def avoid_enemy_collisions(enemies, min_distance=50):
    for i in range(len(enemies)):
        for j in range(i + 1, len(enemies)):
            dx = enemies[j][0] - enemies[i][0]
            dy = enemies[j][1] - enemies[i][1]
            distance = math.sqrt(dx**2 + dy**2)
            if distance < min_distance:
                # Separar los enemigos
                angle = math.atan2(dy, dx)
                move_dist = (min_distance - distance) / 2
                enemies[i][0] -= move_dist * math.cos(angle)
                enemies[i][1] -= move_dist * math.sin(angle)
                enemies[j][0] += move_dist * math.cos(angle)
                enemies[j][1] += move_dist * math.sin(angle)
selected_local = None  
selected_visitante = "Visitante" 
if selected_local == "Local":
    # Asignar el jugador local como amigo, el visitante será el enemigo
    player_image = pygame.transform.scale(pygame.image.load('img/jugadores/amigo_local.png'), (player_size, player_size))
    enemy_image = pygame.transform.scale(pygame.image.load('img/jugadores/enemigo_local.png'), (Dimensiones.enemy_size, Dimensiones.enemy_size))
elif selected_visitante == "Visitante":
    # Asignar el jugador visitante como enemigo, el local será el amigo
    player_image = pygame.transform.scale(pygame.image.load('img/jugadores/amigo_visitante.png'), (player_size, player_size))
    enemy_image = pygame.transform.scale(pygame.image.load('img/jugadores/enemigo_local.png'), (Dimensiones.enemy_size, Dimensiones.enemy_size))

def presentation_screen(level):
    running = True
    font = pygame.font.SysFont(None, 48)
    message = f"Nivel {level} - ¡A JUGAR!"
    if level == 1:
        background_img = pygame.image.load('img/campos/Ambito1.png')
    elif level == 2:
        background_img = pygame.image.load('img/campos/Ambito2.png')
    else:
        background_img = pygame.image.load('img/campos/Ambito3.png')
    
    background_img = pygame.transform.scale(background_img, (Dimensiones.SCREEN_WIDTH, Dimensiones.SCREEN_HEIGHT))
    play_level_music(level)
    while running:
        screen.blit(background_img, (0, 0))
        message_surface = font.render(message, True, Dimensiones.BLACK)
        screen.blit(message_surface, (Dimensiones.SCREEN_WIDTH // 2 - message_surface.get_width() // 2,
                                      Dimensiones.SCREEN_HEIGHT // 2 - message_surface.get_height() // 2))
        draw_button("Comenzar", Dimensiones.SCREEN_WIDTH - 250, Dimensiones.SCREEN_HEIGHT - 60, 200, 50, Dimensiones.GRAY, Dimensiones.GREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and is_button_clicked(Dimensiones.SCREEN_WIDTH - 250, Dimensiones.SCREEN_HEIGHT - 80, 200, 50):
                running = False
        pygame.display.flip()

def restart_game():
    global level, goals_player, goals_enemy, ball_x, ball_y, ball_moving, ball_owned, start_time
    level = 1  # Reiniciar el nivel
    goals_player = 0
    goals_enemy = 0
    ball_x = Dimensiones.SCREEN_WIDTH // 2
    ball_y = Dimensiones.SCREEN_HEIGHT // 2
    ball_moving = False
    ball_owned = False
    start_time = pygame.time.get_ticks()  
    pygame.mixer.music.stop()  # Detener la música actual
    play_level_music(level)  # Cargar y reproducir la música del primer nivel
    print("El juego ha sido reiniciado.")

# Función para mostrar la pantalla de victoria
def display_victory_screen():
    global level 
    pygame.mixer.music.load('videos/Cancion_campeon.mp3')  
    pygame.mixer.music.play(-1, 0.0) 
    victory_background = pygame.image.load('img/Interfaces/VictoriaFinal.png')
    victory_background = pygame.transform.scale(victory_background, (Dimensiones.SCREEN_WIDTH, Dimensiones.SCREEN_HEIGHT))  # Ajustamos el tamaño al de la pantalla
    # Dibujar el fondo
    screen.blit(victory_background, (0, 0))  # Dibuja la imagen de fondo
    # Mostrar el mensaje de victoria
    victory_message = custom_font_large.render("", True, Dimensiones.BLACK)
    screen.blit(victory_message, (Dimensiones.SCREEN_WIDTH // 2 - victory_message.get_width() // 2, Dimensiones.SCREEN_HEIGHT // 3))
    # Mostrar botones de reiniciar y salir (solo texto sin fondo ni borde)
    restart_text = custom_font_medium.render("Reiniciar", True, (255, 255, 255))  # Blanco
    quit_text = custom_font_medium.render("Salir", True, (255, 255, 255))         # Blanco
    restart_button_x = Dimensiones.SCREEN_WIDTH - 700
    restart_button_y = Dimensiones.SCREEN_HEIGHT // 2 + 50
    quit_button_x = Dimensiones.SCREEN_WIDTH - 300
    quit_button_y = Dimensiones.SCREEN_HEIGHT // 2 + 50
    screen.blit(restart_text, (restart_button_x + (200 - restart_text.get_width()) // 2, restart_button_y + (50 - restart_text.get_height()) // 2))
    screen.blit(quit_text, (quit_button_x + (200 - quit_text.get_width()) // 2, quit_button_y + (50 - quit_text.get_height()) // 2))
    pygame.display.flip()  # Actualizar la pantalla
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if restart_button_x < mouse_x < restart_button_x + 200 and restart_button_y < mouse_y < restart_button_y + 50:
                    reset_goals()  # Reinicia los goles
                    restart_game()
                    waiting_for_input = False
                elif quit_button_x < mouse_x < quit_button_x + 200 and quit_button_y < mouse_y < quit_button_y + 50:
                    pygame.quit()
                    sys.exit()
        pygame.time.Clock().tick(60)
# Función para mostrar la pantalla de derrota
def display_perdido_screen():
    global level
    # Reproducir música de derrota
    pygame.mixer.music.load('videos/Cancion_game_over.mp3')  # Cargar archivo de música
    pygame.mixer.music.play(-1, 0.0)  # Reproducir música en bucle
    # Cargar la imagen de fondo de derrota
    lost_background = pygame.image.load('img/Interfaces/perdida.png')
    lost_background = pygame.transform.scale(lost_background, (Dimensiones.SCREEN_WIDTH, Dimensiones.SCREEN_HEIGHT))  # Ajustamos el tamaño al de la pantalla
    screen.blit(lost_background, (0, 0))  # Dibujar el fondo
    # Mostrar el mensaje de derrota
    lost_message = custom_font_large.render("", True, Dimensiones.BLACK)
    screen.blit(lost_message, (Dimensiones.SCREEN_WIDTH // 2 - lost_message.get_width() // 2, Dimensiones.SCREEN_HEIGHT // 3))
    # Mostrar botones de reiniciar y salir (solo texto sin fondo ni borde)
    restart_text = custom_font_medium.render("Reintentar", True, Dimensiones.BLACK)  # Negro
    quit_text = custom_font_medium.render("Salir", True, Dimensiones.BLACK)
    restart_button_x = Dimensiones.SCREEN_WIDTH - 700
    restart_button_y = Dimensiones.SCREEN_HEIGHT // 2 + 50
    quit_button_x = Dimensiones.SCREEN_WIDTH - 300
    quit_button_y = Dimensiones.SCREEN_HEIGHT // 2 + 50
    screen.blit(restart_text, (restart_button_x + (200 - restart_text.get_width()) // 2, restart_button_y + (50 - restart_text.get_height()) // 2))
    screen.blit(quit_text, (quit_button_x + (200 - quit_text.get_width()) // 2, quit_button_y + (50 - quit_text.get_height()) // 2))
    pygame.display.flip()  # Actualizar la pantalla
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if restart_button_x < mouse_x < restart_button_x + 200 and restart_button_y < mouse_y < restart_button_y + 50:
                    reset_goals()  # Reinicia los goles
                    restart_game()
                    ball_x = Dimensiones.SCREEN_WIDTH // 2
                    ball_y = Dimensiones.SCREEN_HEIGHT // 2
                    ball_moving = False
                    ball_owned = False
                    goals_player = 0
                    goals_enemy = 0
                    start_time = pygame.time.get_ticks()  # Reiniciar el tiempo
                    presentation_screen(level)  # Mostrar la pantalla de presentación del nivel
                    waiting_for_input = False
                elif quit_button_x < mouse_x < quit_button_x + 200 and quit_button_y < mouse_y < quit_button_y + 50:
                    pygame.quit()
                    sys.exit()
        pygame.time.Clock().tick(60)
start_screen()
second_screen()
third_screen()
tutorial_screen()
presentation_screen(level)
# Función para pasar al siguiente nivel
def next_level():
    global current_goalkeeper_enemy_image
    # Cambiar la imagen del portero enemigo según el nivel actual
    if level == 1:
        current_goalkeeper_enemy_image = goalkeeper_enemy_images[1]
    elif level == 2:
        current_goalkeeper_enemy_image = goalkeeper_enemy_images[2]
    elif level == 3:
        current_goalkeeper_enemy_image = goalkeeper_enemy_images[3]
def check_ball_possession(player_x, player_y, ball_x, ball_y, distance=30):
    dx = player_x - ball_x
    dy = player_y - ball_y
    return math.sqrt(dx**2 + dy**2) < distance

def check_enemy_steal(player_x, player_y, enemies, ball_owned):
    if ball_owned:
        for enemy in enemies:
            if check_ball_possession(enemy[0], enemy[1], player_x, player_y, distance=30):
                return True, enemy[0], enemy[1]  
    return False, None, None

# Función para disparar la pelota
def shoot_ball(player_x, player_y):
    direction_x = Dimensiones.SCREEN_WIDTH - player_x
    direction_y = random.choice([-1, 1]) * 3  
    distance = math.sqrt(direction_x ** 2 + direction_y ** 2)
    return (direction_x / distance) * 10, (direction_y / distance) * 10  
def move_goalkeeper(y, speed, direction):
    y += speed * direction
    if y <= Dimensiones.SCREEN_HEIGHT // 2 - 100 or y >= Dimensiones.SCREEN_HEIGHT // 2 + 100 - Dimensiones.goalkeeper_size:
        direction *= -1  # Cambiar la dirección cuando toca los límites del área de gol
    return y, direction
# Función para mover el portero compañero automáticamente
def move_partner_goalkeeper(y, speed, direction):
    y += speed * direction
    if y <= Dimensiones.SCREEN_HEIGHT // 2 - 100 or y >= Dimensiones.SCREEN_HEIGHT // 2 + 100 - Dimensiones.goalkeeper_size:
        direction *= -1  # Cambiar la dirección cuando toca los límites del área de gol
    return y, direction
def draw_player(x, y):
    screen.blit(player_image, (x, y))
def draw_ball(x, y):
    screen.blit(Dimensiones.ball_image, (x, y))
def draw_enemy(x, y, level):
    screen.blit(enemy_images[level], (x, y))
def draw_goalkeeper_enemy(x, y):
    screen.blit(current_goalkeeper_enemy_image, (x, y))
def draw_goalkeeper_partner(x, y):
    screen.blit(Dimensiones.goalkeeper_image_partner, (x, y))
# Función para dibujar el puntaje y el tiempo
def draw_score_and_time(goals_player, goals_enemy, time_left):
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Goles: {goals_player} - {goals_enemy}", True, Dimensiones.BLACK)
    time_text = font.render(f"Tiempo: {time_left}", True, Dimensiones.BLACK)
    screen.blit(score_text, (20, 20))
    screen.blit(time_text, (Dimensiones.SCREEN_WIDTH - 200, 20))
# Función para mostrar mensajes
def display_message(message):
    font = pygame.font.SysFont(None, 48)
    message_surface = font.render(message, True, Dimensiones.BLACK)
    screen.fill(Dimensiones.WHITE)  # Llenar la pantalla de blanco antes de mostrar el mensaje
    screen.blit(message_surface, (Dimensiones.SCREEN_WIDTH // 2 - message_surface.get_width() // 2, Dimensiones.SCREEN_HEIGHT // 2 - message_surface.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(2000)  
def draw_names():
    font = pygame.font.SysFont(None, 24)
    player_name_text = font.render(player_name, True, Dimensiones.BLACK)
    partner_name_text = font.render(partner_name, True, Dimensiones.BLACK)
    goalkeeper_name_text = font.render("Courtois", True, Dimensiones.BLACK)
    screen.blit(player_name_text, (player_x, player_y - 20))
    screen.blit(partner_name_text, (partner_goalkeeper_x, partner_goalkeeper_y - 20))
    screen.blit(goalkeeper_name_text, (Dimensiones.goalkeeper_x, Dimensiones.goalkeeper_y - 20))
# Bucle principal del juego
running = True
clock = pygame.time.Clock()
partner_goalkeeper_direction = 1  
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    player_x, player_y = move_player(keys, player_x, player_y, player_speed)
    move_enemies(player_x, player_y, enemies, level + 1)
    partner_goalkeeper_y, partner_goalkeeper_direction = move_partner_goalkeeper(partner_goalkeeper_y, Dimensiones.goalkeeper_speed, partner_goalkeeper_direction)
    if check_ball_possession(player_x, player_y, ball_x, ball_y) and not ball_moving:
        ball_owned = True  # El jugador tiene la pelota
    enemy_steals, new_ball_x, new_ball_y = check_enemy_steal(player_x, player_y, enemies, ball_owned)
    if enemy_steals:
        ball_owned = False  # El enemigo roba la pelota
        ball_x = new_ball_x
        ball_y = new_ball_y
        ball_speed_x = 0
        ball_speed_y = 0
    if ball_owned:
        ball_x = player_x + player_size // 2
        ball_y = player_y + player_size // 2
    if keys[pygame.K_SPACE] and ball_owned:
        ball_speed_x, ball_speed_y = shoot_ball(player_x, player_y)
        ball_moving = True
        ball_owned = False  # El jugador ya no tiene la pelota
    if ball_moving:
        ball_x += ball_speed_x
        ball_y += ball_speed_y
        # Verificar si la pelota sale de la pantalla
        if ball_x < 0 or ball_x > Dimensiones.SCREEN_WIDTH:
            ball_moving = False  # La pelota deja de moverse
            ball_x = Dimensiones.SCREEN_WIDTH // 2
            ball_y = Dimensiones.SCREEN_HEIGHT // 2
    Dimensiones.goalkeeper_y, Dimensiones.goalkeeper_direction = move_goalkeeper(Dimensiones.goalkeeper_y, Dimensiones.goalkeeper_speed, Dimensiones.goalkeeper_direction)
    if ball_x >= goal_area_right.left and goal_area_right.top < ball_y < goal_area_right.bottom:
        goals_player += 1
        gol_sound.play()  # Reproduce el sonido del gol
        total_score += 1
        ball_x = Dimensiones.SCREEN_WIDTH // 2
        ball_y = Dimensiones.SCREEN_HEIGHT // 2
        ball_moving = False
        ball_owned = False  
        if goals_player >= goals_to_win:
            level += 1
            if level > max_level:
                display_victory_screen()
            else:
                reset_goals()
                next_level()  # Cambiar portero enemigo según el nivel
                goals_to_win = set_goals_to_win(level)  # Establece los goles necesarios para el siguiente nivel
                presentation_screen(level)  # Mostrar la pantalla de presentación del siguiente nivel
    
    if ball_x >= Dimensiones.goalkeeper_x and Dimensiones.goalkeeper_y < ball_y < Dimensiones.goalkeeper_y + Dimensiones.goalkeeper_size:
        ball_moving = False  # La pelota deja de moverse
        ball_x = Dimensiones.SCREEN_WIDTH // 2
        ball_y = Dimensiones.SCREEN_HEIGHT // 2
    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
    time_left = max(0, time_limit - elapsed_time)
    if time_left <= 0:
        goals_enemy += 1
        ball_x = Dimensiones.SCREEN_WIDTH // 2
        ball_y = Dimensiones.SCREEN_HEIGHT // 2
        ball_moving = False
        ball_owned = False  
        if goals_enemy >= 1:  # Si los enemigos marcan 3 goles
            display_perdido_screen()
        else:
            start_time = pygame.time.get_ticks() 
    screen.blit(Dimensiones.backgrounds[level - 1], (0, 0)) 
    draw_player(player_x, player_y)
    draw_ball(ball_x, ball_y)
    draw_goalkeeper_enemy(Dimensiones.goalkeeper_x, Dimensiones.goalkeeper_y) 
    draw_goalkeeper_partner(partner_goalkeeper_x, partner_goalkeeper_y) 
    for enemy in enemies:
        draw_enemy(enemy[0], enemy[1], level)
    pygame.draw.rect(screen, Dimensiones.YELLOW, goal_area_right, 2)
    pygame.draw.rect(screen, Dimensiones.YELLOW, goal_area_left, 2)
    draw_score_and_time(goals_player, goals_enemy, int(time_left))
    draw_names()
    pygame.display.flip()
    clock.tick(60) 
pygame.quit()
