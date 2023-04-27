import pygame
import sys
import math

# initialize Pygame
pygame.init()

# set up the window
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Go Game')

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# set up the font
font = pygame.font.SysFont(None, 48)

# set up the clock
clock = pygame.time.Clock()

# set up the ball
ball_rect = pygame.Rect(50, 40, 25, 25)
ball_color = GREEN
ball_speed = 5

# set up the boards
boards = []
board_1_rect = pygame.Rect(50, 50, 100, 20)
boards.append(board_1_rect)
board_2_rect = pygame.Rect(200, 150, 100, 20)
boards.append(board_2_rect)
board_3_rect = pygame.Rect(50, 250, 100, 20)
boards.append(board_3_rect)
board_4_rect = pygame.Rect(200, 350, 100, 20)
boards.append(board_4_rect)
victory_board_rect = pygame.Rect(50, 450, 150, 30)
boards.append(victory_board_rect)

# set up thorns
thorns_rect = pygame.Rect(0, 550, 1000, 50)
thorns_color = RED

# set up the AI variables
ai_speed = 3
ai_next_board = 0 # index of the next board in the path

# set up game state
game_over = False
you_win = False

# define the AI function
def ai_move():
    global ai_next_board
    distances = []
    for board in boards:
        distance = math.sqrt((board.centerx - ball_rect.centerx)**2 + (board.centery - ball_rect.centery)**2)
        distances.append(distance)
    ai_next_board = distances.index(min(distances))

# main game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # move the ball using the AI algorithm
    if not you_win:
        ai_move()
        next_board_rect = boards[ai_next_board]
        if ball_rect.bottom < next_board_rect.top:
            ball_rect.move_ip(0, ball_speed)
        else:
            # if the ball has reached the next board, update the next board index
            ai_next_board += 1
            if ai_next_board >= len(boards):
                next_board_rect = victory_board_rect
                you_win = True
            else:
                next_board_rect = boards[ai_next_board]

        # move the ball towards the next board
        dx = next_board_rect.centerx - ball_rect.centerx
        dy = next_board_rect.centery - ball_rect.centery
        distance = math.sqrt(dx**2 + dy**2)
        if distance > ball_speed:
            dx = dx * ball_speed / distance
            dy = dy * ball_speed / distance
        ball_rect.move_ip(dx, dy)

    # check for collision with thorns
    if ball_rect.colliderect(thorns_rect):
        game_over = True

    # clear the screen
    window_surface.fill(WHITE)

    # draw the ball and boards
    pygame.draw.circle(window_surface, ball_color, ball_rect.center, ball_rect.width // 2)

    # draw the boards
    for board_rect in boards:
        pygame.draw.rect(window_surface, BLACK, board_rect)
        

    # draw the victory board
    pygame.draw.rect(window_surface, GREEN, victory_board_rect)
    font = pygame.font.SysFont(None, 40)
    victory_board_text = font.render('VICTORY!', True, BLACK)
    victory_board_text_rect = victory_board_text.get_rect(center=victory_board_rect.center)
    window_surface.blit(victory_board_text, victory_board_text_rect)

    # draw the thorns
    pygame.draw.rect(window_surface, thorns_color, thorns_rect)


    # draw the victory message if the player has won
    if you_win:
        font = pygame.font.SysFont(None, 100)
        victory_text = font.render('You Win!', True, WHITE)
        window_surface.fill(GREEN)
        victory_rect = victory_text.get_rect()
        victory_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        window_surface.blit(victory_text, victory_rect)



    # update the display
    pygame.display.update()

    # tick the clock
    clock.tick(60)

# game over
game_over_text = font.render('Game Over', True, RED,)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
window_surface.blit(game_over_text, game_over_rect)
pygame.display.update()
pygame.time.wait(2000)

# wait for a moment before quitting
pygame.time.wait(3000)

# quit Pygame
pygame.quit()
sys.exit()
