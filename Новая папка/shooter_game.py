from pygame import *
from random import randint
from time import time as timer

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

img_back = 'galaxy.jpg'

font.init()
font2 = font.Font(None, 48)
win = font2.render('YOU WIN!', True, (255,255,255))
lose = font2.render('YOU LOSE!', True, (100,0,0))

rel_time = False
num_fire = 0
last_time = 0

max_lost = 3
goal = 10

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Shooter')
background = transform.scale(image.load(img_back), (win_width, win_height))
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_speed, size_x, size_y, player_x, player_y):
        super(). __init__()
        self.image = transform.scale(image.load(player_image), (size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.size_x = size_x
        self.size_y = size_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y, self.size_x, self.size_y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        self.image = transform.scale(image.load('rocket.png'), (self.size_x,self.size_y))
    def fire(self):
        global num_fire
        global rel_time
        global last_time
        keys = key.get_pressed()
        if keys[K_DOWN]:
            if num_fire < 5 and rel_time == False:
                bullet = Bullet('bullet.png', -15, 15, 15, self.rect.x+self.size_x/2-8, self.rect.top-6)
                bullets.add(bullet)
                num_fire += 1
            if num_fire >= 5 and rel_time == False:
                last_time = timer()
                rel_time = True
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        global c
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = -100
            self.speed = randint(1,5)
            lost += 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < -65:
            self.kill()
bullets = sprite.Group()
monsters = sprite.Group()
n = 5
if n > 1000:
    print('Слишком много!')
    exit()
for i in range(n):
    monster = Enemy('ufo.png', randint(1,10), 80, 50, randint(80, win_width - 80), -100)
    monsters.add(monster)
    print('Загружено: ' + str(100/n*len(monsters)) + '%')

ship = Player('rocket.png', 20, 80, 80, 300, 400)

score = 0
lost = 0

finish = False
run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
    if not finish:
        window.blit(background,(0,0))
        
        text = font2.render('Счет: ' + str(score), 1, (255,255,255))
        window.blit(text, (10,20))

        text_lose = font2.render('Пропущено: ' + str(lost), 1, (255,255,255))
        window.blit(text_lose, (10,50))

        ship.update()
        monsters.update()
        bullets.update()
        ship.fire()
        
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        
        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 3:
                reload = font2.render('wait, reload...', 1, (150, 0, 0))
                window.blit(reload, (260,460))
            else:
                num_fire = 0
                rel_time = False

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy('ufo.png', randint(1,10), 80, 50, randint(80, win_width - 80), -40,)
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200,200))
        if score >= goal:
            finish = True
            window.blit(win, (200,200))
        display.update()
    else:
        finish = False
        score = 0
        lost = 0
        num_fire = 0
        life = 3
        for i in bullets:
            i.kill()
        for i in monsters:
            i.kill()
        time.delay(3000)
        for i in range(n):
            monster = Enemy('ufo.png', randint(1,10), 80, 50, randint(80, win_width - 80), -100)
            monsters.add(monster)
            print('Загружено: ' + str(100/n*len(monsters)) + '%')
    time.delay(50)