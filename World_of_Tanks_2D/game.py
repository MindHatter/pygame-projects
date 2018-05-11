import pygame
import random
import time

pygame.init()
pygame.mixer.init()

surf_w = 800
surf_h = 600
surface = pygame.display.set_mode((surf_w, surf_h))
pygame.display.set_caption("Tanks")
clock = pygame.time.Clock()

class Bullet:
    def __init__(self, x, y):
        self.bu = pygame.image.load('img/bul_up.png')
        self.bd = pygame.image.load('img/bul_down.png')
        self.bl = pygame.image.load('img/bul_left.png')
        self.br = pygame.image.load('img/bul_right.png')
        self.x = x
        self.y = y
        self.x_move = 0
        self.y_move = 0


class Tank():
    def __init__(self, name, x, y):
        self.name = name
        self.hp = 3
        self.tu = pygame.image.load('img/'+self.name+'_up.png')
        self.td = pygame.image.load('img/'+self.name+'_down.png')
        self.tl = pygame.image.load('img/'+self.name+'_left.png')
        self.tr = pygame.image.load('img/'+self.name+'_right.png')
        self.x = x
        self.y = y
        self.x_move = 0
        self.y_move = 0


def lives(p_lives, e_lives):
    sm_txt = pygame.font.Font('fonts/pixel.ttf', 20)
    txt_surf = sm_txt.render("HP: "+str(p_lives), True, (255,0,0))
    surface.blit(txt_surf, (0,0))

    sm_txt = pygame.font.Font('fonts/pixel.ttf', 20)
    txt_surf = sm_txt.render("HP: "+str(e_lives), True, (255,0,0))
    surface.blit(txt_surf, (surf_w-100,0))

def replay_or_quit():
    for event in pygame.event.get([pygame.KEYDOWN, pygame.KEYUP, pygame.QUIT]):
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        elif event.type == pygame.KEYDOWN:
            continue

        return event.key
    return None

def mk_txt_obj(txt, font):
    txt_surf = font.render(txt, True, (255,0,0))
    return txt_surf, txt_surf.get_rect()

def game_over():
    sm_txt = pygame.font.Font('fonts/pixel.ttf', 20)
    lg_txt = pygame.font.Font('fonts/pixel.ttf', 80)
    ttl_txt_surf, ttl_txt_rect = mk_txt_obj('GAME OVER', lg_txt)
    ttl_txt_rect.center = surf_w // 2, surf_h // 2
    surface.blit(ttl_txt_surf, ttl_txt_rect)

    tp_txt_surf, tp_txt_rect = mk_txt_obj('Press any key to continue', sm_txt)
    tp_txt_rect.center = surf_w // 2, surf_h // 2 + 100
    surface.blit(tp_txt_surf, tp_txt_rect)

    pygame.display.update()
    time.sleep(2)

    while replay_or_quit() is None:
        clock.tick()

    main()

def main():
    houses = {str(i): [pygame.image.load('img/House0'+str(i)+'.png'), random.randint(i*200-200,i*200), random.randint(i*150-150,i*150)] for i in range(1,4)}
    craters = {str(i): [pygame.image.load('img/cr'+str(i)+'.png'), random.randint(0, surf_w), random.randint(0, surf_h)] for i in range(1,6)}
    player = Tank('player', 20, surf_h-148)
    enemy = Tank('enemy', surf_w-148, 20)
    player_turn = player.tr
    enemy_turn = enemy.tl

    enemy_bullet = Bullet(-50, -50)
    player_bullet = Bullet(-50, -50)
    enemy_bullet_turn = enemy_bullet.bl
    player_bullet_turn = player_bullet.br
    background = pygame.image.load('img/surface.jpg')

    game = True

    pygame.mixer.music.load(random.choice(['sfx/pustinya.wav','sfx/naiti.wav','sfx/ulica.wav']))
    pygame.mixer.music.play()

    enemy_shot = pygame.mixer.Sound('sfx/enemy_shot.wav')
    player_shot = pygame.mixer.Sound('sfx/player_shot.wav')
    gusenica = pygame.mixer.Sound('sfx/gusenica.wav')

    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False

            if event.type == pygame.KEYDOWN:

                # yellow tank calc move
                if event.key == pygame.K_UP:
                    enemy_turn = enemy.tu
                    enemy.y_move = -2
                    gusenica.play()

                if event.key == pygame.K_DOWN:
                    enemy_turn = enemy.td
                    enemy.y_move = 2
                    gusenica.play()

                if event.key == pygame.K_LEFT:
                    enemy_turn = enemy.tl
                    enemy.x_move = -2
                    gusenica.play()

                if event.key == pygame.K_RIGHT:
                    enemy_turn = enemy.tr
                    enemy.x_move = 2
                    gusenica.play()

                # green tank calc move
                if event.key == pygame.K_w:
                    player_turn = player.tu
                    player.y_move = -2
                    gusenica.play()

                if event.key == pygame.K_s:
                    player_turn = player.td
                    player.y_move = 2
                    gusenica.play()

                if event.key == pygame.K_a:
                    player_turn = player.tl
                    player.x_move = -2
                    gusenica.play()

                if event.key == pygame.K_d:
                    player_turn = player.tr
                    player.x_move = 2
                    gusenica.play()

                # yellow tank calc shot
                if event.key == pygame.K_RSHIFT:
                    if enemy_turn == enemy.tu:
                        enemy_bullet.x, enemy_bullet.y = enemy.x+46, enemy.y
                        enemy_bullet_turn = enemy_bullet.bu
                        enemy_bullet.y_move, enemy_bullet.x_move = -5, 0

                    if enemy_turn == enemy.td:
                        enemy_bullet.x, enemy_bullet.y = enemy.x+46, enemy.y+108
                        enemy_bullet_turn = enemy_bullet.bd
                        enemy_bullet.y_move, enemy_bullet.x_move = 5, 0

                    if enemy_turn == enemy.tl:
                        enemy_bullet.x, enemy_bullet.y = enemy.x, enemy.y+32
                        enemy_bullet_turn = enemy_bullet.bl
                        enemy_bullet.x_move, enemy_bullet.y_move = -5, 0

                    if enemy_turn == enemy.tr:
                        enemy_bullet.x, enemy_bullet.y = enemy.x+108, enemy.y+32
                        enemy_bullet_turn = enemy_bullet.br
                        enemy_bullet.x_move, enemy_bullet.y_move = 5, 0

                    enemy_shot.play()

                # green tank calc shot
                if event.key == pygame.K_LSHIFT:
                    if player_turn == player.tu:
                        player_bullet.x, player_bullet.y = player.x+46, player.y
                        player_bullet_turn = player_bullet.bu
                        player_bullet.y_move, player_bullet.x_move = -5, 0

                    if player_turn == player.td:
                        player_bullet.x, player_bullet.y = player.x+46, player.y+108
                        player_bullet_turn = player_bullet.bd
                        player_bullet.y_move, player_bullet.x_move = 5, 0

                    if player_turn == player.tl:
                        player_bullet.x, player_bullet.y = player.x, player.y+32
                        player_bullet_turn = player_bullet.bl
                        player_bullet.x_move, player_bullet.y_move = -5, 0

                    if player_turn == player.tr:
                        player_bullet.x, player_bullet.y = player.x+108, player.y+32
                        player_bullet_turn = player_bullet.br
                        player_bullet.x_move, player_bullet.y_move = 5, 0

                    player_shot.play()

            # stop move
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    game = False

                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    enemy.y_move = 0
                    gusenica.stop()
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    enemy.x_move = 0
                    gusenica.stop()

                if event.key == pygame.K_w or event.key == pygame.K_s:
                    player.y_move = 0
                    gusenica.stop()
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    player.x_move = 0
                    gusenica.stop()

        for i in player, enemy:
            # bound on window side
            if i.x < -30: i.x = -30
            if i.x > surf_w - 98: i.x = surf_w - 98
            if i.y < -30: i.y = -30
            if i.y > surf_h - 98: i.y = surf_h - 98

            # bound with houses
            for h in houses.values():
                if h[1]-98<i.x<h[1]+132 and h[2]<i.y<h[2]+132:
                    i.x -= i.x_move
                    i.x_move = 0
                    i.y -= i.y_move
                    i.y_move = 0

        for i in player_bullet, enemy_bullet:
            if i.x < -30 or i.x > surf_w:
                i.x = -50
            if i.y < -30 or i.y > surf_h:
                i.y = -50

            for h in houses.values():
                if h[1]-32<i.x<h[1]+162 and h[2]+32<i.y<h[2]+162:
                    i.x = -50
                    i.x_move = 0
                    i.y = -50
                    i.y_move = 0

        # damage
        if enemy.x+20 < player_bullet.x < enemy.x+108 and enemy.y+20 < player_bullet.y < enemy.y+108:
            enemy.hp -= 1
            player_bullet.x = -50
            player_bullet.x_move = 0
            player_bullet.y = -50
            player_bullet.y_move = 0

        if player.x+20 < enemy_bullet.x < player.x+108 and player.y+20 < enemy_bullet.y < player.y+108:
            player.hp -= 1
            enemy_bullet.x = -50
            enemy_bullet.x_move = 0
            enemy_bullet.y = -50
            enemy_bullet.y_move = 0

        lives(player.hp, enemy.hp)

        if player.hp == 0 or enemy.hp == 0:
            game_over()

        # tank move
        enemy.x += enemy.x_move
        enemy.y += enemy.y_move
        player.x += player.x_move
        player.y += player.y_move

        # bullet move
        enemy_bullet.x += enemy_bullet.x_move
        enemy_bullet.y += enemy_bullet.y_move
        player_bullet.x += player_bullet.x_move
        player_bullet.y += player_bullet.y_move

        pygame.display.update()
        surface.blit(background, (0, 0))
        for v in craters.values():
            surface.blit(v[0], (v[1], v[2]))
        surface.blit(player_turn, (player.x, player.y))
        surface.blit(enemy_turn, (enemy.x, enemy.y))
        surface.blit(enemy_bullet_turn, (enemy_bullet.x, enemy_bullet.y))
        surface.blit(player_bullet_turn, (player_bullet.x, player_bullet.y))
        for v in houses.values():
            surface.blit(v[0], (v[1], v[2]))

        clock.tick(60)

if __name__ == "__main__":
    main()
    pygame.quit()
    quit()
