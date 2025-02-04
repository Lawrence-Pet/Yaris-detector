import cv2
import os
import matplotlib.pyplot as plt
from typing import List


def read_images_from_folder(foldername: str) -> List[cv2.typing.MatLike]:
    '''
    Returns a list of cv2.typing.MatLike objects based on all files in the passed folder.
    Does NOT verify that files in the folder are images. 
    '''
    images = []
    for filename in os.listdir(foldername):
        img = cv2.imread(os.path.join(foldername, filename))
        if img is not None:
            images.append(img)
    return images

def image_squarer(img: cv2.typing.MatLike) -> cv2.typing.MatLike:
    '''
    Padds the image either horisontally or vertically resulting in a square image.
    Padding occurs equally in the padding dimension resulting in a centered image.
    (E.g if the image is width=100 and height=200 the image will be padded by 50 pixels on each side to reach a width of 100.)
    '''
    # Calculate the difference to make the image square
    height_diff = img.shape[1] - img.shape[0]
    padding = abs(height_diff) // 2

    # Add padding to the top and bottom if height is less than width
    if height_diff > 0:
        # Calculate the mean color value of the top half and bottom half of the image
        mean_color_top = img[:img.shape[0]//2, :, :].mean(axis=(0, 1)).astype(int).tolist()
        mean_color_bottom = img[img.shape[0]//2:, :, :].mean(axis=(0, 1)).astype(int).tolist()
        padded_img = cv2.copyMakeBorder(img, padding,0, 0, 0, cv2.BORDER_CONSTANT, value=mean_color_top)
        padded_img = cv2.copyMakeBorder(padded_img, 0, padding, 0, 0, cv2.BORDER_CONSTANT, value=mean_color_bottom)
    
    # if width is less than height add padding to sides
    elif height_diff < 0:
        mean_color_left = img[:, :img.shape[1]//2, :].mean(axis=(0, 1)).astype(int).tolist()
        mean_color_right = img[:, img.shape[1]//2:, :].mean(axis=(0, 1)).astype(int).tolist()
        padded_img = cv2.copyMakeBorder(img, 0,0, padding, 0, cv2.BORDER_CONSTANT, value=mean_color_left)
        padded_img = cv2.copyMakeBorder(padded_img, 0, 0, 0, padding, cv2.BORDER_CONSTANT, value=mean_color_right)

    elif height_diff == 0: # if no do nothing
        padded_img = img
    return padded_img

def resizer(width: int, height: int, img: cv2.typing.MatLike) -> cv2.typing.MatLike:
    '''Resizes an image to a required dimensionality. Both up and down.'''
    return cv2.resize(src = img, dsize=(width, height))

def pipe_pictures(foldername: str) -> List[cv2.typing.MatLike]:
    '''
    Pipes pictures in a folder through a pipeline that squares and resizes the images.
    '''
    images = read_images_from_folder(foldername)
    square_images = [image_squarer(img) for img in images]
    resized = [resizer(100, 100, img) for img in square_images]