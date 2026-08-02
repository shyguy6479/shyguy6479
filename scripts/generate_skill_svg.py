#!/usr/bin/env python3
"""
generate_skill_svg.py
---------------------
Generates assets/skill-bars.svg - an animated Cyberpunk Skill Dashboard
for shyguy6479.

Skills & Metrics:
- Python: 95%
- FastAPI: 90%
- React: 85%
- Machine Learning: 90%
- Deep Learning: 80%
- LLMs: 75%

Features:
- Smooth keyframe animation filling bars from 0% to target value.
- Neon glow gradients (#00C8FF -> #00E5FF -> #00FFB3).
- Standard SVG & CSS animations compatible with GitHub.
"""

import os


def generate_skill_svg(output_path: str = "assets/skill-bars.svg") -> None:
    width = 850
    height = 360

    skills = [
        {"name": "Python", "val": 95, "icon": "🐍"},
        {"name": "FastAPI", "val": 90, "icon": "⚡"},
        {"name": "React", "val": 85, "icon": "⚛️"},
        {"name": "Machine Learning", "val": 90, "icon": "🤖"},
        {"name": "Deep Learning", "val": 80, "icon": "🧠"},
        {"name": "LLMs & AI Agents", "val": 75, "icon": "🔮"},
    ]

    skill_rows_svg = []
    start_y = 75
    row_height = 42
    bar_max_width = 540  # Max pixel width for 100%

    keyframe_css_list = []

    for idx, skill in enumerate(skills):
        y_pos = start_y + idx * row_height
        target_pct = skill["val"]
        target_px = int((target_pct / 100.0) * bar_max_width)
        anim_name = f"fillSkill{idx}"
        delay = round(0.3 + (idx * 0.2), 2)

        # Build dynamic CSS keyframe animation for this skill bar
        keyframe_css_list.append(f"""
      @keyframes {anim_name} {{
        0% {{ width: 0px; }}
        100% {{ width: {target_px}px; }}
      }}
      #skill-bar-{idx} {{
        animation: {anim_name} 1.8s cubic-bezier(0.1, 0.8, 0.2, 1) {delay}s forwards;
      }}""")

        skill_rows_svg.append(f"""
    <g transform="translate(30, {y_pos})">
      <text x="0" y="16" class="skill-name">{skill['icon']} {skill['name']}</text>
      <!-- Background Bar -->
      <rect x="200" y="2" width="{bar_max_width}" height="18" rx="4" class="bar-bg"/>
      <!-- Animated Fill Bar -->
      <rect id="skill-bar-{idx}" x="200" y="2" height="18" rx="4" class="bar-fill"/>
      <!-- Percentage Text -->
      <text x="{215 + bar_max_width}" y="16" class="skill-val">{target_pct}%</text>
    </g>""")

    skills_code = "\n".join(skill_rows_svg)
    keyframes_code = "\n".join(keyframe_css_list)

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="{height}">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&amp;display=swap');

      .card-bg {{ fill: #0A0F1F; stroke: #00E5FF; stroke-width: 1.5; stroke-opacity: 0.5; }}
      .title-text {{ font-family: 'JetBrains Mono', monospace; font-size: 11.5px; fill: #5EEAFF; font-weight: bold; }}

      .skill-name {{ font-family: 'JetBrains Mono', monospace; font-size: 13px; fill: #FFFFFF; font-weight: 600; }}
      .skill-val {{ font-family: 'JetBrains Mono', monospace; font-size: 12px; fill: #00FFB3; font-weight: bold; }}

      .bar-bg {{ fill: #050816; stroke: #00E5FF; stroke-opacity: 0.25; stroke-width: 0.8; }}
      .bar-fill {{
        fill: url(#skillGrad);
        width: 0px;
      }}

      {keyframes_code}

      .scanline {{
        fill: url(#skillScanline);
        opacity: 0.12;
        pointer-events: none;
      }}
    </style>

    <linearGradient id="skillGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00C8FF"/>
      <stop offset="60%" stop-color="#00E5FF"/>
      <stop offset="100%" stop-color="#00FFB3"/>
    </linearGradient>

    <pattern id="skillScanline" width="100" height="4" patternUnits="userSpaceOnUse">
      <line x1="0" y1="0" x2="100" y2="0" stroke="#000000" stroke-width="1.5" opacity="0.3" />
    </pattern>

    <filter id="skillGlow" x="-10%" y="-10%" width="120%" height="120%">
      <feGaussianBlur stdDeviation="2" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>

  <!-- Base Card -->
  <rect x="4" y="4" width="{width - 8}" height="{height - 8}" rx="10" ry="10" class="card-bg" filter="url(#skillGlow)"/>

  <!-- Header Bar -->
  <path d="M 4 14 Q 4 4 14 4 L {width - 14} 4 Q {width - 4} 4 {width - 4} 14 L {width - 4} 40 L 4 40 Z" fill="#050816"/>
  <line x1="4" y1="40" x2="{width - 4}" y2="40" stroke="#00E5FF" stroke-opacity="0.3" stroke-width="1"/>

  <circle cx="20" cy="22" r="4.5" fill="#FF5F56"/>
  <circle cx="34" cy="22" r="4.5" fill="#FFBD2E"/>
  <circle cx="48" cy="22" r="4.5" fill="#27C93F"/>

  <text x="{width // 2}" y="26" text-anchor="middle" class="title-text">shyguy6479@AI-OS:~ // TECHNICAL_SKILLS_MATRIX</text>

  <!-- Skill Rows -->
  {skills_code}

  <!-- Scanline Overlay -->
  <rect x="4" y="4" width="{width - 8}" height="{height - 8}" rx="10" ry="10" class="scanline"/>
</svg>
"""

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content.strip())
    print(f"✅ Generated skill dashboard SVG: {output_path}")


if __name__ == "__main__":
    generate_skill_svg()
