import os
import time

import cv2
import numpy as np
from colorama import Fore, init

init()

ASCII_CHARS = " .,:;i1tfLCG08@"

VIDEO_PATH = "video.mp4"

FRAME_WIDTH = 100

FPS_FALLBACK = 30

SHARPEN_KERNEL = np.array([
    [ 0, -1,  0],
    [-1,  5, -1],
    [ 0, -1,  0]
], dtype=np.float32)


def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")


def resize_frame(frame, width):
    height, original_width = frame.shape[:2]
    aspect_ratio = height / original_width
    new_height = int(width * aspect_ratio * 0.5)
    return cv2.resize(frame, (width, new_height))


def grayscale(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.filter2D(gray, -1, SHARPEN_KERNEL)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    return clahe.apply(gray)


def frame_to_ascii(gray_frame):
    ascii_image = ""
    char_count = len(ASCII_CHARS)

    for row in gray_frame:
        for pixel in row:
            index = int(pixel / 255 * (char_count - 1))
            ascii_image += ASCII_CHARS[index]
        ascii_image += "\n"

    return ascii_image


def main():
    cap = cv2.VideoCapture(VIDEO_PATH)

    if not cap.isOpened():
        print("Cannot open video.")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        fps = FPS_FALLBACK

    frame_delay = 1 / fps

    clear_terminal()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        resized_frame = resize_frame(frame, FRAME_WIDTH)
        gray_frame = grayscale(resized_frame)
        ascii_frame = frame_to_ascii(gray_frame)

        print("\033[H", end="")
        print(Fore.GREEN + ascii_frame)

        time.sleep(frame_delay)

    cap.release()


if __name__ == "__main__":
    main()