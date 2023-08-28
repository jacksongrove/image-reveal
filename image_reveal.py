# Import necessary libraries
import os
import random
import pygame as pg
import cv2
import numpy as np

# Constants
DIRECTORY = '/Users/jacksongrove/Desktop/Code/Projects/Image_Reveal/Image Bank'
WINDOW_SIZE = (800, 800)

def get_random_image(directory):
    """
    Retrieve a random image file path from the specified directory.
    
    Args:
        directory (str): Path to the directory containing images.
        
    Returns:
        str: Randomly selected image file path.
    """
    file_list = [os.path.join(directory, filename) for filename in os.listdir(directory) if os.path.isfile(os.path.join(directory, filename))]
    return random.choice(file_list)

class Dot:
    """
    Class to represent a dot on the screen.
    """
    def __init__(self, rect, color):
        self.rect = rect
        self.color = color

    def draw(self, screen):
        """
        Render the dot on the screen.
        
        Args:
            screen (pygame.Surface): Pygame screen surface.
        """
        center = self.rect.center
        radius = min(self.rect.size) // 2
        pg.draw.circle(screen, self.color, center, radius)

    def hit_test(self, pos):
        """
        Check if a given position is within the dot's area.
        
        Args:
            pos (tuple): Position coordinates (x, y).
            
        Returns:
            bool: True if position is within the dot, False otherwise.
        """
        dx, dy = pos[0] - self.rect.centerx, pos[1] - self.rect.centery
        return dx * dx + dy * dy <= min(self.rect.size) // 2 * min(self.rect.size) // 2

def main():
    # Load a random image and convert its color space
    file_name = get_random_image(DIRECTORY)
    img = cv2.cvtColor(cv2.imread(file_name), cv2.COLOR_BGR2RGB)

    # Resize the image to fit within the specified window size
    scale = min(WINDOW_SIZE[0] / img.shape[1], WINDOW_SIZE[1] / img.shape[0])
    img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)

    # Initialize Pygame
    pg.init()
    screen = pg.display.set_mode(WINDOW_SIZE)

    # Create initial dots based on the image's average color in certain regions
    dot_space = 1
    dot_size = ((img.shape[1] - dot_space) // 2, (img.shape[0] - dot_space) // 2)
    offset = ((WINDOW_SIZE[0] - img.shape[1]) // 2, (WINDOW_SIZE[1] - img.shape[0]) // 2)
    dots = [Dot(pg.Rect(offset[0] + dx * dot_size[0], offset[1] + dy * dot_size[1], *dot_size),
                img[dy * dot_size[1]:(dy + 1) * dot_size[1], dx * dot_size[0]:(dx + 1) * dot_size[0]].mean(axis=(0, 1)).astype(int))
            for dx in range(2) for dy in range(2)]

    # Main game loop
    gameState = True
    while gameState:
        # Clear the screen
        screen.fill((0, 0, 0))

        # Render all dots
        for dot in dots:
            dot.draw(screen)

        # Update the display
        pg.display.flip()

        # Handle user events
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                gameState = False
            elif event.type == pg.MOUSEMOTION:
                for dot in dots.copy():
                    if dot.hit_test(event.pos) and max(dot.rect.size) > dot_space:
                        dots.remove(dot)
                        size = (dot.rect.width - dot_space) // 2, (dot.rect.height - dot_space) // 2
                        for dx in range(2):
                            for dy in range(2):
                                rect = pg.Rect(dot.rect.x + dx * (size[0] + dot_space), dot.rect.y + dy * (size[1] + dot_space), *size)
                                sub_img = img[rect.y - offset[1]:rect.y + rect.h - offset[1], rect.x - offset[0]:rect.x + rect.w - offset[0]]
                                color = np.round(sub_img.mean(axis=(0, 1))).astype(int)
                                color = np.clip(color, 0, 255)  # Ensure color values are within the valid range
                                dots.append(Dot(rect, color))

    # Cleanup and exit
    pg.quit()

if __name__ == "__main__":
    main()