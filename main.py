#Kniznice
import pygame
import random

pygame.init()

#vlastnosti okna hry
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

#Okno hry
obrazovka = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chameleon Jump")

#rychlosť pohybu
clock = pygame.time.Clock()
FPS = 60

#zakony hry
SCROLL_THRESH = 200
scroll = 0
GRAVITY = 1
MAX_PLATFORMS = 10
bg_scroll = 0
game_over = False
score = 0
fade_counter = 0

#FARBY
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


#define font
font_small = pygame.font.SysFont("Lucida Sans", 20)
font_big = pygame.font.SysFont("Lucida Sans", 22)

#obrazky
chameleon_image = pygame.image.load("zelenyy.png").convert_alpha()
bg_image = pygame.image.load("game_background_3. 2.png").convert_alpha()
platform_image = pygame.image.load("platforma.png").convert_alpha()

#funkcia na text na obrazovke
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    obrazovka.blit(img, (x, y))


#funkcia na vykreslenie pozadia
def draw_bg(bg_scroll):
    obrazovka.blit(bg_image, (0, 0 + bg_scroll))
    obrazovka.blit(bg_image, (0, -600 + bg_scroll))



#klasa hráč
class Player():
    def __init__(self, x, y):
        self.image = pygame.transform.scale(chameleon_image, (40, 70))
        self.width = 35
        self.height = 60
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
        self.vel_y = 0
        self.flip = False

    def move(self):
        #reset variables
        scroll = 0
        dx = 0
        dy = 0

        #stlacanie klaves
        key = pygame.key.get_pressed()
        if key[pygame.K_a] :
            dx = -8
            self.flip = True
        if key[pygame.K_d] :
            dx = 8
            self.flip = False


        #gravitacia 2
        self.vel_y += GRAVITY
        dy += self.vel_y


        #uistenie nech nejde za obrazovku
        if self.rect.left + dx < 0:
            dx = 0 - self.rect.left
        if self.rect.right + dx > SCREEN_WIDTH:
            dx = SCREEN_WIDTH - self.rect.right


        #kolizia s platformamy
        for platform in platform_group:
            #kolizia Y
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy,self.width, self.height ):

                #check if above platform
                if self.rect.bottom < platform.rect.centery:
                    if self.vel_y > 0:
                        self.rect.bottom = platform.rect.top
                        dy = 0
                        self.vel_y = -20



        #check if the player has bounced onm the top of the screm
        if self.rect.top <= SCROLL_THRESH:
            #if player is bouncing
            if self.vel_y < 0:
                scroll = -dy




       #obnovovanie rect pozicie
        self.rect.x += dx
        self.rect.y += dy + scroll

        return  scroll

    def draw(self):
        obrazovka.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x -2, self.rect.y - 5))
        pygame.draw.rect(obrazovka, WHITE, self.rect, 2)


#klasa platforma
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platform_image, (width, 10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, scroll):

        #update pkatform
        self.rect.y += scroll


        #chcek if platform has gone off the screen
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

#Player instance
chameleon = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)

#create sprite groups
platform_group = pygame.sprite.Group()

#štartovacia platforma
platform = Platform(SCREEN_WIDTH // 2 -50, SCREEN_HEIGHT - 50, 100)
platform_group.add(platform)



#loop
run = True
while run:

    clock.tick(FPS)

    if game_over == False:
        scroll = chameleon.move()

        #vykreslit pozadie
        bg_scroll += scroll
        if bg_scroll >= 600:
            bg_scroll = 0
        draw_bg(bg_scroll)

        #generate úlatforms
        if len(platform_group) < MAX_PLATFORMS:
            p_w = random.randint(40, 60)
            p_x = random.randint(0, SCREEN_WIDTH - p_w)
            p_y = platform.rect.y - random.randint(80, 120)
            platform = Platform(p_x, p_y, p_w)
            platform_group.add(platform)




        #update platforms
        platform_group.update(scroll)

        # draw sprites
        platform_group.draw(obrazovka)
        chameleon.draw()


        #chcek game over
        if chameleon.rect.top > SCREEN_HEIGHT:
            game_over = True

    else:
        if fade_counter < SCREEN_WIDTH:
            fade_counter += 5
            for y in range(0, 6, 2):
                pygame.draw.rect(obrazovka, BLACK, (0, y*100, fade_counter, 100))
                pygame.draw.rect(obrazovka, BLACK, (SCREEN_WIDTH -  fade_counter, (y+1)*100, SCREEN_WIDTH, 100))
        draw_text("GAME OVER", font_big, WHITE, 130, 200)
        draw_text("SCORE: " + str(score), font_big, WHITE, 130, 250)
        draw_text("PRESS SPACE TO PLAY AGAIN", font_big, WHITE, 40, 300)
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            #reset
            game_over = False
            score = 0
            scroll = 0
            fade_counter = 0
             # reposition chameleom
            chameleon.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT -150)
            #reset platformy
            platform_group.empty()
            # štartovacia platforma
            platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50, 100)
            platform_group.add(platform)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    pygame.display.update()

pygame.quit()






