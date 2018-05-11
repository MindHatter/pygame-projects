import pygame
import time
import random

# Colors
BACK = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
TEXT = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
BLOCK = (random.randint(0,255), random.randint(0,255), random.randint(0,255))

surf_w = 800
surf_h = 400

pygame.init()
surface = pygame.display.set_mode((surf_w, surf_h))
pygame.display.set_caption("FlappyCopter")
clock = pygame.time.Clock()
img = pygame.image.load('img/helicopter.png')

def block(x_b, y_b, b_w, b_h, gap):
    pygame.draw.rect(surface, BLOCK, [x_b, y_b, b_w, b_h])
    pygame.draw.rect(surface, BLOCK, [x_b, y_b+b_h+gap, b_w, surf_h-b_h-gap])

def replay_or_quit():
    for event in pygame.event.get([pygame.KEYDOWN, pygame.KEYUP, pygame.QUIT]):
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        elif event.type == pygame.KEYDOWN:
            continue

        return event.key
    return None

def score(count):
    sm_txt = pygame.font.Font('fonts/pixel.ttf', 20)
    txt_surf = sm_txt.render("Score: "+str(count), True, TEXT)
    surface.blit(txt_surf, (0,0))

def mk_txt_obj(txt, font):
    txt_surf = font.render(txt, True, TEXT)
    return txt_surf, txt_surf.get_rect()

def msg_surf(txt):
    sm_txt = pygame.font.Font('fonts/pixel.ttf', 20)
    lg_txt = pygame.font.Font('fonts/pixel.ttf', 100)
    ttl_txt_surf, ttl_txt_rect = mk_txt_obj(txt, lg_txt)
    ttl_txt_rect.center = surf_w // 2, surf_h // 2
    surface.blit(ttl_txt_surf, ttl_txt_rect)

    tp_txt_surf, tp_txt_rect = mk_txt_obj('Press any key to continue', sm_txt)
    tp_txt_rect.center = surf_w // 2, surf_h // 2 + 100
    surface.blit(tp_txt_surf, tp_txt_rect)

    pygame.display.update()
    time.sleep(1)

    while replay_or_quit() is None:
        clock.tick()

    main()

def game_over_func():
    msg_surf('BOOM!')


def helicopter(x, y, img):
    surface.blit(img, (x, y))

def main():
    global BACK
    global TEXT
    global BLOCK

    x = 150
    y = 200
    y_move = 5
    game_over = False

    gap = 150
    x_b = surf_w
    y_b = 0
    b_w = 75
    b_h = random.randint(0, surf_h-gap)
    block_move = 3
    count = 0

    difficult = 0
    pygame.mixer.music.load('sfx/'+str(random.randint(1, 4))+'.wav')
    pygame.mixer.music.play()
    heli = pygame.mixer.Sound('sfx/helicopter.wav')
    heli.set_volume(0.25)
    expl = pygame.mixer.Sound('sfx/explosion.wav')

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                heli.stop()
                expl.play()
                game_over_func()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    y_move = -5
                    heli.play()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    y_move = 5
                    heli.stop()
                if event.key == pygame.K_ESCAPE:
                    game_over = True

        y += y_move

        pygame.display.update()
        surface.fill(BACK)
        helicopter(x, y, img)

        block(x_b, y_b, b_w, b_h, gap)
        x_b -= block_move

        if x_b <= 0-b_w:
            x_b = surf_w
            b_h = random.randint(0, surf_h-gap)
            count += 1
            if count % 5 == 0:
                if y_move <= 10:
                    y_move = abs(y_move)+1

                if b_w < 125:
                    b_w += 5

                if gap > 125:
                    gap -= 5

                if block_move < 15:
                    block_move += 3

            if count%10 == 0:
                pygame.mixer.music.load('sfx/'+str(random.randint(1, 4))+'.wav')
                pygame.mixer.music.play()
                BACK = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
                TEXT = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
                BLOCK = (random.randint(0,255), random.randint(0,255), random.randint(0,255))

            if count > 25:
                b_h_m = random.choice([3, -3])

        if count > 25:
            if b_h > surf_h-gap-5:
                b_h_m = -3
            if b_h < 5:
                b_h_m = 3
            b_h += b_h_m

        if y > surf_h-50 or y < 0:
            expl.play()
            game_over_func()

        score(count)

        if x_b-50 < x <x_b+b_w:
            if y < b_h or y > b_h + gap - 50:
                heli.stop()
                expl.play()
                game_over_func()

        clock.tick(60)

main()
pygame.quit()
quit()
