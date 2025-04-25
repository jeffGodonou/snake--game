"""
Date: 2021-06-27
Created by: Jeff G.
Inspired by: https://www.edureka.co/blog/snake-game-with-pygame/
"""

import pygame
import random
import time
pygame.init()

"""
TODO: create obstacle in the game 
TODO: create levels
"""

"""
Define colors
"""
black = (0, 0, 0)
blue = (50, 50, 100)
green  = (0, 255, 0)
red = (255, 0, 0)
white = (255, 255, 255)
yellow = (255, 255, 102)

dis_width = 800
dis_height = 600

dis = pygame.display.set_mode((dis_width, dis_height), pygame.RESIZABLE)
pygame.display.set_caption('Snake game by Jeff G.')

clock = pygame.time.Clock()

snake_block = 10
snake_speed = 15

font_style = pygame.font.SysFont("timesnewroman", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

"""
Define the score
"""
def your_score(score):
    value = score_font.render("Score: " + str(score), True, yellow)
    dis.blit(value, [0, 0])

"""
Draw the snake
"""
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

"""
Define message object
"""
def message (msg, color):
    lines = msg.split('\n')
    y_offset = dis_height / 2
    for line in lines:
        m = font_style.render(line, True, color)
        dis.blit(m, [dis_width / 5, y_offset])
        y_offset += 30
    
def game_over_screen(timer_mode):
    over = True 
    while over:
        dis.fill(white)
        message("Game Over!\n Press: \nM-Main Menu\nQ-Quit\nR-Play again", black)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_r:
                    gameloop(timer_mode)
                elif event.key == pygame.K_m:
                    main_menu()    
    
"""
Main menu function
"""    
def main_menu():
    menu = True
    while menu:
        dis.fill(blue)
        title = font_style.render("Main Menu", True, white)
        dis.blit(title, [dis_width / 2.5, dis_height / 3])
        message(" Press T-Timer Mode \n Press P-Training Mode", white)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    gameloop(timer_mode = True)
                elif event.key == pygame.K_p:
                    gameloop(timer_mode = False)

def gameloop(timer_mode): 
    game_over = False
    game_pause = False
    game_close = False
    
    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    ## Randomly generate the food
    foodx = round(random.randrange(0, dis_width - (2 * snake_block)) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - (2 * snake_block)) / 10.0) * 10.0
    
    ## Start the time
    start_time = time.time()
    time_limit = 180 if timer_mode else None
    
    ## Game Pause behavior
    def pause_game():
        game_pause = True
        while game_pause:
            message("Game paused. Press C to continue or Q to quit", red)
            your_score(Length_of_snake - 1)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        game_pause = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        quit()

    while not game_over:

        while game_close == True:
            game_over_screen(timer_mode)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    x1_change = 0
                    y1_change = -snake_block
                elif event.key == pygame.K_DOWN:
                    x1_change = 0
                    y1_change = snake_block
                elif event.key == pygame.K_p:
                    game_pause = True
                    pause_game()
                elif event.key == pygame.K_ESCAPE:
                    game_over = True
    
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
    
        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)

        """
        Draw the contour of the field
        """
        pygame.draw.line(dis, black, [0, 0], [0, dis_height], 2 )
        pygame.draw.line(dis, black, [0, 0], [dis_width, 0], 2 )
        pygame.draw.line(dis, black, [dis_width, 0], [dis_width, dis_height], 2 )
        pygame.draw.line(dis, black, [0, dis_height], [dis_width, dis_height], 2 )
        
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        your_score(Length_of_snake - 1)
        
        ## Display the timer if in timer mode
        if timer_mode:
            elapsed_time = time.time() - start_time
            remaining_time = max(0, time_limit - elapsed_time)
            timer_text = font_style.render(f"Time Left: {int(remaining_time)}", True , red)
            dis.blit(timer_text, [dis_width -200, 0])
            if remaining_time <= 0:
                game_close = True

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - (2 *snake_block)) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - (2 * snake_block)) / 10.0) * 10.0
            Length_of_snake += 1

        clock.tick(snake_speed)
        
    pygame.quit()
    quit()

main_menu()