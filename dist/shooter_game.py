from pygame import *
from random import randint
from time import time as Timer
window = display.set_mode((700, 500))
display.set_caption("Shooter-game")
background = transform.scale(image.load("galaxy.jpg"), (700, 500))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire = mixer.Sound('fire.ogg')
#kick.play()

clock = time.Clock()
FPS = 60



class GameSprite(sprite.Sprite):
    def __init__(self,filename,speed,x,y, size_x=65, size_y=65):
        super().__init__()
        self.image = transform.scale(image.load(filename),(size_x,size_y))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

bullets = sprite.Group()

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x >= 0 :
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x <= 635 :
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png",10, self.rect.centerx, self.rect.top,10,20)
        bullets.add(bullet)

global lost, score, text_lose, text_score

class Enemy(GameSprite):
    def update(self):
        global lost, text_lose
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(0,635)
            lost = lost + 1
            text_lose = font1.render("Missed:" + str(lost),1,(255,255,255)) 
        else:
            self.rect.y += self.speed

class Enemy2(GameSprite):
    def update(self):
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(0,635)
        else:
            self.rect.y += self.speed


hero1 = Player("rocket.png", 10, 20, 425)


monsters = sprite.Group()

asteroids = sprite.Group()


for i in range(6):
    monster = Enemy("ufo.png", randint(1,5), randint(0,635),0)
    monsters.add(monster)

for i in range(3):
    asteroid = Enemy("asteroid.png", randint(1,5), randint(0,635),0)
    asteroids.add(asteroid)



font.init()
font1 = font.SysFont("Arial", 36)

font2 = font.SysFont("Arial", 100)
lost = 0
text_lose = font1.render("Missed:" + str(lost),1,(255,255,255)) 
score = 0
text_score = font1.render("Score:" + str(score),1,(255,255,255)) 

num_fire = 0
rel_fire = False

game = True
finish = False
while game:
    window.blit(background,(0, 0))
    window.blit(text_lose,(0, 0))
    window.blit(text_score,(0, 25))
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_fire == False:
                    hero1.fire()
                    num_fire = num_fire + 1
                if num_fire >= 5 and rel_fire == False:
                    rel_fire = True
                    cur_time = Timer()
    if finish != True:
        hero1.reset()
        hero1.update()
        monsters.draw(window)
        asteroids.draw(window)
        bullets.draw(window)
        bullets.update()
        asteroids.update()
        if rel_fire == True:
            cur_time2 = Timer()
            if cur_time2 - cur_time < 3:
                re = font2.render('Wait, reload...', True, (255, 215, 0))
                window.blit(re, (200,200))
            else:
                num_fire = 0
                rel_fire = False
        if sprite.spritecollide(hero1, asteroids, False):
            finish = True
            lose = font2.render('You lose', True, (255, 215, 0))
            window.blit(lose, (200,200))
        monsters.update()
        sprites_list = sprite.groupcollide(monsters, bullets, True, True)
        for i in sprites_list:
            score += 1
            text_score = font1.render("Score:" + str(score),1,(255,255,255)) 
            monster = Enemy("ufo.png", randint(1,5), randint(0,635),0)
            monsters.add(monster)
        if score >= 10:
            finish = True
            win = font2.render('You WON', True, (255, 215, 0))
            window.blit(win, (200,200))
        if lost >= 30:
            finish = True
            lose = font2.render('You lose', True, (255, 215, 0))
            window.blit(lose, (200,200))
        display.update()
        clock.tick(FPS)


