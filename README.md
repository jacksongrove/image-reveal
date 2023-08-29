# Image Reveal Game

An interactive visual game built with Pygame and OpenCV. Hover over the dots to gradually reveal a randomly selected image from the 'Image Bank'.

![Game Screenshot](image-reveal/image-reveal-demo.gif) <!-- Replace 'path_to_screenshot.png' with the path to an actual screenshot of your game if you have one -->

## Features

- **Random Image Selection**: Each game session starts with a randomly chosen image from the 'Image Bank' directory.
- **Image Processing**: Uses OpenCV to fit the selected image to the game window and extract color information.
- **Interactive Gameplay**: Hover over the dots to split them into smaller ones, revealing more of the underlying image.
- **Dynamic Dot Representation**: Dots represent portions of the image, with their color determined by averaging the colors of the pixels they cover.
- **User-Friendly Controls**: Exit the game anytime by closing the window or pressing the ESC key.

## Installation & Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/jacksongrove/image-reveal.git
   ```
2. Navigate to the project directory:
   ```bash
   cd image-reveal
   ```
4. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
5. Add your own images to the `Image Bank` directory or use the provided sample images.
   
6. Run the game: 
   ```bash
   python image-reveal.py
   ```
