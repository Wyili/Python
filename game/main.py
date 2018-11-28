import pygame
import random
from pygame.locals import *

WIDTH = 1200
HEIGHT = 600
GRADE = 0


class Background:
    def __init__(self):
        self.image = pygame.image.load('./res/background.jpg')
        self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))
        self.image_rect = self.image.get_rect()

    def display(self):
        screen.blit(self.image, self.image_rect)


class Peas:
    def __init__(self):
        self.image = pygame.image.load('./res/peas.jpg')
        self.image = pygame.transform.scale(self.image, (int(0.05 * WIDTH), int(0.15 * HEIGHT)))
        self.image_rect = self.image.get_rect()
        self.image_rect.top = 280
        self.image_rect.left = 220
        self.is_move_up = False
        self.is_move_down = False
        self.is_shot = False

    def display(self):
        screen.blit(self.image, self.image_rect)

    def move_up(self):
        if peas.image_rect.top > 80:
            self.image_rect.move_ip(0, -9)
        for z in Zombie.zombie_list:
            if self.image_rect.colliderect(z.image_rect):
                print('总分为：', GRADE)
                pygame.quit()
                exit()

    def move_down(self):
        if peas.image_rect.bottom < 565:
            self.image_rect.move_ip(0, 9)
        for z in Zombie.zombie_list:
            if self.image_rect.colliderect(z.image_rect):
                print('总分为：', GRADE)
                pygame.quit()
                exit()

    def shot_bullet(self):
        bullets = Bullet(self)
        Bullet.bullet_list.append(bullets)


class Bullet:
    bullet_list = []
    interval = 0

    def __init__(self, pea):
        self.image = pygame.image.load('./res/bullet.jpg')
        self.image = pygame.transform.scale(self.image, (int(0.02 * WIDTH), int(0.05 * HEIGHT)))
        self.image_rect = self.image.get_rect()
        self.image_rect.top = pea.image_rect.top + 5
        self.image_rect.left = pea.image_rect.right

    def display(self):
        screen.blit(self.image, self.image_rect)

    def move(self):
        self.image_rect.move_ip(10, 0)
        if self.image_rect.left > WIDTH - 10:
            Bullet.bullet_list.remove(self)
        for z in Zombie.zombie_list:
            if self.image_rect.colliderect(z.image_rect):
                Bullet.bullet_list.remove(self)
                Zombie.zombie_list.remove(z)
                global GRADE
                GRADE += 1
                break


class Zombie:
    zombie_list = []
    interval = 0

    def __init__(self):
        self.image = pygame.image.load('./res/zombie.jpg')
        self.image = pygame.transform.scale(self.image, (int(0.05 * WIDTH), int(0.15 * HEIGHT)))
        self.image_rect = self.image.get_rect()
        self.image_rect.top = random.randint(60, HEIGHT - 120)
        self.image_rect.left = WIDTH - 200

    def display(self):
        screen.blit(self.image, self.image_rect)

    def move(self):
        self.image_rect.move_ip(-5, 0)
        if self.image_rect.right <= 0:
            Zombie.zombie_list.remove(self)
        for b in Bullet.bullet_list:
            if self.image_rect.colliderect(b.image_rect):
                Zombie.zombie_list.remove(self)
                Bullet.bullet_list.remove(b)
                global GRADE
                GRADE += 1
                break
        if self.image_rect.colliderect(peas.image_rect):
            print('总分为：', GRADE)
            pygame.quit()
            exit()


def key_control():
    for event in pygame.event.get():
        if event.type == QUIT:
            print('总分为：', GRADE)
            pygame.quit()
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_UP:
                peas.is_move_up = True
            elif event.key == K_DOWN:
                peas.is_move_down = True
            elif event.key == K_SPACE:
                peas.is_shot = True
        elif event.type == KEYUP:
            if event.key == K_UP:
                peas.is_move_up = False
            elif event.key == K_DOWN:
                peas.is_move_down = False
            elif event.key == K_SPACE:
                peas.is_shot = False


if __name__ == '__main__':
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    background = Background()
    clock = pygame.time.Clock()
    peas = Peas()
    while True:
        screen.fill((0, 0, 0))
        background.display()
        peas.display()
        key_control()
        if peas.is_move_up:
            peas.move_up()
        if peas.is_move_down:
            peas.move_down()
        Bullet.interval += 1
        if peas.is_shot and Bullet.interval >= 20:
            Bullet.interval = 0
            peas.shot_bullet()
        Zombie.interval += 1
        if Zombie.interval >= 20:
            Zombie.interval = 0
            zombie = Zombie()
            Zombie.zombie_list.append(zombie)
        for bullet in Bullet.bullet_list:
            bullet.display()
            bullet.move()
        for zombie in Zombie.zombie_list:
            zombie.display()
            zombie.move()
        clock.tick(60)
        pygame.display.update()
