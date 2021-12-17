import random

import pygame

from pong.const import WIDTH, HEIGHT, FPS
from pong.colors import BLACK, WHITE, RED, GRAY
from pong.menu import MenuItem, MenuCursor
from pong.player import Player
from pong.ball import Ball
from pong.sound import hit_sound, goal_sound, rebound_sound


def reset_positions(ball, player1, player2):
    ball.rect.center = (WIDTH / 2, HEIGHT / 2)
    ball.dy = random.uniform(-1.5, 1.5)
    ball.speed = 5
    player1.reset_position()
    player2.reset_position()


def draw_field(screen, player1_score, player2_score):
    for i in range(0, HEIGHT, 10):
        pygame.draw.line(screen, WHITE, [WIDTH / 2, i], [WIDTH / 2, i + 6], 1)
    font = pygame.font.SysFont('Comic Sans MS', 56)
    score_text = font.render(f'{player1_score}     {player2_score}', False, WHITE)
    score = score_text.get_rect()
    score.center = (WIDTH / 2, 40)
    screen.blit(score_text, score)


def paused(screen):
    clock = pygame.time.Clock()

    blur = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    blur.fill((0, 0, 0, 190))
    screen.blit(blur, (0, 0))

    font = pygame.font.SysFont('Comic Sans MS', 56)
    score_text = font.render('Paused', False, WHITE)
    score = score_text.get_rect()
    score.center = (WIDTH / 2, HEIGHT / 2)
    screen.blit(score_text, score)

    menu_resume = MenuItem(name='Resume', position=1)
    menu_exit = MenuItem(name='Exit', position=2)
    full_screen = MenuItem(name='Full screen', position=3)
    menu_items = pygame.sprite.Group(menu_resume, menu_exit, full_screen)

    cursor = MenuCursor(menu_elements=(menu_resume, menu_exit, full_screen))

    all_sprites = pygame.sprite.Group()
    all_sprites.add(menu_resume, menu_exit, full_screen, cursor)
    # menu_font = pygame.font.SysFont('Comic Sans MS', 42)
    # menu_resume_text = menu_font.render('Resume', False, (200, 200, 200))
    # menu_resume = menu_resume_text.get_rect()
    # menu_resume.center = (WIDTH / 2, HEIGHT / 2 + 50)
    # screen.blit(menu_resume_text, menu_resume)
    # menu_exit_text = menu_font.render('Exit', False, (200, 200, 200))
    # menu_exit = menu_exit_text.get_rect()
    # menu_exit.center = (WIDTH / 2, HEIGHT / 2 + 100)
    # screen.blit(menu_exit_text, menu_exit)

    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    rebound_sound.play()
                    pause = False
                cursor.navigate(event)

                for sprite in menu_items:
                    sprite.rerender(GRAY)

                collide = pygame.sprite.spritecollideany(cursor, menu_items)
                if collide:
                    rebound_sound.play()
                    collide.rerender(WHITE)

                if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    rebound_sound.play()
                    if collide is menu_exit:
                        pygame.quit()
                        quit()
                    if collide is menu_resume:
                        pause = False
                    if collide is full_screen:
                        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

        all_sprites.update()
        all_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(30)


def main_loop():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("pong")
    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    player1 = Player(playable=True, left_side=True)
    # player1 = Player(left_side=True)
    player2 = Player()
    ball = Ball()

    all_sprites.add(player1, player2, ball)
    players = pygame.sprite.Group(player1, player2)

    vectors = {
        15: {'speed': 7.5, 'angle': 1.5},
        35: {'speed': 5, 'angle': 1},
        # 50: {'speed': 3.5, 'angle': 0},
        55: {'speed': 5, 'angle': 1},
        75: {'speed': 7.5, 'angle': 1.5}
    }

    keys = [pygame.K_UP, pygame.K_DOWN]

    if pygame.joystick.get_count():
        gamepad = pygame.joystick.Joystick(0)
        gamepad.init()

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_SPACE):
                    rebound_sound.play()
                    paused(screen)

        # collide for ball
        # for player in players:
        #     if pygame.sprite.collide_mask(ball, player):
        #         print(player)

        # if pygame.key.get_pressed()[pygame.K_SPACE]:
        #     print('here')
        #     pause_handler()
        #     print('outer')

        collide = pygame.sprite.spritecollideany(ball, players)
        if collide:
            hit_sound.play()
            clip = collide.rect.clip(ball.rect)
            collide_point = collide.rect.y + collide.rect.height - clip.y
            ball.dx = ball.dx * -1
            sign = -1 if ball.dy < 0 else 1

            for vector in vectors:
                speed_mod = 0
                if list(key for key in keys if pygame.key.get_pressed()[key]):
                    speed_mod = 2
                if collide_point <= vector:
                    ball.dy = vectors.get(vector).get('angle') * sign
                    ball.speed = vectors.get(vector).get('speed') + speed_mod
                    break

            if ball.rect.x > WIDTH / 2:
                ball.rect.x = player2.rect.x - ball.rect.width
            else:
                ball.rect.x = player1.rect.x + player1.rect.width + ball.rect.width

        if ball.rect.right >= WIDTH:
            player1.score += 1
            reset_positions(ball, player1, player2)
            goal_sound.play()
        if ball.rect.left <= 0:
            player2.score += 1
            reset_positions(ball, player1, player2)
            goal_sound.play()

        player1.bot_1(ball.rect.center, ball.direction())
        player2.bot_1(ball.rect.center, ball.direction())
        # player2.bot_2(ball.rect.center)

        all_sprites.update()
        screen.fill(BLACK)
        all_sprites.draw(screen)
        draw_field(screen, player1.score, player2.score)
        pygame.display.flip()

    pygame.quit()
    quit()

# Если мяч попадает в лопатку прямо в центре, он удаляется точно горизонтально; если он ударяет прямо по краю, он
# улетает под крайним углом (75 градусов). И он всегда путешествует с постоянной скоростью.
