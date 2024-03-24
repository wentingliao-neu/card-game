from character import *
import sys
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

hints = [
    'Use card to defeat enemies',
    'Powerful cards are guarded by enemies in the maze',
    'Be care of element relationship',
    'Different options may cause different results.',
    "Try to find extra content!"
]


def bag_check_events(funcs):
    status = [False] * 4
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_position = event.pos
                status[0] = 967 < mouse_position[
                    0] < 1007 and 124 < mouse_position[
                        1] < 164  # red cross button
                if funcs:
                    status[1:] = [
                        func.collidepoint(mouse_position[0], mouse_position[1])
                        for func in funcs
                    ]
    return status


class Bag:

    def __init__(self, player):
        self.player = player
        self.background = pygame.transform.rotozoom(
            pygame.image.load('../assets/icons/game_menu.png').convert(), 0,
            2 / 3).convert()
        self.status = pygame.image.load('../assets/icons/status.png').convert()
        self.status = pygame.transform.rotozoom(self.status, 0, 2 / 3)
        self.status.set_colorkey((self.status.get_at((0, 0))))
        self.surface = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        self.font = pygame.font.Font('../assets/icons/CaslonAntique.ttf', 28)
        self.get_status()
        self.button = pygame.image.load('../assets/icons/button.png').convert()
        self.exit_but = pygame.image.load(
            '../assets/icons/return_hover.png').convert()
        self.background.blit(self.exit_but, (967, 124))
        self.clock = pygame.time.Clock()

    def show_main(self):
        card_group = pygame.sprite.Group()
        for d0 in self.player.card_deck:
            cd = CardDraw(d0, self.player.card_deck.index(d0))
            card_group.add(cd)

        button1 = self.button.copy()
        button2 = self.button.copy()
        button3 = self.button.copy()

        func1 = self.font.render('Cards', True, 'Brown')
        func2 = self.font.render('Clues', True, 'Brown')
        func3 = self.font.render('Help', True, 'Brown')

        button1.blit(func1, func1.get_rect(center=button1.get_rect().center))
        button2.blit(func2, func2.get_rect(center=button1.get_rect().center))
        button3.blit(func3, func3.get_rect(center=button1.get_rect().center))

        rect1 = button1.get_rect(center=(827, 218))
        rect2 = button1.get_rect(center=(827, 368))
        rect3 = button1.get_rect(center=(827, 518))
        rects = [rect1, rect2, rect3]

        while True:
            self.clock.tick(30)
            self.surface.blit(self.background, (0, 0))
            self.surface.blit(self.status, (220, 100))
            [q, d, k, h] = bag_check_events(rects)
            if d:
                self.show_card(card_group)
            if k:
                self.show_keys()
            if h:
                self.show_help()
            if q:
                break
            else:
                self.surface.blit(button1, rect1)
                self.surface.blit(button2, rect2)
                self.surface.blit(button3, rect3)

            pygame.display.flip()

    def show_card(self, cg):
        q = False
        while not q:
            self.clock.tick(30)
            self.surface.blit(self.background, (0, 0))

            cg.draw(self.surface)
            mp = pygame.mouse.get_pos()
            for c in cg:
                if c.rect.collidepoint(mp):
                    self.surface.blit(self.font.render(c.intro, True, 'Brown'),
                                      (300, 100))
            pygame.display.flip()
            q, *_ = bag_check_events([])
            if q:
                return

    def show_keys(self):
        q = False
        text_sur = []
        if self.player.keys:
            for word in self.player.keys:
                t = ''
                words = word.split(' ')
                for w in words:
                    if self.font.render(t + w, True,
                                        'Brown').get_width() > 700:
                        text_sur.append(self.font.render(t, True, 'Brown'))
                        t = w + ' '
                    else:
                        t += w + ' '
                text_sur.append(self.font.render(t, True, 'Brown'))
        while not q:
            self.clock.tick(30)
            self.surface.blit(self.background, (0, 0))
            for i in range(len(text_sur)):
                self.surface.blit(text_sur[i], (270, 130 + i *
                                                (self.font.get_height() + 3)))
            pygame.display.flip()
            q, *_ = bag_check_events([])
            if q:
                return

    def show_help(self):
        q = False
        text_sur = [(self.font.render(hint, True, 'Brown')) for hint in hints]
        while not q:
            self.clock.tick(30)
            self.surface.blit(self.background, (0, 0))
            for i in range(len(text_sur)):
                self.surface.blit(text_sur[i], (270, 130 + i *
                                                (self.font.get_height() + 3)))
            pygame.display.flip()
            q, *_ = bag_check_events([])
            if q:
                return

    def get_status(self):
        row = 195
        clo = 280
        dc = 90
        dr = 190
        self.status.blit(self.font.render(str(self.player.atk), True, 'Brown'),
                         (row, clo))
        self.status.blit(
            self.font.render(str(self.player.total_HP), True, 'Brown'),
            (row + dr, clo))
        self.status.blit(
            self.font.render(str(self.player.defe), True, 'Brown'),
            (row, clo + dc))
        self.status.blit(
            self.font.render(str(len(self.player.keys)), True, 'Brown'),
            (row + dr, clo + dc))
        self.status.blit(self.font.render(str(self.player.chi), True, 'Brown'),
                         (row, clo + 2 * dc))


class CardDraw(pygame.sprite.Sprite):

    def __init__(self, card, num):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.rotozoom(card.picture, 0, 1 / 2)
        self.intro = card.intro
        self.rect = self.image.get_rect(
            center=(370 + num % 6 * (5 + self.image.get_width()) + 10,
                    200 + num // 6 * (5 + self.image.get_height()) + 10))
