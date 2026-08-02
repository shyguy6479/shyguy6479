#!/usr/bin/env python3
"""
generate_projects_svg.py
------------------------
Generates assets/projects.svg - an animated Cyberpunk terminal project dashboard
for shyguy6479.

Features:
- Simulated terminal command execution: `$ ls -la ~/projects/`
- Projects featured:
  1. 🤖 AVO AI (Autonomous Agent System)
  2. 🏥 Medical AI Assistant (Diagnostic Intelligence)
  3. 🧠 AI Codebase Analyzer (Static Analysis & Refactoring)
  4. 🎥 AI Video Editor (Automated Clip Generation)
  5. 📄 Resume Builder AI (LLM Tailored Formatting)
- One-by-one sequential card entry animation with glowing neon highlights.
- 100% SVG/CSS standard compatible.
"""

import os


def generate_projects_svg(output_path: str = "assets/projects.svg") -> None:
    width = 850
    height = 420

    projects = [
        {
            "icon": "🤖",
            "name": "AVO AI",
            "type": "Autonomous Agentic AI Framework",
            "stack": "Python • LangChain • FastAPI • PyTorch",
            "status": "ACTIVE",
            "status_color": "#00FFB3"
        },
        {
            "icon": "🏥",
            "name": "Medical AI Assistant",
            "type": "Clinical Intelligence & Diagnostics",
            "stack": "Python • TensorFlow • OpenCV • React",
            "status": "DEPLOYED",
            "status_color": "#00E5FF"
        },
        {
            "icon": "🧠",
            "name": "AI Codebase Analyzer",
            "type": "AST Parser & LLM Refactoring Engine",
            "stack": "Python • Tree-sitter • Supabase • FastAPI",
            "status": "ACTIVE",
            "status_color": "#00FFB3"
        },
        {
            "icon": "🎥",
            "name": "AI Video Editor",
            "type": "Automated Scene Detection & Highlight Clips",
            "stack": "Python • OpenCV • FFmpeg • PyTorch",
            "status": "BETA",
            "status_color": "#FFBD2E"
        },
        {
            "icon": "📄",
            "name": "Resume Builder AI",
            "type": "Smart Tailored Resume & Portfolio Synthesizer",
            "stack": "React • Node.js • Firebase • Gemini API",
            "status": "STABLE",
            "status_color": "#00E5FF"
        }
    ]

    cards_svg_list = []
    card_height = 54
    card_gap = 12
    start_y = 80

    for idx, proj in enumerate(projects):
        y_pos = start_y + idx * (card_height + card_gap)
        delay = round(0.3 + (idx * 0.3), 2)

        cards_svg_list.append(f"""
    <g id="proj-card-{idx}" class="project-card" style="animation-delay: {delay}s;" transform="translate(24, {y_pos})">
      <rect width="802" height="{card_height}" rx="8" class="card-box"/>
      <text x="18" y="32" class="proj-icon">{proj['icon']}</text>
      <text x="52" y="32" class="proj-title">{proj['name']}</text>
      <text x="260" y="32" class="proj-type">{proj['type']}</text>
      <text x="540" y="32" class="proj-stack">{proj['stack']}</text>
      <rect x="710" y="16" width="75" height="22" rx="4" fill="#050816" stroke="{proj['status_color']}" stroke-width="0.8"/>
      <text x="747.5" y="31" text-anchor="middle" class="status-text" fill="{proj['status_color']}">{proj['status']}</text>
    </g>""")

    cards_svg = "\n".join(cards_svg_list)

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="{height}">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&amp;display=swap');

      .card-bg {{ fill: #0A0F1F; stroke: #00E5FF; stroke-width: 1.5; stroke-opacity: 0.5; }}
      .header-bg {{ fill: #050816; }}
      .title-text {{ font-family: 'JetBrains Mono', monospace; font-size: 11.5px; fill: #5EEAFF; font-weight: bold; }}
      .cmd-text {{ font-family: 'JetBrains Mono', monospace; font-size: 13px; fill: #00FFB3; font-weight: bold; }}

      .card-box {{ fill: #050816; stroke: #00E5FF; stroke-opacity: 0.3; stroke-width: 1; }}
      .project-card {{
        opacity: 0;
        transform: translateY(8px);
        animation: slideIn 0.4s ease-out forwards;
      }}

      .proj-icon {{ font-size: 18px; }}
      .proj-title {{ font-family: 'JetBrains Mono', monospace; font-size: 14px; fill: #FFFFFF; font-weight: bold; }}
      .proj-type {{ font-family: 'JetBrains Mono', monospace; font-size: 11px; fill: #B5C7FF; }}
      .proj-stack {{ font-family: 'JetBrains Mono', monospace; font-size: 10.5px; fill: #5EEAFF; opacity: 0.85; }}
      .status-text {{ font-family: 'JetBrains Mono', monospace; font-size: 9.5px; font-weight: bold; letter-spacing: 0.5px; }}

      @keyframes slideIn {{
        0% {{ opacity: 0; transform: translateY(8px); }}
        100% {{ opacity: 1; transform: translateY(0); }}
      }}

      .scanline {{
        fill: url(#projScanline);
        opacity: 0.12;
        pointer-events: none;
      }}
    </style>

    <pattern id="projScanline" width="100" height="4" patternUnits="userSpaceOnUse">
      <line x1="0" y1="0" x2="100" y2="0" stroke="#000000" stroke-width="1.5" opacity="0.3" />
    </pattern>

    <filter id="projGlow" x="-10%" y="-10%" width="120%" height="120%">
      <feGaussianBlur stdDeviation="2" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>

  <!-- Container -->
  <rect x="4" y="4" width="{width - 8}" height="{height - 8}" rx="10" ry="10" class="card-bg" filter="url(#projGlow)"/>

  <!-- Header -->
  <path d="M 4 14 Q 4 4 14 4 L {width - 14} 4 Q {width - 4} 4 {width - 4} 14 L {width - 4} 40 L 4 40 Z" fill="#050816"/>
  <line x1="4" y1="40" x2="{width - 4}" y2="40" stroke="#00E5FF" stroke-opacity="0.3" stroke-width="1"/>

  <circle cx="20" cy="22" r="4.5" fill="#FF5F56"/>
  <circle cx="34" cy="22" r="4.5" fill="#FFBD2E"/>
  <circle cx="48" cy="22" r="4.5" fill="#27C93F"/>

  <text x="{width // 2}" y="26" text-anchor="middle" class="title-text">shyguy6479@AI-OS:~ // PROJECT_CATALOG</text>

  <!-- Terminal Command Prompt -->
  <text x="24" y="65" class="cmd-text">$ ls -la --sort=priority ~/projects/</text>

  <!-- Project Cards -->
  {cards_svg}

  <!-- Scanlines Overlay -->
  <rect x="4" y="4" width="{width - 8}" height="{height - 8}" rx="10" ry="10" class="scanline"/>
</svg>
"""

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content.strip())
    print(f"✅ Generated projects SVG: {output_path}")


if __name__ == "__main__":
    generate_projects_svg()
