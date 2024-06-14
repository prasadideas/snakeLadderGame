import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height))

# Load the image
image = pygame.image.load('images/pawn.png')  # Replace 'your_image.png' with the path to your image

# Initial and target coordinates
x1, y1 = 958, 990
x2, y2 = 958, 630

# Movement speed (pixels per frame)
speed = 5

# Calculate the distance and direction
dx = x2 - x1
dy = y2 - y1
distance = math.sqrt(dx**2 + dy**2)
steps = int(distance // speed)
if steps == 0:
    steps = 1
x_step = dx / steps
y_step = dy / steps

print(f"Initial position: ({x1}, {y1})")
print(f"Target position: ({x2}, {y2})")
print(f"Steps: {steps}, x_step: {x_step}, y_step: {y_step}")

def main():
    clock = pygame.time.Clock()

    # Current position
    current_x = x1
    current_y = y1

    moving = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if moving:
            # Update the position
            current_x += x_step
            current_y += y_step

            # Check if the image has reached the target
            if (dx == 0 and abs(current_y - y2) < abs(y_step)) or (dy == 0 and abs(current_x - x2) < abs(x_step)) or (abs(current_x - x2) < abs(x_step) and abs(current_y - y2) < abs(y_step)):
                current_x = x2
                current_y = y2
                moving = False
                print(f"Reached target position: ({current_x}, {current_y})")

        # Clear screen
        screen.fill((255, 255, 255))  # Fill the screen with white

        # Draw the image at the current position
        screen.blit(image, (current_x, current_y))

        # Update the display
        pygame.display.flip()
        clock.tick(60)  # Limit to 60 frames per second

if __name__ == "__main__":
    main()
