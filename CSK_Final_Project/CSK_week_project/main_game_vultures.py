import random

import pygame
from sys import exit

GAME_WIDTH = 672.5
GAME_HEIGHT = 900

pygame.init()

window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("CSK Flappy Bird")
clock = pygame.time.Clock()

# bird
bird_x = GAME_WIDTH/8
bird_y = GAME_HEIGHT/2
bird_width = 80
bird_height = 80

class Bird(pygame.Rect):
    def __init__(self, img):
        pygame.Rect.__init__(self, bird_x, bird_y, bird_width, bird_height)
        self.img = img

#cloud obstacles
cloud_x = GAME_WIDTH
cloud_y = 0
cloud_width, vulture_width = 300, 200
cloud_height, vulture_height = 300, 150
top_cloud_image = pygame.image.load("assets/top_obstacle.png")
top_cloud_image = pygame.transform.scale(top_cloud_image, (cloud_width, cloud_height))
bottom_cloud_image = pygame.image.load("assets/bottom_obstacle.png")
bottom_cloud_image = pygame.transform.scale(bottom_cloud_image, (cloud_width, cloud_height))


vulture_image = pygame.image.load("assets/vulture.png")
vulture_image = pygame.transform.scale(vulture_image, (vulture_width, vulture_height))
vulture2_image = pygame.image.load("assets/vulture2.png")
vulture2_image = pygame.transform.scale(vulture2_image, (vulture_width, vulture_height))


class Cloud(pygame.Rect):
    def __init__(self, img):
        pygame.Rect.__init__(self, cloud_x, cloud_y, cloud_width, cloud_height)
        self.img = img
        self.passed = False # check if bird passed

class Vulture(pygame.Rect):
    def __init__(self, img):
        pygame.Rect.__init__(self, cloud_x, cloud_y, vulture_width, vulture_height)
        self.img = img
        self.passed = False # check if bird passed

# loading images
bird_image = pygame.image.load("assets/character.png")
bird_image = pygame.transform.scale(bird_image, (bird_width, bird_height))

background_image = pygame.image.load("assets/background.png")

# game logic
bird = Bird(bird_image)
clouds = []
velocity_x = -3
velocity_y = 0
gravity = 0.6
score = 0 
game_over = False

def draw_images():
    window.blit(background_image, (0, 0))
    window.blit(bird_image, bird)

    for cloud in clouds:
        window.blit(cloud.img, cloud)
        pygame.draw.rect(window, (255, 0, 0), cloud, 2)

    text_content = str(int(score))

    if game_over:
        text_content = "Game Over! Score: " + text_content

    text_font = pygame.font.Font(None, 50)
    text_render = text_font.render(text_content, True, "black")
    window.blit(text_render, (10, 10))


def move():
    global velocity_y, score, game_over
    velocity_y += gravity
    bird.y += velocity_y
    bird.y = max(bird.y, -100)  # Prevent bird from going above the screen

    if bird.y > GAME_HEIGHT:
        game_over = True
        return

    for cloud in clouds:
        cloud.x += velocity_x

        if not cloud.passed and bird.left > cloud.right:
            score += 0.5  # Increment score by 0.5 for each cloud passed
            cloud.passed = True

        if bird.colliderect(cloud):
            game_over = True
            return

    while clouds and clouds[0].right < 0:
        clouds.pop(0)  # Remove the cloud that has moved off-screen, 

def create_clouds():
    if len(clouds) >= 2:
        last_pair_x = clouds[-1].x

        if last_pair_x > GAME_WIDTH - 350:
            return
    
    random_cloud_y = random.random()*(cloud_height/2) 
    random_vulture_y = random.random()*(vulture_height/2)
    opening_space = 250

    choose_top_obstacle = random.choice([top_cloud_image, vulture_image])
    if choose_top_obstacle == top_cloud_image:
        top_obstacle = Cloud(choose_top_obstacle)
        top_obstacle.y = random_cloud_y
        clouds.append(top_obstacle) 
    elif choose_top_obstacle == vulture_image:
        top_obstacle = Vulture(choose_top_obstacle)
        top_obstacle.y = random_vulture_y
        clouds.append(top_obstacle)

    choose_bottom_obstacle = random.choice([bottom_cloud_image, vulture2_image])
    if choose_bottom_obstacle == bottom_cloud_image:
        bottom_obstacle = Cloud(choose_bottom_obstacle)
        bottom_obstacle.y = top_obstacle.y + top_obstacle.height + opening_space 
        clouds.append(bottom_obstacle)
    elif choose_bottom_obstacle == vulture2_image:
        bottom_obstacle = Vulture(choose_bottom_obstacle)
        bottom_obstacle.y = top_obstacle.y + top_obstacle.height + opening_space
        clouds.append(bottom_obstacle)

    print(len(clouds))

create_clouds_timer = pygame.USEREVENT + 0
#spawn_time = max(600, 1500 - int(abs( velocity_x) * 80))
pygame.time.set_timer(create_clouds_timer, 1500)  # every 1 second new cloud

speed_of_game = pygame.USEREVENT + 1
pygame.time.set_timer(speed_of_game, 1000)  # every 1 second increase speed


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if len(clouds) == 0:
            create_clouds()

        else:
            last_pair = clouds[-1]

            if GAME_WIDTH - last_pair.right >= 250:
                create_clouds()

        if event.type == speed_of_game and not game_over:
            velocity_x -= 0.3  # Increase the speed of the game by decreasing the velocity_x

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                velocity_y = -10 # flap up

            #resetting the game
            if event.key == pygame.K_SPACE and game_over:
                pygame.time.wait(1000)
                bird.y = bird_y 
                clouds.clear()
                score = 0
                velocity_x = -3
                game_over = False

    if not game_over:
        move()
        draw_images()
        pygame.display.update()
        clock.tick(60)  # 60 FPS