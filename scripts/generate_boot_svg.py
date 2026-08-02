#!/usr/bin/env python3
"""
generate_boot_svg.py
--------------------
Generates assets/boot-screen.svg - an animated Cyberpunk AI Terminal Boot Screen
for shyguy6479's GitHub profile.

Features:
- Animated line typing sequence with SMIL / CSS keyframes.
- Progress bar filling up to 100%.
- Blinking terminal cursor.
- One-time animation sequence (completes and freezes).
- GitHub-compatible SVG (no JS, no foreignObject).
"""

import os


def generate_boot_svg(output_path: str = "assets/boot-screen.svg") -> None:
    width = 850
    height = 340

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="{height}">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&amp;display=swap');

      .bg {{ fill: #050816; }}
      .card-bg {{ fill: #0A0F1F; stroke: #00E5FF; stroke-width: 1.5; stroke-opacity: 0.6; }}
      .header-bg {{ fill: #0d152d; }}
      .title-text {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 13px; fill: #5EEAFF; font-weight: bold; letter-spacing: 1px; }}
      .status-text {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 11px; fill: #00FFB3; }}
      
      .log-line {{
        font-family: 'JetBrains Mono', 'Fira Code', monospace;
        font-size: 14px;
        fill: #FFFFFF;
        opacity: 0;
        animation: fadeIn 0.4s ease-out forwards;
      }}
      .tag {{ font-weight: bold; }}
      .tag-sys {{ fill: #00E5FF; }}
      .tag-mod {{ fill: #5EEAFF; }}
      .tag-vis {{ fill: #B5C7FF; }}
      .tag-mem {{ fill: #00FFB3; }}
      .tag-net {{ fill: #00C8FF; }}
      .tag-ok  {{ fill: #00FFB3; font-weight: bold; }}

      .progress-bg {{ fill: #0d1730; rx: 4px; ry: 4px; }}
      .progress-bar {{
        fill: url(#progressGradient);
        rx: 4px; ry: 4px;
        width: 0px;
        animation: fillProgress 3.5s cubic-bezier(0.1, 0.7, 0.1, 1) 0.5s forwards;
      }}
      .progress-text {{
        font-family: 'JetBrains Mono', 'Fira Code', monospace;
        font-size: 12px;
        fill: #00E5FF;
        font-weight: bold;
      }}

      .cursor {{
        fill: #00E5FF;
        animation: blink 0.8s infinite alternate;
      }}

      .scanline {{
        fill: url(#scanlinePattern);
        opacity: 0.15;
        pointer-events: none;
      }}

      .grid-pattern {{
        stroke: #00E5FF;
        stroke-width: 0.5;
        stroke-opacity: 0.07;
      }}

      /* Delay Timings for Line Reveal */
      #line1 {{ animation-delay: 0.3s; }}
      #line2 {{ animation-delay: 0.9s; }}
      #line3 {{ animation-delay: 1.5s; }}
      #line4 {{ animation-delay: 2.1s; }}
      #line5 {{ animation-delay: 2.7s; }}
      #line6 {{ animation-delay: 3.3s; }}

      @keyframes fadeIn {{
        0% {{ opacity: 0; transform: translateY(4px); }}
        100% {{ opacity: 1; transform: translateY(0); }}
      }}

      @keyframes fillProgress {{
        0% {{ width: 0px; }}
        100% {{ width: 730px; }}
      }}

      @keyframes blink {{
        0% {{ opacity: 1; }}
        100% {{ opacity: 0; }}
      }}
    </style>

    <linearGradient id="progressGradient" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00C8FF" />
      <stop offset="50%" stop-color="#00E5FF" />
      <stop offset="100%" stop-color="#00FFB3" />
    </linearGradient>

    <pattern id="scanlinePattern" width="100" height="4" patternUnits="userSpaceOnUse">
      <line x1="0" y1="0" x2="100" y2="0" stroke="#000000" stroke-width="1.5" opacity="0.3" />
    </pattern>

    <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
      <path d="M 20 0 L 0 0 0 20" fill="none" class="grid-pattern"/>
    </pattern>

    <filter id="neonGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>

  <!-- Base Card Background -->
  <rect x="5" y="5" width="{width - 10}" height="{height - 10}" rx="10" ry="10" class="card-bg" filter="url(#neonGlow)"/>
  <rect x="6" y="6" width="{width - 12}" height="{height - 12}" rx="9" ry="9" fill="url(#grid)"/>
  
  <!-- Terminal Header Bar -->
  <path d="M 6 15 Q 6 6 15 6 L {width - 15} 6 Q {width - 6} 6 {width - 6} 15 L {width - 6} 42 L 6 42 Z" class="header-bg"/>
  <line x1="6" y1="42" x2="{width - 6}" y2="42" stroke="#00E5FF" stroke-opacity="0.4" stroke-width="1"/>

  <!-- Window Controls -->
  <circle cx="24" cy="24" r="5.5" fill="#FF5F56"/>
  <circle cx="42" cy="24" r="5.5" fill="#FFBD2E"/>
  <circle cx="60" cy="24" r="5.5" fill="#27C93F"/>

  <!-- Window Title -->
  <text x="{width // 2}" y="28" text-anchor="middle" class="title-text">shyguy6479@AI-OS:~ // BOOT_SEQUENCE</text>
  <text x="{width - 25}" y="28" text-anchor="end" class="status-text">[ ONLINE ]</text>

  <!-- Terminal Output Logs -->
  <g transform="translate(30, 70)">
    <text id="line1" y="0" class="log-line">
      <tspan class="tag tag-sys">[SYS_INIT]</tspan> Initializing AI Core...
    </text>

    <text id="line2" y="30" class="log-line">
      <tspan class="tag tag-mod">[NEURAL]</tspan> Loading Neural Network... <tspan fill="#00FFB3">[OK]</tspan>
    </text>

    <text id="line3" y="60" class="log-line">
      <tspan class="tag tag-vis">[VISION]</tspan> Loading Vision Models... <tspan fill="#00FFB3">[OK]</tspan>
    </text>

    <text id="line4" y="90" class="log-line">
      <tspan class="tag tag-mem">[MEMORY]</tspan> Loading Memory... <tspan fill="#00FFB3">[OK]</tspan>
    </text>

    <text id="line5" y="120" class="log-line">
      <tspan class="tag tag-net">[NET_SYNC]</tspan> Connecting GitHub...
    </text>

    <text id="line6" y="150" class="log-line">
      <tspan class="tag tag-ok">[SUCCESS]</tspan> Connected :: Welcome, User <tspan font-weight="bold" fill="#00E5FF">shyguy6479</tspan>
      <rect x="360" y="-12" width="10" height="16" class="cursor"/>
    </text>
  </g>

  <!-- Progress Bar Container -->
  <g transform="translate(30, 260)">
    <text x="0" y="-10" class="progress-text">SYSTEM BOOT PROGRESS</text>
    <text x="730" y="-10" text-anchor="end" class="progress-text">100%</text>
    <rect x="0" y="0" width="730" height="14" class="progress-bg"/>
    <rect x="0" y="0" height="14" class="progress-bar"/>
  </g>

  <!-- Scanlines Overlay -->
  <rect x="6" y="6" width="{width - 12}" height="{height - 12}" rx="9" ry="9" class="scanline"/>
</svg>
"""

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content.strip())
    print(f"✅ Generated boot screen SVG: {output_path}")


if __name__ == "__main__":
    generate_boot_svg()
