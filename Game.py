import cv2
import mediapipe as mp
import pygame
import sys
import random
import time
from pygame.locals import *

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils


pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("CV Space Invaders ")

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

spaceship_image = pygame.image.load('ship.png')
spaceship_image = pygame.transform.scale(spaceship_image, (50, 50))
alien_image = pygame.image.load('alien.png')
alien_image = pygame.transform.scale(alien_image, (45, 45))
fast_alien_image = pygame.image.load('fast_alien.jpg')
fast_alien_image = pygame.transform.scale(fast_alien_image, (45, 45))
strong_alien_image = pygame.image.load('strong_alien.jpg')
strong_alien_image = pygame.transform.scale(strong_alien_image, (45, 45))
shooting_alien_image = pygame.image.load('shooting_alien.jpg')
shooting_alien_image = pygame.transform.scale(shooting_alien_image, (45, 45))
boss_alien_image = pygame.image.load('boss_alien.jpg')
boss_alien_image = pygame.transform.scale(boss_alien_image, (90, 90))
shield_image = pygame.image.load('shield.jpg')
shield_image = pygame.transform.scale(shield_image, (30, 30))
health_pack_image = pygame.image.load('health_pack.jpg')
health_pack_image = pygame.transform.scale(health_pack_image, (30, 30))
double_bullet_image = pygame.image.load('double_bullet.jpg')
double_bullet_image = pygame.transform.scale(double_bullet_image, (30, 30))
spread_bullet_image = pygame.image.load('spread_bullet.jpg')
spread_bullet_image = pygame.transform.scale(spread_bullet_image, (30, 30))


player_size = 50
player_pos = [screen_width // 2, screen_height - 2 * player_size]

bullet_size = 7
bullet_speed = 10
bullet_type = 'single'  # Types: 'single', 'double', 'spread'

alien_size = 45
alien_speed = 5
fast_alien_speed = 10
strong_alien_hits = 2
boss_alien_hits = 3
alien_bullet_speed = 7

power_up_size = 30
power_up_speed = 5

player_health = 3
shield_active = False
shield_duration = 5
shield_start_time = 0

ADDALIEN = pygame.USEREVENT + 1
pygame.time.set_timer(ADDALIEN, 1000)

ADDPOWERUP = pygame.USEREVENT + 2
pygame.time.set_timer(ADDPOWERUP, 10000)

clock = pygame.time.Clock()
fps = 30

cap = cv2.VideoCapture(0)

font = pygame.font.SysFont("monospace", 35)

high_score_file = "high_score.txt"

def detect_hand_position(image):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    result = hands.process(image_rgb)
    hand_landmarks = result.multi_hand_landmarks
    if hand_landmarks:
        for handLms in hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                if id == 9:  # Index finger tip
                    return cx, cy
    return None

def load_high_score():
    try:
        with open(high_score_file, "r") as file:
            return int(file.read().strip())
    except (FileNotFoundError, ValueError):
        return 0

def save_high_score(score):
    high_score = load_high_score()
    if score > high_score:
        with open(high_score_file, "w") as file:
            file.write(str(score))

def game_loop():
    global shield_active, shield_start_time, bullet_type
    running = True
    bullets = []
    aliens = []
    alien_bullets = []
    power_ups = []
    last_bullet_time = time.time()
    score = 0
    health = player_health

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == ADDALIEN:
                alien_type = random.choice(['normal', 'fast', 'strong', 'shooting', 'boss'])
                alien_x = random.randint(0, screen_width - alien_size)
                alien_y = 0
                alien_hits = strong_alien_hits if alien_type == 'strong' else (boss_alien_hits if alien_type == 'boss' else 1)
                aliens.append([alien_x, alien_y, alien_type, alien_hits])
            elif event.type == ADDPOWERUP:
                power_up_type = random.choice(['shield', 'health', 'double_bullet', 'spread_bullet'])
                power_up_x = random.randint(0, screen_width - power_up_size)
                power_up_y = 0
                power_ups.append([power_up_x, power_up_y, power_up_type])

        ret, frame = cap.read()
        if not ret:
            break

        hand_pos = detect_hand_position(frame)
        if hand_pos:
            hand_x, hand_y = hand_pos
            player_pos[0] = screen_width - (hand_x * screen_width // cap.get(cv2.CAP_PROP_FRAME_WIDTH))

        current_time = time.time()
        if (current_time - last_bullet_time > 1):  # Fixed firing rate
            if bullet_type == 'single':
                bullets.append([player_pos[0] + player_size // 2, player_pos[1]])
            elif bullet_type == 'double':
                bullets.append([player_pos[0] + player_size // 4, player_pos[1]])
                bullets.append([player_pos[0] + 3 * player_size // 4, player_pos[1]])
            elif bullet_type == 'spread':
                bullets.append([player_pos[0] + player_size // 2, player_pos[1]])
                bullets.append([player_pos[0] + player_size // 2 - 10, player_pos[1] - 5])
                bullets.append([player_pos[0] + player_size // 2 + 10, player_pos[1] - 5])
            last_bullet_time = current_time

        bullets = [[b[0], b[1] - bullet_speed] for b in bullets if b[1] > 0]

        for alien in aliens:
            if alien[2] == 'normal':
                alien[1] += alien_speed
            elif alien[2] == 'fast':
                alien[1] += fast_alien_speed
            elif alien[2] == 'strong' or alien[2] == 'boss':
                alien[1] += alien_speed
            elif alien[2] == 'shooting':
                alien[1] += alien_speed
                if random.randint(0, 100) < 5:
                    alien_bullets.append([alien[0] + alien_size // 2, alien[1] + alien_size])

        aliens = [a for a in aliens if a[1] < screen_height]

        alien_bullets = [[b[0], b[1] + alien_bullet_speed] for b in alien_bullets if b[1] < screen_height]

        for power_up in power_ups:
            power_up[1] += power_up_speed
        power_ups = [p for p in power_ups if p[1] < screen_height]

        for bullet in bullets:
            for alien in aliens:
                if (alien[0] < bullet[0] < alien[0] + alien_size and
                        alien[1] < bullet[1] < alien[1] + alien_size):
                    bullets.remove(bullet)
                    alien[3] -= 1  # Decrease hit points for strong and boss aliens
                    if alien[3] == 0:
                        aliens.remove(alien)
                        score += 10 if alien[2] != 'boss' else 100
                    break

        for alien in aliens:
            if (player_pos[0] < alien[0] < player_pos[0] + player_size or
                    player_pos[0] < alien[0] + alien_size < player_pos[0] + player_size) and \
                    (player_pos[1] < alien[1] < player_pos[1] + player_size or
                     player_pos[1] < alien[1] + alien_size < player_pos[1] + player_size):
                if not shield_active:
                    health -= 1
                    aliens.remove(alien)
                    if health == 0:
                        running = False
                else:
                    aliens.remove(alien)
                break

        for bullet in alien_bullets:
            if (player_pos[0] < bullet[0] < player_pos[0] + player_size and
                player_pos[1] < bullet[1] < player_pos[1] + player_size):
                if not shield_active:
                    health -= 1
                    alien_bullets.remove(bullet)
                    if health == 0:
                        running = False
                else:
                    alien_bullets.remove(bullet)
                break

        for power_up in power_ups:
            if (player_pos[0] < power_up[0] < player_pos[0] + player_size or
                    player_pos[0] < power_up[0] + power_up_size < player_pos[0] + player_size) and \
                    (player_pos[1] < power_up[1] < player_pos[1] + player_size or
                     player_pos[1] < power_up[1] + power_up_size < player_pos[1] + player_size):
                if power_up[2] == 'shield':
                    shield_active = True
                    shield_start_time = current_time
                elif power_up[2] == 'health':
                    health = min(player_health, health + 1)
                elif power_up[2] == 'double_bullet':
                    bullet_type = 'double'
                elif power_up[2] == 'spread_bullet':
                    bullet_type = 'spread'
                power_ups.remove(power_up)

        if shield_active and current_time - shield_start_time > shield_duration:
            shield_active = False

        screen.fill(black)
        screen.blit(spaceship_image, (player_pos[0], player_pos[1]))

        for bullet in bullets:
            pygame.draw.rect(screen, red, (bullet[0], bullet[1], bullet_size, bullet_size))

        for alien in aliens:
            if alien[2] == 'normal':
                screen.blit(alien_image, (alien[0], alien[1]))
            elif alien[2] == 'fast':
                screen.blit(fast_alien_image, (alien[0], alien[1]))
            elif alien[2] == 'strong':
                screen.blit(strong_alien_image, (alien[0], alien[1]))
            elif alien[2] == 'shooting':
                screen.blit(shooting_alien_image, (alien[0], alien[1]))
            elif alien[2] == 'boss':
                screen.blit(boss_alien_image, (alien[0], alien[1]))

        for bullet in alien_bullets:
            pygame.draw.rect(screen, yellow, (bullet[0], bullet[1], bullet_size, bullet_size))

        for power_up in power_ups:
            if power_up[2] == 'shield':
                screen.blit(shield_image, (power_up[0], power_up[1]))
            elif power_up[2] == 'health':
                screen.blit(health_pack_image, (power_up[0], power_up[1]))
            elif power_up[2] == 'double_bullet':
                screen.blit(double_bullet_image, (power_up[0], power_up[1]))
            elif power_up[2] == 'spread_bullet':
                screen.blit(spread_bullet_image, (power_up[0], power_up[1]))

        # Render score and health
        score_text = font.render(f"Score: {score}", True, white)
        health_text = font.render(f"Health: {health}", True, green)
        screen.blit(score_text, (screen_width - score_text.get_width() - 10, 10))
        screen.blit(health_text, (10, 10))

        pygame.display.flip()
        clock.tick(fps)

    save_high_score(score)
    show_game_over(score)

def show_game_over(score):
    high_score = load_high_score()
    game_over = True
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:  # Press Y to play again
                    game_loop()
                elif event.key == pygame.K_n:  # Press N to quit
                    pygame.quit()
                    sys.exit()

        screen.fill(black)
        game_over_text = font.render("Game Over", True, white)
        score_text = font.render(f"Score: {score}", True, white)
        high_score_text = font.render(f"High Score: {high_score}", True, white)
        play_again_text = font.render("Play again? Y/N", True, white)

        screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 4))
        screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 2))
        screen.blit(high_score_text, (screen_width // 2 - high_score_text.get_width() // 2, screen_height * 3 // 4))
        screen.blit(play_again_text, (screen_width // 2 - play_again_text.get_width() // 2, screen_height * 7 // 8))

        pygame.display.flip()

if __name__ == "__main__":
    game_loop()
    cap.release()
    cv2.destroyAllWindows()
    pygame.quit()
    sys.exit()
