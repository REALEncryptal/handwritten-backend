import base64
import numpy as np
from PIL import Image
import cv2
import random
import io
import matplotlib.pyplot as plt

from database import Database
from perlin_noise import PerlinNoise

db = Database()

def rotate_image(image, angle):

    # Get the center of the image
    height, width = image.shape[:2]
    center = (width / 2, height / 2)
    
    # Generate the rotation matrix
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    
    # Apply the rotation matrix to the image
    rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height))
    
    return rotated_image

def warp_image(image, warp_factor):
    height, width = image.shape[:2]
    
    # Generate a random grid
    grid_x, grid_y = np.meshgrid(np.arange(width), np.arange(height))
    grid_x = grid_x.astype(np.float32)
    grid_y = grid_y.astype(np.float32)
    
    # Add random noise to the grid
    noise = np.random.normal(0, warp_factor, (height, width, 2))
    grid_x += noise[:, :, 0]
    grid_y += noise[:, :, 1]
    
    # Generate the warped image
    warped_image = cv2.remap(image, grid_x, grid_y, cv2.INTER_LINEAR)
    
    return warped_image

def create(sentence="你 你 你你", target_height=100):
    noise = PerlinNoise(seed=random.randint(0, 1000))
    images = []

    for i, character in enumerate(sentence):
        print(character)

        if character == " ":
            min_width = .3
            max_width = .5

            random_width = random.uniform(min_width, max_width)
            image_np = np.ones((target_height, int(target_height * random_width), 4), dtype=np.uint8) * 255
        else:
            encoded_image = db.GetCharacter(character)[0][0]
            image_data = base64.b64decode(encoded_image.split(',')[1])

            image_pil = Image.open(io.BytesIO(image_data))
            image_np = np.array(image_pil)

            # Warp image
            warp_factor = random.randint(0, 10) / 10    
            image_np = warp_image(image_np, warp_factor)


            # Rotate image
            rotate_angle = noise(i/1.1) * 10 + random.randint(-5, 5)
            image_np = rotate_image(image_np, rotate_angle)


            # Resize to target height
            ratio = target_height / image_np.shape[0]
            image_np = cv2.resize(image_np, (int(image_np.shape[1] * ratio), target_height))
        
        images.append(image_np)
        print("done")
    
    # add images next to each other to create a sentence
    sentence_image = np.concatenate(images, axis=1)

    # Smooth the image
    sentence_image = cv2.GaussianBlur(sentence_image, (7, 7), 0)

    # Sharpen
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    sentence_image = cv2.filter2D(sentence_image, -1, kernel)

    # create a white background with 4 channels
    background = np.ones_like(sentence_image) * 255

    # add the sentence to the background
    result = cv2.add(sentence_image, background)
    
    # Display the image
    plt.imshow(sentence_image)
    plt.show()


    cv2.waitKey(0)

create()
