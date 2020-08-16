import pygame
import random
import os
pygame.mixer.init()
pygame.init()


# colors
white = (255,255,255)
red = (255,0,0)
black = (0,0,0)

# Creating Window
screen_width = 600
screen_height = 400
gameWindow = pygame.display.set_mode((screen_width,screen_height))

# background image
back_image = pygame.image.load("snake_image.jpg")
back_image = pygame.transform.scale(back_image,(screen_width,screen_height)).convert_alpha()
# Game Title
pygame.display.set_caption("Snake Game")
pygame.display.update()



clock = pygame.time.Clock()
font = pygame.font.SysFont(None,30)

def screen_text(text, color, x, y):
    screen_text = font.render(text,True,color)
    gameWindow.blit(screen_text, [x,y])

def plot_snake(gameWindow,color,snake_list,snake_size):
    for x, y in snake_list:
        pygame.draw.rect(gameWindow, black, [x, y, snake_size, snake_size])

def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill(white)
        screen_text("Welcome To Snake Game",red,120,150)
        screen_text("Press Spacebar To Play!", red, 125, 170)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load('back.mp3')
                    pygame.mixer.music.play()
                    gameloop()
        pygame.display.update()
        clock.tick(30)

# Game loop
def gameloop():

    # Game Specific Varibles
    exit_game = False
    game_over = False
    snake_x = 55
    snake_y = 45
    velocity_x = 0
    velocity_y = 0
    initial_velocity = 5
    food_x = random.randint(20, screen_width / 2)
    food_y = random.randint(20, screen_height / 2)
    score = 0
    snake_size = 10
    fps = 30
    # Check if the highscore file exits if not handle it
    if (not os.path.exists("highscore.txt")):
        with open("highscore.txt","w") as f:
            f.write(str(0))
    with open("highscore.txt", "r") as f:
        high_score = f.read()

    snake_list = []
    snake_length = 1

    while not exit_game:
        if game_over:
            gameWindow.fill(white)
            with open("highscore.txt", "w") as f:
                f.write(str(high_score))
            screen_text("Game Over.Press Enter to continue!!", red, 100, 200)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = initial_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = - initial_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y = - initial_velocity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = initial_velocity
                        velocity_x = 0

                    # chit code
                    if event.key == pygame.K_q:
                        score = score + 10

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x - food_x)<8 and abs(snake_y - food_y)<8:
                score = score + 10
                food_x = random.randint(20, screen_width / 2)
                food_y = random.randint(20, screen_height / 2)
                snake_length = snake_length + 3
                if score > int(high_score):
                    high_score = score

            gameWindow.fill(white)
            gameWindow.blit(back_image,(0,0))
            screen_text("Score:" + str(score) + "  High Score:" + str(high_score), red, 5, 5)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)

            if len(snake_list)>snake_length:
                del snake_list[0]

            if head in snake_list[:-1]:
                game_over = True
                pygame.mixer.music.load('Game_over.mp3')
                pygame.mixer.music.play()

            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True
                pygame.mixer.music.load('Game_over.mp3')
                pygame.mixer.music.play()

            plot_snake(gameWindow,black,snake_list,snake_size)
        pygame.display.update()
        clock.tick(fps)


    pygame.quit()
    quit()
# gameloop()
welcome()