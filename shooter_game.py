#Создай собственный Шутер!
from pygame import *
from random import randint
from time import time as timer
lost = 0
score = 0
font.init()
font1 = font.SysFont("Arial", 36)
font2 = font.SysFont("Arial", 36)
font3 = font.SysFont("Arial", 70)
font4 = font.SysFont("Arial", 70)
font5 = font.SysFont("Arial", 36)
text_lose1 = font4.render("YOU LOSE!", True, (0, 0, 0))
text_win = font3.render("YOU WIN!", True, (255, 215, 0))
text_score = font2.render("Счет:" + str(score), 1, (255, 255, 255))
text_lose = font1.render("Пропущено:" + str(lost), 1, (255, 255, 255))
text_reload = font5.render("Wait, reload...", 1, (255, 255, 255))
window = display.set_mode((700, 500))
display.set_caption("Shooter")
background = transform.scale(image.load("galaxy.jpg"),(700, 500))
clock = time.Clock()
FPS = 60
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, widht=65, height=65):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(widht,height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 635:
            self.rect.x += self.speed
    def shoot(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 5, 10, 10)
        bullets.add(bullet)         
class Enemy(GameSprite):
    def update(self):
        if self.rect.y <= 500:
            self.rect.y += self.speed
        if self.rect.y >= 500:
            global lost 
            lost += 1
            self.rect.y = 0
            self.rect.x = randint(0, 630)
class Asteroid(GameSprite):
    def update(self):
        if self.rect.y <= 500:
            self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(0, 630)
class Bullet(GameSprite):
    def update(self):
        if self.rect.y >= 0:
            self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()
ship = Player("rocket.png", 250, 430, 5)
ufos = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()
for i in range(3):
    asteroid = Asteroid("asteroid.png", randint(10,650), 0, 2)
    asteroids.add(asteroid)
num_fire = 0
rel_time = False
for i in range(5):
    ufo = Enemy("ufo.png", randint(10,650), 0, randint(1, 1))
    ufos.add(ufo)
game = True
finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    ship.shoot()
                    num_fire += 1
                else:
                    rel_time = True
                    last_time = timer()
                    
    if finish != True:
        window.blit(background, (0,0))
        ship.reset()
        ship.update()
        ufos.update()
        asteroids.update()
        bullets.update()
        bullets.draw(window)
        ufos.draw(window)
        asteroids.draw(window)
        text_lose = font1.render("Пропущено:" + str(lost), 1, (255, 255, 255))
        text_score = font2.render("Счет:" + str(score), 1, (255, 255, 255))
        window.blit(text_lose, (0,0))
        window.blit(text_score, (0,50))
        sprites_list = sprite.groupcollide(ufos, bullets, True, True)
        f = sprite.spritecollide(ship, ufos, False)
        d = sprite.spritecollide(ship, asteroids, False)
        if sprites_list:
            score += 1
            ufo = Enemy("ufo.png", randint(10,650), 0, randint(1,3))
            ufos.add(ufo)
        if lost == 3 or f or d:
            finish = True
            text_lose1 = font4.render("YOU LOSE!", 1, (255, 255, 255))
            window.blit(text_lose1, (250, 230))
        if score == 10:
            finish = True
            text_win = font3.render("YOU WIN!", True, (255, 215, 0))
            window.blit(text_win, (250, 230))
        if rel_time == True:
            new_time = timer()
            
            if new_time - last_time >= 3:
                num_fire = 0
                rel_time = False
            window.blit(text_reload, (300, 400))
    display.update()
    clock.tick(FPS)