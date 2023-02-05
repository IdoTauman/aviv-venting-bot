import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
score_font = pygame.font.Font('font/Pixeltype.ttf', 50)

score = 0
start_score = 0

snail_reps = 0

sky = pygame.image.load('graphics\Sky.png').convert()
ground = pygame.image.load('graphics\ground.png').convert()
player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()

snail1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_walk = [snail1,snail2]
snail_index = 0
snail_surf = snail_walk[snail_index]

player_surf = player_walk[player_index]
player_rect = player_walk_1.get_rect(midbottom = (80,300))
snail_rect = snail_surf.get_rect(midbottom = (600,300))
snail_hitbox = pygame.Rect(548, 264, 40, 36)

title_text = score_font.render('Click to play', False, 'White')
title_rect = title_text.get_rect(center = (400,200))


player_grav = 0
grav_timer = 0

best_score = 0

is_active = False

def display_score():
    score = pygame.time.get_ticks() // 100 - start_score // 100
    score_text = score_font.render(f'Score: {score}', False, 'Black')
    score_rect = score_text.get_rect(center=(300, 50))
    screen.blit(score_text, (score_rect))
    global best_score
    best_text = score_font.render(f'Best : {best_score}', False, 'Black')
    best_rect = best_text.get_rect(center=(500, 50))
    screen.blit(best_text, (best_rect))
    if score > best_score: best_score = score

def anim():
    global player_surf, player_index, snail_surf, snail_index

    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        player_surf = player_walk[int(player_index) % 2]
    snail_index += 0.1
    snail_surf = snail_walk[int(snail_index) % 2]

while True:
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if player_rect.bottom == 300: player_grav = -15

        if event.type == pygame.MOUSEBUTTONDOWN:
            if player_rect.collidepoint(event.pos):
                if player_rect.bottom == 300:
                    player_grav = -15


    clock.tick(60)

    anim()

    snail_hitbox.midbottom = snail_rect.midbottom

    screen.blit(sky, (0, 0))
    screen.blit(ground, (0, 300))

    if is_active:
        if snail_rect.left <= -100:
            snail_rect.left = 800
            snail_reps += 1
        else:
            snail_rect.left -= 4 + snail_reps/2.5
        screen.blit(snail_surf, snail_rect)
        screen.blit(player_surf, player_rect)

        mouse_pos = pygame.mouse.get_pos()
        if player_rect.collidepoint(mouse_pos):
            pygame.mouse.get_pressed()

        if snail_hitbox.colliderect(player_rect):
            is_active = False
            player_rect.bottom = 300
            snail_rect.midbottom = (600,300)

        player_rect.top += player_grav

        if player_rect.bottom < 300:
            grav_timer += 0.1
            player_grav += 0.75 * 1.01 ** grav_timer
        elif player_rect.bottom == 300:
            grav_timer = 0
            player_grav = 0
        else:
            grav_timer = 0
            player_grav = 0
            player_rect.bottom = 300

        display_score()


    else:
        screen.fill('black')
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN: is_active = True
            if event.type == pygame.QUIT: pygame.quit(); exit()
        start_score = pygame.time.get_ticks()
        player_grav = 0
        screen.blit(title_text,title_rect)
        snail_reps = 0
