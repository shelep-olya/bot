import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 400, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Уникай ворога!")

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

player_size = 50
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT - player_size - 10
player_speed = 20

enemy_size = 50
enemy_x = random.randint(0, WIDTH - enemy_size)
enemy_y = -enemy_size
enemy_speed = 5

clock = pygame.time.Clock()
# font = pygame.font.SysFont(None, 36)

def draw_window(score):
    WIN.fill(WHITE)
    pygame.draw.rect(WIN, GREEN, (player_x, player_y, player_size, player_size))
    pygame.draw.rect(WIN, RED, (enemy_x, enemy_y, enemy_size, enemy_size))
    # score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    # WIN.blit(score_text, (10, 10))
    pygame.display.update()

def main():
    global player_x, enemy_x, enemy_y, enemy_speed
    run = True
    score = 0

    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
            player_x += player_speed

        enemy_y += enemy_speed
        if enemy_y > HEIGHT:
            enemy_y = -enemy_size
            enemy_x = random.randint(0, WIDTH - enemy_size)
            score += 1
            enemy_speed += 1  

        if (
            player_y < enemy_y + enemy_size and
            player_y + player_size > enemy_y and
            player_x < enemy_x + enemy_size and
            player_x + player_size > enemy_x
        ):
            print(f"Game Over! Final Score: {score}")
            run = False

        draw_window(score)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
