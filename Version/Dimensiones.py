import pygame

# Inicializar Pygame
pygame.init()

# Colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRAY = (114, 108, 107 )  # Gris
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

TEXT_COLOR = (0, 0, 0)  # Negro 100%
TEXT_OUTLINE_COLOR = (0, 0, 0)  # Negro 10%
# Dimensiones de la pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Pelota
ball_size = 20

# Enemigos
num_enemies = 4  # Número inicial de enemigos
enemy_size = 40

# Porteros (incluyendo compañero)
goalkeeper_size = 50
goalkeeper_x = SCREEN_WIDTH - 60  # El portero enemigo se mueve cerca del área de gol
goalkeeper_y = SCREEN_HEIGHT // 2 - goalkeeper_size // 2
goalkeeper_speed = 5
goalkeeper_direction = 1

music_files = {
    "start_screen": 'videos/Cancion_inicio.mp3',  # Reemplaza con la ruta a tu archivo de música para la pantalla de inicio
    "second_screen": 'videos/Cancion_Controles.mp3',  # Reemplaza con la ruta a tu archivo de música para la segunda pantalla
    "third_screen": 'videos/SeleccionJugadores.mp3',  # Reemplaza con la ruta a tu archivo de música para la tercera pantalla
    "tutorial_screen": 'videos/Cancion_Tutorial.mp3'  # Reemplaza con la ruta a tu archivo de música para la tercera pantalla
}

# Cargar imágenes de fondo
backgrounds = [
    pygame.transform.scale(pygame.image.load('img/campos/Ambito1_sinBoton.png'), (SCREEN_WIDTH, SCREEN_HEIGHT)),
    pygame.transform.scale(pygame.image.load('img/campos/Ambito2_sinBoton.png'), (SCREEN_WIDTH, SCREEN_HEIGHT)),
    pygame.transform.scale(pygame.image.load('img/campos/Ambito3_sinBoton.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))
]

# Cargar imágenes de los jugadores y enemigos
ball_image = pygame.transform.scale(pygame.image.load('img/balones/Balon_1.png'), (ball_size, ball_size))  # Asegúrate de tener una imagen de pelota
# Cargar imágenes para los porteros
goalkeeper_image_enemy = pygame.transform.scale(pygame.image.load('img/jugadores/PorteroBarcelona_local.png'), (goalkeeper_size, goalkeeper_size))
goalkeeper_image_partner = pygame.transform.scale(pygame.image.load('img/jugadores/PorteroRealMadrid_visitante.png'), (goalkeeper_size, goalkeeper_size))

background_image = pygame.image.load('img/Interfaces/Interfaz_inicio.png')
background_image2 = pygame.image.load('img/Interfaces/Interfaz_Tutorial.png')
background_image3 = pygame.image.load('img/Interfaces/Interfaz_SeleccionEquipo.png')
background_image4 = pygame.image.load('img/campos/Ambito1_Tutorial.png')

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Cargar nueva imagen del portero para el tutorial
goalkeeper_image_tutorial = pygame.transform.scale(pygame.image.load('img/jugadores/Portero_practica.png'), (goalkeeper_size, goalkeeper_size))


# Cargar la fuente personalizada
font_path = 'fonts/retropix.ttf'  # Ruta a tu archivo de fuente
font_size = 20  # Tamaño de la fuente
custom_font = pygame.font.Font(font_path, font_size)

font_path2 = 'fonts/PressStart2P-Regular.ttf'

def draw_button(text, x, y, width, height, color, hover_color):
    text_surface = custom_font.render(text, True, BLACK)  # Usar la fuente personalizada
    screen.blit(text_surface, (x + (width - text_surface.get_width()) // 2, y + (height - text_surface.get_height()) // 2))

# Función para comprobar si el botón ha sido presionado
def is_button_clicked(x, y, width, height):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0]:
        if x < mouse_x < x + width and y < mouse_y < y + height:
            return True
    return False

# Función para reproducir música de fondo
def play_music(track):
    pygame.mixer.music.load(track)
    pygame.mixer.music.play(-1)  # Reproducir en bucle

# Función para la pantalla inicial
def start_screen():
    play_music(music_files["start_screen"])
    running = True
    while running:
        # Dibujar el fondo
        screen.blit(background_image, (0, 0))  # Dibuja la imagen de fondo en la pantalla (en la posición 0,0)
        # Dibujar el botón en la parte inferior derecha
        draw_button("continuar", SCREEN_WIDTH - 250, SCREEN_HEIGHT - 60, 200, 50, GRAY, GREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and is_button_clicked(SCREEN_WIDTH - 250, SCREEN_HEIGHT - 80, 200, 50):
                running = False  # Este evento cierra la pantalla de inicio y abre la siguiente interfaz
        pygame.display.flip()

# Función para la segunda interfaz
def second_screen():
    play_music(music_files["second_screen"])
    running = True
    while running:
        # Dibujar el fondo (podría ser el mismo que el de la pantalla inicial)
        screen.blit(background_image2 , (0, 0))  # Dibuja la imagen de fondo
        # Dibujar el botón en la parte inferior derecha
        draw_button("continuar", SCREEN_WIDTH - 250, SCREEN_HEIGHT - 60, 200, 50, GRAY, GREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and is_button_clicked(SCREEN_WIDTH - 250, SCREEN_HEIGHT - 80, 200, 50):
                running = False  # Este evento cierra la pantalla de continuación y finalmente inicia el juego
        pygame.display.flip()

selected_local = None
selected_visitante = None

# Opciones de jugadores por nivel
jugadores_por_nivel = {
    1: [
        [('img/jugadores/amigo_local.png', 'Local'), ('img/jugadores/amigo_visitante.png', 'Visitante')],
        [('img/jugadores/enemigo_local.png', 'Visitante'), ('img/jugadores/enemigo_visitante.png', 'Local')]
    ],
    2: [
        [('img/jugadores/amigo_local.png', 'Local'), ('img/jugadores/amigo_visitante.png', 'Visitante')],
        [('img/jugadores/bayern.png', 'Visitante'), ('img/jugadores/bayern_2.png', 'Local')]
    ],
    3: [
        [('img/jugadores/amigo_local.png', 'Local'), ('img/jugadores/amigo_visitante.png', 'Visitante')],
        [('img/jugadores/juvents.png', 'Visitante'), ('img/jugadores/juvents_2.png', 'Local')]
    ]
}


def third_screen(level):
    global selected_local, selected_visitante  # Usar variables globales para mantener las elecciones
    play_music(music_files["third_screen"])
    running = True
    
    # Obtener las opciones de jugadores según el nivel
    jugador_local_opciones, jugador_visitante_opciones = jugadores_por_nivel.get(level, jugadores_por_nivel[1])
    
    # Inicialización de los índices de selección
    jugador_local_index = 0
    jugador_visitante_index = 0
    
    # Cargar las imágenes de los jugadores según el índice seleccionado
    jugador_local_actual = pygame.image.load(jugador_local_opciones[jugador_local_index][0])
    jugador_visitante_actual = pygame.image.load(jugador_visitante_opciones[jugador_visitante_index][0])
    
    # Ajustar las imágenes a un tamaño adecuado
    jugador_local_actual = pygame.transform.scale(jugador_local_actual, (100, 100))
    jugador_visitante_actual = pygame.transform.scale(jugador_visitante_actual, (100, 100))
    
    balon_imagenes = ['img/balones/Balon_1.png', 'img/balones/Balon_2.png']
    balon_index = 0
    balon_actual = pygame.image.load(balon_imagenes[balon_index])
    balon_actual = pygame.transform.scale(balon_actual, (30, 30))

    while running:
        screen.blit(background_image3, (0, 0))
        screen.blit(jugador_local_actual, (SCREEN_WIDTH // 3 - jugador_local_actual.get_width() // 2, SCREEN_HEIGHT // 2 - jugador_local_actual.get_height() // 2))
        screen.blit(jugador_visitante_actual, (2 * SCREEN_WIDTH // 3 - jugador_visitante_actual.get_width() // 2, SCREEN_HEIGHT // 2 - jugador_visitante_actual.get_height() // 2))
        balon_x = SCREEN_WIDTH  - balon_actual.get_width() - 370
        balon_y = SCREEN_HEIGHT - balon_actual.get_height() - 130
        screen.blit(balon_actual, (balon_x, balon_y))
        draw_button("Jugar", SCREEN_WIDTH - 250, SCREEN_HEIGHT - 60, 200, 50, GRAY, GREEN)
        draw_button("Tutorial", SCREEN_WIDTH - 500, SCREEN_HEIGHT - 60, 200, 50, GRAY, BLUE)  # Botón de Tutorial
        draw_button(jugador_local_opciones[jugador_local_index][1], SCREEN_WIDTH // 2 - 95, SCREEN_HEIGHT - 450, 80, 40, GRAY, BLUE)
        draw_button(jugador_visitante_opciones[jugador_visitante_index][1], 2 * SCREEN_WIDTH // 3 - 125, SCREEN_HEIGHT - 450, 80, 40, GRAY, RED)
        
        # Mostrar el nivel actual en la parte superior
        # Cargar la fuente RetroPix desde el archivo
        retro_font = pygame.font.Font(font_path2, 25)
        retro_font.set_bold(True)
        # Mostrar el nivel actual en la parte superior
        level_text = retro_font.render(f"Nivel: {level}", True, GRAY)  # Usar la fuente RetroPix
        screen.blit(level_text, (SCREEN_WIDTH // 2 - level_text.get_width() // 2, 55))  # Dibujar el texto en la pantalla

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # Detecta clic en el botón "Jugar" para iniciar el juego
            if event.type == pygame.MOUSEBUTTONDOWN and is_button_clicked(SCREEN_WIDTH - 250, SCREEN_HEIGHT - 80, 200, 50):
                if selected_local is None or selected_visitante is None:
                    print("Error: Debes seleccionar ambos equipos.")
                else:
                    print(f"Selección Local: {selected_local}")
                    print(f"Selección Visitante: {selected_visitante}")
                    running = False  # Este evento inicia el juego
            # Detecta clic en el botón "Tutorial" para iniciar la pantalla de tutorial
            if event.type == pygame.MOUSEBUTTONDOWN and is_button_clicked(SCREEN_WIDTH - 500, SCREEN_HEIGHT - 80, 200, 50):
                tutorial_screen()  # Ir a la pantalla de tutorial
            # Cambiar imagen del jugador local
            if event.type == pygame.MOUSEBUTTONDOWN and is_button_clicked(SCREEN_WIDTH // 2 - 95, SCREEN_HEIGHT - 450, 80, 40):
                jugador_local_index = (jugador_local_index + 1) % len(jugador_local_opciones)
                jugador_local_actual = pygame.image.load(jugador_local_opciones[jugador_local_index][0])
                jugador_local_actual = pygame.transform.scale(jugador_local_actual, (100, 100))
                selected_local = jugador_local_opciones[jugador_local_index][1]  # Actualizar la elección de Local
                print(f"Seleccionado equipo Local: {selected_local}")  # Imprime la selección del equipo local
            # Cambiar imagen del jugador visitante
            if event.type == pygame.MOUSEBUTTONDOWN and is_button_clicked(2 * SCREEN_WIDTH // 3 - 125, SCREEN_HEIGHT - 450, 80, 40):
                jugador_visitante_index = (jugador_visitante_index + 1) % len(jugador_visitante_opciones)
                jugador_visitante_actual = pygame.image.load(jugador_visitante_opciones[jugador_visitante_index][0])
                jugador_visitante_actual = pygame.transform.scale(jugador_visitante_actual, (100, 100))
                selected_visitante = jugador_visitante_opciones[jugador_visitante_index][1]  # Actualizar la elección de Visitante
                print(f"Seleccionado equipo Visitante: {selected_visitante}")  # Imprime la selección del equipo visitante
            # Cambiar la imagen del balón si se hace clic en él
            if event.type == pygame.MOUSEBUTTONDOWN and is_button_clicked(balon_x, balon_y, 30, 30):
                balon_index = (balon_index + 1) % len(balon_imagenes)
                balon_actual = pygame.image.load(balon_imagenes[balon_index])
                balon_actual = pygame.transform.scale(balon_actual, (30, 30))
        pygame.display.flip()


# Función para la pantalla de tutorial
def tutorial_screen():
    play_music(music_files["tutorial_screen"])  # Puedes agregar música específica para el tutorial si lo deseas
    running = True
    while running:
        screen.blit(backgrounds[0], (0, 0)) 
        draw_button("Regresar", SCREEN_WIDTH - 250, SCREEN_HEIGHT - 60, 200, 50, GRAY, GREEN)
        draw_button("Comenzar a Practicar", SCREEN_WIDTH - 250, SCREEN_HEIGHT - 120, 200, 50, GRAY, GREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if is_button_clicked(SCREEN_WIDTH - 250, SCREEN_HEIGHT - 80, 200, 50):
                    running = False  # Regresa a la pantalla de selección
                elif is_button_clicked(SCREEN_WIDTH - 250, SCREEN_HEIGHT - 140, 200, 50):
                    presentation_screenTutorial(0)  # Ir a la pantalla de presentación del nivel 0
                    running = False
        pygame.display.flip()
# Función para mover el portero enemigo
def move_goalkeeper(y, speed, direction):
    # Calculamos los límites del arco
    upper_limit = SCREEN_HEIGHT // 2 - 100  # Limite superior del área del arco
    lower_limit = SCREEN_HEIGHT // 2 + 100 - goalkeeper_size  # Limite inferior del área del arco
    
    # Mover al portero
    y += speed * direction
    
    # Asegurarse de que el portero no salga del área del arco
    if y <= upper_limit or y >= lower_limit:
        direction *= -1  # Cambiar la dirección cuando toca los límites del área de gol
    
    return y, direction

# Agregar la imagen de la pelota
ball_image = pygame.transform.scale(pygame.image.load('img/balones/Balon_1.png'), (ball_size, ball_size))  # Ajusta el tamaño de la pelota si es necesario

def presentation_screenTutorial(lvl):
    if lvl == 0:
        # Configuración del nivel de tutorial
        tutorial_running = True
        player_x = SCREEN_WIDTH // 4  # Posición inicial del jugador
        player_y = SCREEN_HEIGHT // 2  # Posición inicial del jugador
        player_speed = 5
        player_image = pygame.transform.scale(pygame.image.load('img/jugadores/amigo_local.png'), (50, 50))
        
        # Inicialización de la pelota
        ball_x = SCREEN_WIDTH // 2  # Balón en el centro del campo
        ball_y = SCREEN_HEIGHT // 2 + 30  # Colocamos la pelota debajo del jugador (ajustamos la posición vertical)
        ball_size = 30  # Definir el tamaño de la pelota
        ball_speed = 5
        ball_direction = 0  # No mueve el balón inicialmente
        ball_moving = False
        ball_rect = pygame.Rect(ball_x, ball_y, ball_size, ball_size)  # Rectángulo para el control del balón
        ball_following_player = False  # La pelota no sigue al jugador al principio

        goalkeeper_x = SCREEN_WIDTH - 100
        goalkeeper_y = SCREEN_HEIGHT // 2 - 25
        goalkeeper_direction = 1
        goalkeeper_speed = 3

        # Rectángulo del portero enemigo
        goalkeeper_rect = pygame.Rect(goalkeeper_x, goalkeeper_y, goalkeeper_size, goalkeeper_size)
        
        while tutorial_running:
            screen.fill(WHITE)  # Fondo blanco para el tutorial
            screen.blit(background_image4, (0, 0))  # Fondo del campo

            # Dibujar jugador
            screen.blit(player_image, (player_x, player_y))
            
            # Dibujar pelota (con la imagen)
            screen.blit(ball_image, (ball_x, ball_y))

            # Dibujar portero enemigo
            # screen.blit(goalkeeper_image_enemy, (goalkeeper_x, goalkeeper_y))
            # Dibujar el portero enemigo usando la nueva imagen en el tutorial
            screen.blit(goalkeeper_image_tutorial, (goalkeeper_x, goalkeeper_y))

            
            # Instrucciones en pantalla
            instructions = [
                
            ]
            for i, text in enumerate(instructions):
                text_surface = custom_font.render(text, True, BLACK)
                screen.blit(text_surface, (50, 50 + i * 30))
            
            # Control del jugador
            keys = pygame.key.get_pressed()
            
            # Movimiento del jugador (Limitar el movimiento dentro de la pantalla)
            if keys[pygame.K_LEFT] and player_x > 0:
                player_x -= player_speed
            if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - 50:  # Resto del tamaño del jugador
                player_x += player_speed
            if keys[pygame.K_UP] and player_y > 0:
                player_y -= player_speed
            if keys[pygame.K_DOWN] and player_y < SCREEN_HEIGHT - 50:  # Resto del tamaño del jugador
                player_y += player_speed

            # Si la pelota está cerca del jugador, que lo siga
            if not ball_moving:
                # Verificamos si la pelota está cerca del jugador
                if abs(ball_x - player_x) < 50 and abs(ball_y - player_y) < 50:
                    ball_following_player = True
                else:
                    ball_following_player = False
                
                if ball_following_player:
                    # La pelota sigue al jugador, pero ahora se coloca debajo
                    ball_x = player_x  # La pelota sigue la posición X del jugador
                    ball_y = player_y + 30  # La pelota se coloca debajo del jugador (ajustamos la distancia aquí)

            # Control del balón (patear)
            if keys[pygame.K_SPACE] and not ball_moving and ball_following_player:
                ball_moving = True
                ball_direction = 1  # Hacia la derecha (puedes cambiar esto si deseas otra dirección)
                # Establecemos una velocidad para el disparo
                ball_speed = 7

            # Movimiento del balón
            if ball_moving:
                ball_x += ball_direction * ball_speed
                # Si el balón sale de la pantalla, lo reiniciamos al centro
                if ball_x > SCREEN_WIDTH:
                    ball_x = SCREEN_WIDTH // 2
                    ball_y = SCREEN_HEIGHT // 2 + 30  # Reposicionar la pelota debajo del jugador
                    ball_moving = False

            # Movimiento del portero enemigo
            goalkeeper_y, goalkeeper_direction = move_goalkeeper(goalkeeper_y, goalkeeper_speed, goalkeeper_direction)

            # Detección de colisiones con el portero (si el balón se mueve hacia el portero)
            if ball_rect.colliderect(goalkeeper_rect):
                # Si el balón colisiona con el portero, lo reiniciamos
                ball_x = SCREEN_WIDTH // 2
                ball_y = SCREEN_HEIGHT // 2 + 30  # Reposicionar la pelota debajo del jugador
                ball_moving = False

            # Dibujar botón de "Siguiente"
            draw_button("Siguiente", SCREEN_WIDTH - 250, SCREEN_HEIGHT - 60, 200, 50, GRAY, GREEN)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN and is_button_clicked(SCREEN_WIDTH - 250, SCREEN_HEIGHT - 60, 200, 50):
                    tutorial_running = False  # Avanza al siguiente nivel o pantalla de selección
            pygame.display.flip()
