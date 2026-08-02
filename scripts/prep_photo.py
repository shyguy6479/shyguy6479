#!/usr/bin/env python3
"""
prep_photo.py
-------------
Preprocesses profile image for ASCII art rendering:
1. Generates synthetic futuristic portrait if no source image provided.
2. Removes background using rembg (if enabled / available).
3. Enhances contrast using OpenCV CLAHE.
4. Converts to grayscale.
"""

import os
import sys
import numpy as np
from PIL import Image, ImageDraw
import cv2

# Check if rembg can be imported and ENABLE_REMBG is set
ENABLE_REMBG = os.environ.get("ENABLE_REMBG", "0") == "1"
REMBG_AVAILABLE = False

if ENABLE_REMBG:
    try:
        from rembg import remove
        REMBG_AVAILABLE = True
    except BaseException:
        REMBG_AVAILABLE = False


def generate_default_cyber_portrait(width: int = 300, height: int = 300) -> Image.Image:
    """Generates a high-contrast synthetic Cyber AI portrait silhouette."""
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    center_x, center_y = width // 2, height // 2

    # Head silhouette
    draw.ellipse([center_x - 65, center_y - 95, center_x + 65, center_y + 35], fill=(240, 240, 240, 255))
    # Neck and shoulders
    draw.polygon([
        (center_x - 30, center_y + 30),
        (center_x + 30, center_y + 30),
        (center_x + 110, center_y + 140),
        (center_x - 110, center_y + 140)
    ], fill=(220, 220, 220, 255))

    # Cyber Visor / Headset outline
    draw.rectangle([center_x - 55, center_y - 45, center_x + 55, center_y - 20], fill=(50, 50, 50, 255))
    draw.line([center_x - 60, center_y - 32, center_x + 60, center_y - 32], fill=(255, 255, 255, 255), width=4)

    return img


def preprocess_image(
    input_path: str = "data/input_profile.png",
    output_path: str = "data/prepped_profile.png"
) -> np.ndarray:
    os.makedirs("data", exist_ok=True)

    # 1. Load or generate image
    if os.path.exists(input_path):
        print(f"📷 Loading input image: {input_path}")
        img = Image.open(input_path).convert("RGBA")
    else:
        print("⚠️ No input image found. Generating synthetic cyber portrait...")
        img = generate_default_cyber_portrait()
        img.save(input_path)

    # 2. Background removal using rembg
    img_no_bg = img
    if REMBG_AVAILABLE:
        try:
            print("✂️ Removing background with rembg...")
            img_no_bg = remove(img)
        except BaseException as e:
            print(f"⚠️ rembg background removal skipped ({e}), using default image canvas.")
            img_no_bg = img
    else:
        print("ℹ️ rembg background removal skipped for fast local rendering.")

    # Convert to OpenCV format (BGRA -> Grayscale)
    np_img = np.array(img_no_bg)
    
    # If transparent, create canvas background
    if np_img.ndim == 3 and np_img.shape[2] == 4:
        alpha = np_img[:, :, 3] / 255.0
        gray_orig = cv2.cvtColor(np_img[:, :, :3], cv2.COLOR_RGB2GRAY)
        gray = (gray_orig * alpha).astype(np.uint8)
    elif np_img.ndim == 3:
        gray = cv2.cvtColor(np_img, cv2.COLOR_RGB2GRAY)
    else:
        gray = np_img.astype(np.uint8)

    # 3. Enhance contrast using CLAHE
    clahe = cv2.createCLAHE(clipLimit=3.5, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)

    # Save prepped image
    cv2.imwrite(output_path, enhanced)
    print(f"✅ Preprocessed profile image saved to: {output_path}")

    return enhanced


if __name__ == "__main__":
    preprocess_image()
