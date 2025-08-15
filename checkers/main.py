
import pygame
from checkers1.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from checkers1.game import Game
from minimax.algorithm import minimax
import os
pygame.mixer.init()

# Background music
SOUND_PATH = os.path.join(os.path.dirname(__file__), "sounds")

pygame.mixer.music.load(os.path.join(SOUND_PATH, "background-music.mp3"))
pygame.mixer.music.set_volume(0.5)  # Volume: 0.0 to 1.0
pygame.mixer.music.play(-1)

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(FPS)
        
        if game.turn == WHITE:
            value, new_board = minimax(game.get_board(), 4, WHITE, game)
            game.ai_move(new_board)
            
        if game.winner() != None:
            print(game.winner())
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()
    
    pygame.quit()

main()