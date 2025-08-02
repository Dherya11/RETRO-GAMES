import pygame
import os 

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galaxy Fighters")

WHITE = (255, 255, 255)

FPS = 60

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_yellow.png"))
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_red.png"))

def draw_window():
    WIN.fill(WHITE)
    WIN.blit(YELLOW_SPACESHIP_IMAGE, (100, 100))
    WIN.bliy(RED_SPACESHIP_IMAGE, (700, 100))
    pygame.display.update()

def main():
    clock = pygame.time.Clock()
    run = True
      
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        draw_window()
    pygame.quit()    
    
if __name__ == "__main__":
    main()    