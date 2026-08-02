#!/usr/bin/env python3
"""
make_ascii_svg.py
-----------------
Converts preprocessed profile photo to monochrome ASCII art and generates assets/ascii-profile.svg.

Features:
- Character ramp: " .`:-=+*cs#%@"
- Line-by-line typing animation with SMIL / CSS keyframe line reveal.
- Monochrome palette (crisp whites, silver grays, cyan accents).
- Terminal frame with scanlines and blinking cursor.
- Executes once and freezes.
"""

import os
import numpy as np
import cv2
from prep_photo import preprocess_image

CHAR_RAMP = " .`:-=+*cs#%@"  # 12 characters


def image_to_ascii(
    img_array: np.ndarray,
    cols: int = 58,
    char_aspect_ratio: float = 0.55
) -> list:
    h, w = img_array.shape
    rows = int((h / w) * cols * char_aspect_ratio)
    
    # Resize image to ASCII grid dimensions
    resized = cv2.resize(img_array, (cols, rows), interpolation=cv2.INTER_AREA)

    ascii_lines = []
    ramp_len = len(CHAR_RAMP)

    for r in range(rows):
        line_chars = []
        for c in range(cols):
            pixel_val = resized[r, c]
            # Map 0..255 to 0..ramp_len-1
            char_idx = int((pixel_val / 255.0) * (ramp_len - 1))
            line_chars.append(CHAR_RAMP[char_idx])
        ascii_lines.append("".join(line_chars))

    return ascii_lines


def generate_ascii_svg(
    prepped_img_path: str = "data/prepped_profile.png",
    output_path: str = "assets/ascii-profile.svg",
    cols: int = 56
) -> None:
    if not os.path.exists(prepped_img_path):
        img_array = preprocess_image(output_path=prepped_img_path)
    else:
        img_array = cv2.imread(prepped_img_path, cv2.IMREAD_GRAYSCALE)

    ascii_lines = image_to_ascii(img_array, cols=cols)

    width = 415
    line_height = 14
    font_size = 11.5
    top_margin = 60
    bottom_margin = 30
    height = top_margin + len(ascii_lines) * line_height + bottom_margin

    # Build animated line elements
    line_svg_elements = []
    total_lines = len(ascii_lines)
    delay_step = 2.4 / max(1, total_lines)

    for idx, line_text in enumerate(ascii_lines):
        y_pos = top_margin + (idx * line_height)
        delay = round(idx * delay_step + 0.2, 2)
        # Escape xml special chars
        escaped_text = (
            line_text.replace("&", "&amp;")
                     .replace("<", "&lt;")
                     .replace(">", "&gt;")
                     .replace(" ", "&#160;")
        )
        
        line_svg_elements.append(
            f'<text x="24" y="{y_pos}" class="ascii-line" style="animation-delay: {delay}s;">{escaped_text}</text>'
        )

    lines_code = "\n    ".join(line_svg_elements)

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="{height}">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&amp;display=swap');

      .card-bg {{ fill: #0A0F1F; stroke: #00E5FF; stroke-width: 1.5; stroke-opacity: 0.5; }}
      .header-bg {{ fill: #050816; stroke: #00E5FF; stroke-width: 1; stroke-opacity: 0.3; }}
      .title-text {{ font-family: 'JetBrains Mono', monospace; font-size: 11px; fill: #5EEAFF; font-weight: bold; }}

      .ascii-line {{
        font-family: 'JetBrains Mono', 'Fira Code', monospace;
        font-size: {font_size}px;
        fill: #E2E8F0;
        white-space: pre;
        opacity: 0;
        animation: lineReveal 0.15s ease-out forwards;
      }}

      .cursor {{
        fill: #00E5FF;
        animation: blink 0.8s infinite alternate;
      }}

      @keyframes lineReveal {{
        0% {{ opacity: 0; transform: translateX(-4px); }}
        100% {{ opacity: 1; transform: translateX(0); }}
      }}

      @keyframes blink {{
        0% {{ opacity: 1; }}
        100% {{ opacity: 0; }}
      }}

      .scanline {{
        fill: url(#asciiScanline);
        opacity: 0.15;
        pointer-events: none;
      }}
    </style>

    <pattern id="asciiScanline" width="100" height="4" patternUnits="userSpaceOnUse">
      <line x1="0" y1="0" x2="100" y2="0" stroke="#000000" stroke-width="1.5" opacity="0.3" />
    </pattern>

    <filter id="asciiGlow" x="-10%" y="-10%" width="120%" height="120%">
      <feGaussianBlur stdDeviation="2" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>

  <!-- Container -->
  <rect x="4" y="4" width="{width - 8}" height="{height - 8}" rx="10" ry="10" class="card-bg" filter="url(#asciiGlow)"/>

  <!-- Header -->
  <path d="M 4 14 Q 4 4 14 4 L {width - 14} 4 Q {width - 4} 4 {width - 4} 14 L {width - 4} 36 L 4 36 Z" fill="#050816"/>
  <line x1="4" y1="36" x2="{width - 4}" y2="36" stroke="#00E5FF" stroke-opacity="0.3" stroke-width="1"/>
  
  <circle cx="20" cy="20" r="4.5" fill="#FF5F56"/>
  <circle cx="34" cy="20" r="4.5" fill="#FFBD2E"/>
  <circle cx="48" cy="20" r="4.5" fill="#27C93F"/>

  <text x="{width // 2}" y="24" text-anchor="middle" class="title-text">shyguy6479@AI-OS:~ // ASCII_PORTRAIT</text>

  <!-- ASCII Art Lines -->
  <g>
    {lines_code}
  </g>

  <!-- Terminal Footer Cursor -->
  <g transform="translate(24, {height - 18})">
    <text x="0" y="0" font-family="'JetBrains Mono', monospace" font-size="11" fill="#00FFB3">&gt; RENDER_COMPLETE</text>
    <rect x="135" y="-10" width="8" height="13" class="cursor"/>
  </g>

  <!-- Scanlines Overlay -->
  <rect x="4" y="4" width="{width - 8}" height="{height - 8}" rx="10" ry="10" class="scanline"/>
</svg>
"""

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content.strip())
    print(f"✅ Generated ASCII portrait SVG: {output_path}")


if __name__ == "__main__":
    generate_ascii_svg()
