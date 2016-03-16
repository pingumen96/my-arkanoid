# disegnare mattoncini
import pygame

# variabili globali
HEIGHT = 600
WIDTH = 800
FPS = 30
clock = pygame.time.Clock()
fineGioco = False

# colori
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKYBLUE = (173, 216, 230)
GREY = (128, 128, 128)
REALBLUE = (39, 64, 139)
ORANGE = (255, 165, 0)

schermataGioco = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Arkanoid')

# movimenti barra_P1
BAR_SPEED = 10
P1_position = {'x': int(WIDTH * 2 / 5), 'y': HEIGHT - 14}
P1_x = int(WIDTH * 2 / 5)
P1_y = HEIGHT - 14

# elementi gioco
barra_P1 = pygame.Rect(P1_position['x'], P1_position['y'], int(
    WIDTH / 6), 10)  # da posizionare al centro orizzontalmente
palla = pygame.draw.circle(schermataGioco, WHITE, [
                           barra_P1.centerx, barra_P1.top], 6)


# blocchi da distruggere
# INIZIO DEBUG
lista_blocchi = []
origin_y = 10  # nome variabile da migliorare
for x in range(0, 8):
    origin_x = 15
    origin_y += 20
    for y in range(0, 13):
        lista_blocchi.append({"esiste": True, "forma": pygame.Rect(
            origin_x, origin_y, 50, 10), "draw": None})
        origin_x += 60
        # #qui non ci fa niente, andrebbe nel ciclo esterno

prova = pygame.Rect(300, 200, 60, 20)  # prova di mattone da buttare giù
# FINE DEBUG

# movimenti pallina
pallina_x = barra_P1.centerx
pallina_y = barra_P1.top - 6
velocita_pallina_x = 10
velocita_pallina_y = -10

# booleane utili
pressed_left = False
pressed_right = False
palla_partita = False
collisione_palla = False

# loop del gioco
while not fineGioco:
    clock.tick(FPS)

    if not palla_partita:
        pallina_x = barra_P1.centerx
        pallina_y = barra_P1.top - 6

    # loop eventi
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            fineGioco = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                pressed_right = True
            if event.key == pygame.K_LEFT:
                pressed_left = True
            if event.key == pygame.K_RETURN:
                palla_partita = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                pressed_right = False
            if event.key == pygame.K_LEFT:
                pressed_left = False

    # movimenti barra
    if pressed_left and not sponda_sinistra.colliderect(barra_P1):
        P1_position['x'] -= BAR_SPEED
    elif pressed_right and not sponda_destra.colliderect(barra_P1):
        P1_position['x'] += BAR_SPEED

    # movimenti palla
    if palla_partita:
        if (palla.colliderect(sponda_sinistra) or palla.left <= sponda_sinistra.right) or (palla.colliderect(sponda_destra) or palla.right >= sponda_destra.left):
            velocita_pallina_x = -velocita_pallina_x
        elif palla.colliderect(sponda_alto) or palla.top <= sponda_alto.bottom:
            velocita_pallina_y = -velocita_pallina_y
        elif palla.colliderect(barra_P1) or (palla.bottom >= barra_P1.top and not palla_partita):
            velocita_pallina_y = -velocita_pallina_y
            if palla.centerx > barra_P1.centerx:  # funziona, forse è da calibrare
                velocita_pallina_x += 2
            elif palla.centerx < barra_P1.centerx:
                velocita_pallina_x -= 2
        elif palla.colliderect(sponda_basso):
            palla_partita = False
        else:
            for x in range(0, len(lista_blocchi)):
                try:  # eccezioni riguardanti gli elementi della lista equivalenti a None vengono ignorate
                    if palla.colliderect(lista_blocchi[x]["draw"]):
                        lista_blocchi[x]["esiste"] = False
                        velocita_pallina_y = -velocita_pallina_y
                except:
                    pass

    # modifica velocità pallina
    pallina_x += velocita_pallina_x
    pallina_y += velocita_pallina_y

    # disegno schermata di gioco
    schermataGioco.fill(BLACK)
    if palla_partita == False:
        palla = pygame.draw.circle(schermataGioco, ORANGE, [
                                   barra_P1.centerx, barra_P1.top - 6], 6)
    else:
        palla = pygame.draw.circle(schermataGioco, ORANGE, [
                                   pallina_x, pallina_y], 6)
    sponda_alto = pygame.draw.line(
        schermataGioco, WHITE, [2, 2], [WIDTH - 2, 2])
    sponda_basso = pygame.draw.line(
        schermataGioco, WHITE, [2, HEIGHT - 2], [WIDTH - 2, HEIGHT - 2])
    sponda_sinistra = pygame.draw.line(
        schermataGioco, WHITE, [2, 2], [2, HEIGHT - 2])
    sponda_destra = pygame.draw.line(
        schermataGioco, WHITE, [WIDTH - 2, 2], [WIDTH - 2, HEIGHT - 2])
    barra_P1 = pygame.Rect(P1_position['x'], P1_position[
                           'y'], int(WIDTH / 6), 10)
    pygame.draw.rect(schermataGioco, WHITE, barra_P1)

    # disegno livello
    for x in range(0, len(lista_blocchi)):
        try:  # eccezioni riguardanti gli elementi della lista equivalenti a None vengono ignorate
            if lista_blocchi[x]["esiste"] == True:
                lista_blocchi[x]["draw"] = pygame.draw.rect(
                    schermataGioco, WHITE, lista_blocchi[x]["forma"])
            elif lista_blocchi[x]["esiste"] == False:  # se il blocco non esiste più
                lista_blocchi[x] = None
        except:
            pass

    pygame.display.update()
pygame.quit()
quit()
