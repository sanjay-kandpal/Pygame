import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flower Bombing")

# Load images
jet_image = pygame.transform.scale(pygame.image.load("jet.png"), (100, 50))  # Adjusted dimensions for jet
flower_image = pygame.transform.scale(pygame.image.load("flower.png"), (30, 30))  # Adjusted dimensions for flower
home_image = pygame.transform.scale(pygame.image.load("home.png"), (100, 100))  # Adjusted dimensions for home
game_over_image = pygame.transform.scale(pygame.image.load("game_over.png"), (WIDTH, HEIGHT))  # Game over image

# Jet plane class
class Jet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = jet_image
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2
        self.rect.y = 50
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

# Flower class
class Flower(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = flower_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5

    def update(self):
        self.rect.y += self.speed

# Home class
class Home(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = home_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Explosion class
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.image = explosion_frames[0]
        self.rect = self.image.get_rect(center=center)
        self.frame_index = 0
        self.frame_rate = 10
        self.last_update = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.frame_index += 1
            if self.frame_index >= len(explosion_frames):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_frames[self.frame_index]
                self.rect = self.image.get_rect(center=center)
            self.last_update = now

# Load explosion frames
explosion_frames = [pygame.transform.scale(pygame.image.load(f"explosion{i}.png"), (100, 100)) for i in range(1, 6)]

# Game variables
score = 0
homes_generated = 0
max_homes = 30  # Maximum number of homes to be generated

# Game loop
jet = Jet()
homes = pygame.sprite.Group()  # Group for homes
flowers = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(jet)
clock = pygame.time.Clock()
running = True
game_over = False

# Generate multiple homes
def generate_homes():
    global homes_generated
    for _ in range(3):  # Adjust the number of homes as needed
        home = Home(random.randint(0, WIDTH - 100), random.randint(HEIGHT // 2, HEIGHT - 100))
        homes.add(home)
        all_sprites.add(home)
        homes_generated += 1

generate_homes()

while running:
    clock.tick(60)  # Limit the frame rate

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        # Drop Bomb
        if random.randint(0, 30) == 0:
            flower = Flower(jet.rect.x, jet.rect.y)
            flowers.add(flower)
            all_sprites.add(flower)

        # Check for collisions with homes
        for home in homes:
            hits = pygame.sprite.spritecollide(home, flowers, True)
            for hit in hits:
                explosion = Explosion(hit.rect.center)
                all_sprites.add(explosion)
                home.kill()  # Remove the home after collision
                generate_homes()  # Generate new homes
                score += 1  # Increment the score

        # Update objects
        jet.update()
        flowers.update()
        all_sprites.update()

        # Draw objects
        screen.fill((135, 206, 235))  # Sky blue background
        all_sprites.draw(screen)

        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        # Check for game over
        if homes_generated >= max_homes:
            game_over = True

    else:  # Game over screen
        screen.blit(game_over_image, (0, 0))
        font = pygame.font.Font(None, 48)
        score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (WIDTH // 2 - 150, HEIGHT // 2 + 50))

    pygame.display.flip()

pygame.quit()
