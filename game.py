# Pygame template
import pygame
import random


# Settings
WIN_WIDTH = 1280
WIN_HEIGHT = 720
TITLE = "Asteroid Shooter"
FPS = 60
DEBUG = True

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Intialize
pygame.init()
pygame.mixer.init() # For sound or music
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), flags=pygame.SCALED, vsync=1)
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

# Sounds
laser_sound = pygame.mixer.Sound('./sounds/laser.ogg')
explosion_sound = pygame.mixer.Sound('./sounds/explosion.wav')
bg_music = pygame.mixer.Sound('./sounds/music.wav')
bg_music.play(-1)


# Sprite Groups
all_sprites = pygame.sprite.Group()
ship_sprite = pygame.sprite.GroupSingle()
laser_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()

# Background
bg_surf = pygame.image.load('./graphics/background.png').convert_alpha()

# Ship
class Ship(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.shoot_time = pygame.time.get_ticks()
        self.duration = 300
        self.image = pygame.image.load('./graphics/ship.png').convert_alpha()
        self.rect = self.image.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2))
        self.mask = pygame.mask.from_surface(self.image)
    
    def update(self):
        self.rect.center = pygame.mouse.get_pos()
    
    def shoot(self):
        laser_sound.play()
        current_time = pygame.time.get_ticks()
        if current_time - self.shoot_time > self.duration:
            self.shoot_time = pygame.time.get_ticks()
            laser = Laser(ship.rect.center)
            laser_sprites.add(laser)


# Laser
class Laser(pygame.sprite.Sprite):
    def __init__(self, ship_center):
        super().__init__()
        self.image = pygame.image.load("./graphics/laser.png").convert_alpha()
        self.rect = self.image.get_rect(center=ship_center)
        self.speed = 300
        self.mask = pygame.mask.from_surface(self.image)
    
    def update(self):
        self.rect.y -= self.speed * dt
        if self.rect.bottom < 0:
            self.kill()


# Meteor
class Meteor(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('./graphics/meteor.png').convert_alpha()
        meteor_size = pygame.math.Vector2(self.image.get_size()) * random.uniform(0.5, 1.5)
        self.orig_img = pygame.transform.scale(self.image, meteor_size)
        self.image = self.orig_img
        self.direction = pygame.math.Vector2(random.uniform(-0.5, 0.5), 1)
        self.rect = self.image.get_rect(midtop=pos)
        self.speed = random.randint(200, 600)
        self.mask = pygame.mask.from_surface(self.image)

        # Rotation
        self.rotation = 0
        self.rotation_speed = random.randint(20, 50)
    
    def update(self):
        self.rect.midtop += self.direction * self.speed * dt
        if self.rect.top > WIN_HEIGHT:
            self.kill()
        self.rotate()
    
    def rotate(self):
        self.rotation += self.rotation_speed * dt
        rotated_img = pygame.transform.rotozoom(self.orig_img, self.rotation, 1)
        self.image = rotated_img
        self.rect = self.image.get_rect(midtop=self.rect.midtop)
        self.mask = pygame.mask.from_surface(self.image)



# Score Text
class ScoreText(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.font = pygame.font.Font('./graphics/subatomic.ttf', 50)
        self.score = round(pygame.time.get_ticks()/1000)
        self.score_txt = f'Score: {self.score}'
        self.image = self.font.render(self.score_txt, True, WHITE)
        self.rect = self.image.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT - 50))

    def update(self):
        self.score = round(pygame.time.get_ticks()/1000)
        self.score_txt = f'Score: {self.score}'
        self.image = self.font.render(self.score_txt, True, WHITE)
        self.rect = self.image.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT - 50))


def spawn_meteor():
    x_pos = random.randint(100, WIN_WIDTH - 100)
    meteor = Meteor(pos=(x_pos, -100))
    meteor_sprites.add(meteor)


ship = Ship(ship_sprite)
score = ScoreText(all_sprites)


# Timer
meteor_timer = pygame.event.custom_type()
pygame.time.set_timer(meteor_timer, 500)

# Game Loop
running = True
while running:
    # Keep loop running at the right speed
    dt = clock.tick(FPS) / 1000
    # clock.tick_busy_loop(FPS)

    # Process input (events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ship.shoot()
        if event.type == meteor_timer:
            spawn_meteor()
            

    # Update Game
    all_sprites.update()
    ship_sprite.update()
    laser_sprites.update()
    meteor_sprites.update()

    # Collisions
    # Ship and Meteors
    if pygame.sprite.spritecollide(ship, meteor_sprites, False, pygame.sprite.collide_mask):
        running = False

    # Meteors and lasers    
    if pygame.sprite.groupcollide(meteor_sprites, laser_sprites, True, True, pygame.sprite.collide_mask):
        explosion_sound.play()


    # Draw / Render
    screen.blit(bg_surf, (0, 0))
    all_sprites.draw(screen)
    laser_sprites.draw(screen)
    meteor_sprites.draw(screen)
    ship_sprite.draw(screen)

    # Draw rectangle on score
    pygame.draw.rect(screen, WHITE, score.rect.inflate(20, 20), 2, 2)

    # Debug
    if DEBUG:
        pygame.draw.rect(screen, 'red', ship.rect, 2)
        for sprite in meteor_sprites:
            pygame.draw.rect(screen, 'red', sprite.rect, 2)
        for sprite_rect in laser_sprites:
            pygame.draw.rect(screen, 'red', sprite_rect, 2)
        
    
    
    # *after* drawing everything flip the display
    pygame.display.flip() # or pygame.display.update()
    

pygame.quit()

