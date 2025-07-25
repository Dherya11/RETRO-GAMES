import pygame
import os
import random 

pygame.font.init()  # Initialize font module

# Set up game window dimensions
WIDTH, HEIGHT = 750, 650
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Define absolute path to assets folder (for images)
ASSET_PATH = os.path.join(os.path.dirname(__file__), "assets")

# Load spaceship images
RED_SPACE_SHIP = pygame.image.load(os.path.join(ASSET_PATH, "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join(ASSET_PATH, "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join(ASSET_PATH, "pixel_ship_blue_small.png"))
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join(ASSET_PATH, "pixel_ship_yellow.png"))

# Load laser images
RED_LAZER = pygame.image.load(os.path.join(ASSET_PATH, "pixel_laser_red.png"))
GREEN_LAZER = pygame.image.load(os.path.join(ASSET_PATH, "pixel_laser_green.png"))
BLUE_LAZER = pygame.image.load(os.path.join(ASSET_PATH, "pixel_laser_blue.png"))
YELLOW_LAZER = pygame.image.load(os.path.join(ASSET_PATH, "pixel_laser_yellow.png"))

# Load and scale background image
BG = pygame.transform.scale(pygame.image.load(os.path.join(ASSET_PATH, "background-black.png")), (WIDTH, HEIGHT)) 


# -------------------------- LASER CLASS --------------------------
class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y 
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)  # For collision detection
        
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
     
    def move(self, vel):
        self.y += vel
        
    def off_screen(self, height):
        return not (0 <= self.y <= height)
    
    def collision(self, obj):
        return collide(obj, self)        


# -------------------------- SHIP BASE CLASS --------------------------
class Ship:
    COOLDOWN = 30  # Frames between shots
    
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0
    
    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)
            
    def cooldown(self):
        # Handles cooldown between laser shots
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0: 
            self.cool_down_counter += 1    
        
    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers[:]:  # Loop over copy of list
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)   
        
    def get_width(self):
        return self.ship_img.get_width()     
       
    def get_height(self):
        return self.ship_img.get_height()  


# -------------------------- PLAYER CLASS --------------------------
class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LAZER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
              
    def shoot(self):
        # Shoots a laser if not on cooldown
        if self.cool_down_counter == 0:
            laser = Laser(self.x + self.get_width()//2 - self.laser_img.get_width()//2, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
            
    def draw(self, window):
        super().draw(window)
        self.health_bar(window)
                
    def health_bar(self, window):
        # Draws health bar below the ship
        pygame.draw.rect(window, (255, 0, 0), 
                         (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))               
        pygame.draw.rect(window, (0, 255, 0), 
                         (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * 
                          (self.health / self.max_health), 10))               


# -------------------------- ENEMY CLASS --------------------------
class Enemy(Ship):
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LAZER),
        "green": (GREEN_SPACE_SHIP, GREEN_LAZER),
        "blue": (BLUE_SPACE_SHIP, BLUE_LAZER),
    }
    
    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]    
        self.mask = pygame.mask.from_surface(self.ship_img)
        
    def move(self, vel):
        self.y += vel 
        
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1 


# -------------------------- COLLISION DETECTION --------------------------
def collide(obj1, obj2):
    # Pixel-perfect collision detection using masks
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


# -------------------------- MAIN GAME LOOP --------------------------
def main():
    run = True
    FPS = 60
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 40)
    lost_font = pygame.font.SysFont("comicsans", 50)

    enemies = []
    wave_length = 7
    enemy_vel = 4
    laser_vel = 10
    
    player_vel = 10
    player = Player(260, 500)
    
    clock = pygame.time.Clock()
    lost = False
    lost_count = 0
    
    def redraw_window():
        WIN.blit(BG, (0, 0))
        # UI labels
        lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))
        level_label = main_font.render(f"Level: {level}", 1, (255,255,255))
        
        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        
        for enemy in enemies:
            enemy.draw(WIN)
            
        player.draw(WIN)
        
        if lost:
            lost_label = lost_font.render("You Lost!", 1, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))
        
        pygame.display.update()
    
    # Main game loop
    while run:
        clock.tick(FPS)
        redraw_window()
        
        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1
         
        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue
            
        if len(enemies) == 0:
            # Spawn new wave
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100), 
                              random.randrange(-1599, 100), 
                              random.choice(["red", "blue", "green"]))
                enemies.append(enemy)
                
        # Handle quit events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        
        # Player movement controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player_vel > 0:
            player.x -= player_vel
        if keys[pygame.K_RIGHT] and player.x + player_vel + player.get_width() < WIDTH:
            player.x += player_vel
        if keys[pygame.K_UP] and player.y - player_vel > 0:
            player.y -= player_vel
        if keys[pygame.K_DOWN] and player.y + player_vel + player.get_height() + 15 < HEIGHT:
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()
         
        # Enemy behavior
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, [player])

            if random.randrange(0, 2*60) == 1:
                enemy.shoot()
            for laser in enemy.lasers[:]:
                if laser.collision(player):
                    player.health -= 10
                    enemy.lasers.remove(laser)
                    
            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)

            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)
                   
        player.move_lasers(-laser_vel, enemies)


# -------------------------- MAIN MENU --------------------------
def main_menu():
    title_font = pygame.font.SysFont("comicsans", 35)
    run = True
    while run:
        WIN.blit(BG, (0, 0))
        title_label = title_font.render("PRESS THE MOUSE TO BEGIN .....", 1, (255, 255, 255))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()                           


# Run the main menu (entry point)
main_menu()
