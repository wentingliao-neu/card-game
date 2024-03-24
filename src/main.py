# -*- coding: utf-8 -*-
import pygame
from character import Character

pygame.init()
pygame.font.init()

from bag import *
from pygame.locals import *
from dialogs import Dialog
from fight_main import *
from settings import *
import maze

name_of_boss = ['WKX', 'XYJ', 'KKX']


class Condition:

    def __init__(self):
        self.back = pygame.image.load('../assets/icons/per_sit0.png').convert()
        self.font = pygame.font.Font('../assets/icons/CaslonAntique.ttf', 28)
        self.sur = pygame.Surface(self.back.get_size())

    def condition(self, player):
        self.sur.blit(self.back, (0, 0))
        text_sur0 = self.font.render(str(player.name), True, (0, 0, 0))
        self.sur.blit(text_sur0, (160, 15))
        text_sur1 = self.font.render(str(player.atk), True, (0, 0, 0))
        self.sur.blit(text_sur1, (185, 40))
        text_sur2 = self.font.render(str(player.defe), True, (0, 0, 0))
        self.sur.blit(text_sur2, (256, 40))
        text_sur3 = self.font.render(str(player.current_HP), True, (0, 0, 0))
        self.sur.blit(text_sur3, (185, 76))
        text_sur4 = self.font.render(str(len(player.card_deck)), True,
                                     (0, 0, 0))
        self.sur.blit(text_sur4, (256, 76))
        return self.sur


class Start:

    def __init__(self):
        self.background = pygame.image.load('../assets/background/start0.jpg')
        self.surface = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        self.surface.blit(self.background, (0, 0))
        pygame.mixer.music.load('../assets/bgm/start.mp3')
        pygame.mixer.music.play(-1)

    def __del__(self):
        self.background = None
        self.surface = None

    def show(self):
        loop1 = True
        while loop1:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                if event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        sys.exit()
                    if event.key == K_RETURN:
                        pygame.mixer.music.stop()
                        loop1 = False
            pygame.display.update()


def check_events():
    key_events = [
        K_ESCAPE, K_LEFT, K_RIGHT, K_UP, K_DOWN, K_SPACE, K_LSHIFT, K_TAB
    ]
    res = [False] * 8
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            res[0] = True
        elif event.type == KEYUP:
            res = [key_event == event.key for key_event in key_events]
    return res


def level_manager(num, player):
    bgm = pygame.mixer.Sound(f'../assets/bgm/stage{num}.mp3')
    bgm.play(-1)
    c = Condition()
    dead_time = 0
    boss_dead_time = 0
    drawer = maze.DrawMaze(num)
    d = Dialog(num, 1)
    player.infected(d[0])
    del d
    drawer.display()
    is_moving = False
    frame_num = 0
    p = 0
    frame_start = -33
    clock = pygame.time.Clock()
    boss = Character(name_of_boss[num - 1], num)

    while True:
        clock.tick(64)
        q, l, r, u, d, e, re, b = check_events()
        if q:
            sys.exit()
        if not player.dead:
            [_, p] = player.check_dire(drawer.maze, u, l, r, d, is_moving, p)
            [is_moving, p] = player.move(p)
            if e:
                frame_start = frame_num
                dead_time, boss_dead_time = player.attack(drawer)
            else:
                e = True if frame_num - frame_start <= 32 else False

            if b:
                bag = Bag(player)
                bag.show_main()
                del bag
        else:
            if re:
                player.dead = False
                player.current_HP = player.total_HP
                dead_time = 0

        drawer.display()
        player.draw_self(drawer.screen, frame_num, is_moving, e, dead_time)
        boss.draw_self(drawer.screen, frame_num, False, False, boss_dead_time)

        drawer.screen.blit(c.condition(player), (950, 50))

        pygame.display.update()
        frame_num += 1

        if player.block == [COL - 1, ROW - 1] and not is_moving and r:
            d = Dialog(num, 4)
            player.infected(d[0])
            del d
            player.reset()
            drawer.screen.fill((0, 0, 0))

            del drawer
            bgm.fadeout(1000)
            pygame.time.delay(3000)
            player.total_HP += 10
            player.ori_atk += 3
            player.ori_defe += 2
            player.battle_end()

            return player


def main():
    pygame.mixer.init()
    pygame.display.set_caption('The Road to Villain')
    pygame.display.set_icon(pygame.image.load("../assets/icons/sword.ico"))

    while True:
        s = Start()
        s.show()
        player = Character('Yi', 0)  # 初始化玩家
        player = level_manager(1, player)
        player = level_manager(2, player)
        player = level_manager(3, player)

        if len(player.keys) == 11:
            fmthm = pygame.mixer.Sound('../assets/bgm/hide.mp3')
            fmthm.play(-1)
            Dialog(0, 1)
            fmthm.stop()
        else:
            Dialog(0, 2)
        del player


if __name__ == '__main__':
    main()
