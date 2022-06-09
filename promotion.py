import pygame

from button import Button

pygame.init()

WD = 100
HG = 120
WIDTH = 720
SQ_SIZE = WIDTH // 8

SCREEN = pygame.display.set_mode((720, 720))
# le nom de la fenetre
pygame.display.set_caption("Chess game")

BG = pygame.transform.smoothscale(pygame.image.load("assets/background.jpg"), (WD, HG))
img = pygame.transform.smoothscale(pygame.image.load("assets/Play Rect.png"), (WD, 50))


# liste de promo avec image
# knight = pygame.transform.smoothscale(pygame.image.load("images/wN.png"), (50, 50))
# bishop = pygame.transform.smoothscale(pygame.image.load("images/wB.png"), (50, 50))
# queen = pygame.transform.smoothscale(pygame.image.load("images/wQ.png"), (50, 50))
# rook = pygame.transform.smoothscale(pygame.image.load("images/wR.png"), (50, 50))

def get_font(size):  # responsable d'afficher l'écriture sous la taille choisie (size)
    return pygame.font.Font(None, size)


def promotion(row, col):
    running = True
    piece_promo = ""
    clock = pygame.time.Clock()
    while running:
        clock.tick(60)
        size = 30
        if row == 0:
            VALUE = 0
        else:
            VALUE = WIDTH

        if col < 4:
            VALUE2 = col * SQ_SIZE + 1.4 * WD
        else:
            VALUE2 = col * SQ_SIZE - WD // 2

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        Knight = Button(img, pos=(VALUE2, abs(VALUE - 25)),
                        text_input="Knight", font=get_font(size), base_color="#d7fcd4", hovering_color="White")
        Bishop = Button(img, pos=(VALUE2, abs(VALUE - 80)),
                        text_input="Bishop", font=get_font(size), base_color="#d7fcd4", hovering_color="White")
        Queen = Button(img, pos=(VALUE2, abs(VALUE - 135)),
                       text_input="Queen", font=get_font(size), base_color="#d7fcd4", hovering_color="White")
        Rook = Button(img, pos=(VALUE2, abs(VALUE - 190)),
                      text_input="Rook", font=get_font(size), base_color="#d7fcd4", hovering_color="White")
        # QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550),
        #                      text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        # respensable du changement de la couleur quand la souris est sur l'élément
        for button in [Knight, Bishop, Queen, Rook]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if Knight.checkForInput(MENU_MOUSE_POS):
                        piece_promo = "N"
                        running = False
                    if Bishop.checkForInput(MENU_MOUSE_POS):
                        piece_promo = "B"
                        running = False
                    if Queen.checkForInput(MENU_MOUSE_POS):
                        print("Queen")
                        piece_promo = "Q"
                        running = False
                    if Rook.checkForInput(MENU_MOUSE_POS):
                        print("Rook")
                        piece_promo = "R"
                        running = False
                # if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                #     pygame.quit()
                #     sys.exit()
        pygame.display.update()
    return piece_promo
