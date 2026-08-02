#!/usr/bin/env python3
"""
render_heatmap_svg.py
---------------------
Reads data/contributions.json and renders assets/contribution-graph.svg - a futuristic
Cyberpunk contribution heatmap graph for shyguy6479.

Features:
- 52-week contribution matrix with animated diagonal entry.
- Cyberpunk color scheme (#0A0F1F -> #004D40 -> #00C8FF -> #00FFB3).
- System Metrics Footer (Total, Current Streak, Longest Streak, Best Day).
- 100% SVG/CSS compliant with GitHub SVG sanitizer.
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List


def render_heatmap_svg(
    json_path: str = "data/contributions.json",
    output_path: str = "assets/contribution-graph.svg"
) -> None:
    if not os.path.exists(json_path):
        from fetch_contributions import save_contributions_json
        save_contributions_json(json_path)

    with open(json_path, "r", encoding="utf-8") as f:
        data: Dict[str, Any] = json.load(f)

    days: List[Dict[str, Any]] = data.get("days", [])
    total_commits = data.get("total_contributions", 0)
    current_streak = data.get("current_streak", 0)
    longest_streak = data.get("longest_streak", 0)
    best_day = data.get("best_day", {"date": "N/A", "count": 0})

    width = 850
    height = 290
    tile_size = 11
    tile_gap = 3.5
    grid_x_start = 45
    grid_y_start = 75

    # Group days into 52 weeks x 7 days
    weeks: List[List[Dict[str, Any]]] = []
    current_week: List[Dict[str, Any]] = []

    for d in days:
        current_week.append(d)
        if len(current_week) == 7:
            weeks.append(current_week)
            current_week = []
    if current_week:
        weeks.append(current_week)

    # Color level mapping
    color_map = {
        0: "#0F172A", # Dark grid space
        1: "#004D40", # Soft teal
        2: "#009688", # Vibrant cyan-green
        3: "#00E5FF", # Bright Cyber Cyan
        4: "#00FFB3"  # Neon Cyber Emerald
    }

    # Generate matrix SVG elements
    tiles_svg_list = []
    for col_idx, week in enumerate(weeks):
        for row_idx, day_info in enumerate(week):
            x = grid_x_start + col_idx * (tile_size + tile_gap)
            y = grid_y_start + row_idx * (tile_size + tile_gap)
            level = day_info.get("level", 0)
            count = day_info.get("count", 0)
            date_str = day_info.get("date", "")
            color = color_map.get(level, color_map[0])
            border_color = "#00E5FF" if level > 2 else ("#1E293B" if level == 0 else "#00FFB3")
            border_opacity = "0.6" if level > 2 else "0.3"

            # Delay calculated diagonally for wave animation
            anim_delay = round((col_idx * 0.03) + (row_idx * 0.02), 2)

            tiles_svg_list.append(
                f'<rect x="{x:.1f}" y="{y:.1f}" width="{tile_size}" height="{tile_size}" rx="2.5" '
                f'fill="{color}" stroke="{border_color}" stroke-opacity="{border_opacity}" stroke-width="0.6" '
                f'class="tile" style="animation-delay: {anim_delay}s;">'
                f'<title>{date_str}: {count} contributions</title></rect>'
            )

    tiles_svg = "\n    ".join(tiles_svg_list)

    # Month Labels
    month_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    month_labels_svg = []
    # Space month labels evenly across 52 columns
    for idx, m_name in enumerate(month_labels):
        col_pos = int((idx / 12) * len(weeks))
        mx = grid_x_start + col_pos * (tile_size + tile_gap)
        month_labels_svg.append(
            f'<text x="{mx:.1f}" y="{grid_y_start - 10}" class="axis-text">{m_name}</text>'
        )

    # Day of week labels (Mon, Wed, Fri)
    dow_labels = [("Mon", 1), ("Wed", 3), ("Fri", 5)]
    dow_labels_svg = []
    for label, r_idx in dow_labels:
        dy = grid_y_start + r_idx * (tile_size + tile_gap) + 9
        dow_labels_svg.append(
            f'<text x="28" y="{dy:.1f}" text-anchor="end" class="axis-text">{label}</text>'
        )

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="{height}">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&amp;display=swap');

      .card-bg {{ fill: #0A0F1F; stroke: #00E5FF; stroke-width: 1.5; stroke-opacity: 0.5; }}
      .title-text {{ font-family: 'JetBrains Mono', monospace; font-size: 13px; fill: #00E5FF; font-weight: bold; letter-spacing: 1px; }}
      .sub-title {{ font-family: 'JetBrains Mono', monospace; font-size: 11px; fill: #B5C7FF; }}
      .axis-text {{ font-family: 'JetBrains Mono', monospace; font-size: 9.5px; fill: #5EEAFF; opacity: 0.8; }}

      .tile {{
        opacity: 0;
        transform: scale(0.5);
        transform-origin: center;
        animation: tileFade 0.4s ease-out forwards;
      }}

      .stat-card {{ fill: #050816; stroke: #00E5FF; stroke-opacity: 0.3; stroke-width: 1; rx: 6px; }}
      .stat-num {{ font-family: 'JetBrains Mono', monospace; font-size: 15px; fill: #00FFB3; font-weight: bold; }}
      .stat-label {{ font-family: 'JetBrains Mono', monospace; font-size: 9.5px; fill: #B5C7FF; text-transform: uppercase; letter-spacing: 0.5px; }}

      .legend-text {{ font-family: 'JetBrains Mono', monospace; font-size: 9px; fill: #B5C7FF; }}

      @keyframes tileFade {{
        0% {{ opacity: 0; transform: scale(0.4); }}
        100% {{ opacity: 1; transform: scale(1); }}
      }}

      .scanline {{
        fill: url(#heatmapScanline);
        opacity: 0.12;
        pointer-events: none;
      }}
    </style>

    <pattern id="heatmapScanline" width="100" height="4" patternUnits="userSpaceOnUse">
      <line x1="0" y1="0" x2="100" y2="0" stroke="#000000" stroke-width="1.5" opacity="0.3" />
    </pattern>

    <filter id="glow" x="-10%" y="-10%" width="120%" height="120%">
      <feGaussianBlur stdDeviation="2.5" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>

  <!-- Container -->
  <rect x="4" y="4" width="{width - 8}" height="{height - 8}" rx="10" ry="10" class="card-bg" filter="url(#glow)"/>

  <!-- Header -->
  <text x="24" y="32" class="title-text">SYSTEM_ACTIVITY // CONTRIBUTION_MATRIX</text>
  <text x="{width - 24}" y="32" text-anchor="end" class="sub-title">YEAR_RECAP :: <tspan fill="#00FFB3" font-weight="bold">{total_commits} COMMITS</tspan></text>

  <!-- Month & Day Labels -->
  {"".join(month_labels_svg)}
  {"".join(dow_labels_svg)}

  <!-- Heatmap Matrix -->
  <g>
    {tiles_svg}
  </g>

  <!-- Footer Stats Cards -->
  <g transform="translate(24, 200)">
    <!-- Stat 1: Total Commits -->
    <rect x="0" y="0" width="180" height="48" class="stat-card"/>
    <text x="14" y="20" class="stat-label">TOTAL CONTRIBUTIONS</text>
    <text x="14" y="38" class="stat-num">{total_commits}</text>

    <!-- Stat 2: Current Streak -->
    <rect x="195" y="0" width="180" height="48" class="stat-card"/>
    <text x="209" y="20" class="stat-label">CURRENT STREAK</text>
    <text x="209" y="38" class="stat-num">{current_streak} DAYS 🔥</text>

    <!-- Stat 3: Longest Streak -->
    <rect x="390" y="0" width="180" height="48" class="stat-card"/>
    <text x="404" y="20" class="stat-label">LONGEST STREAK</text>
    <text x="404" y="38" class="stat-num">{longest_streak} DAYS ⚡</text>

    <!-- Stat 4: Best Single Day -->
    <rect x="585" y="0" width="216" height="48" class="stat-card"/>
    <text x="599" y="20" class="stat-label">PEAK PERFORMANCE</text>
    <text x="599" y="38" class="stat-num">{best_day.get('count', 0)} COMMITS ({best_day.get('date', 'N/A')[-5:]})</text>
  </g>

  <!-- Legend Bar -->
  <g transform="translate({width - 200}, 180)">
    <text x="-35" y="10" class="legend-text">Less</text>
    <rect x="0" y="1" width="10" height="10" rx="2" fill="{color_map[0]}" stroke="#1E293B" stroke-width="0.5"/>
    <rect x="14" y="1" width="10" height="10" rx="2" fill="{color_map[1]}" stroke="#00FFB3" stroke-width="0.5"/>
    <rect x="28" y="1" width="10" height="10" rx="2" fill="{color_map[2]}" stroke="#00FFB3" stroke-width="0.5"/>
    <rect x="42" y="1" width="10" height="10" rx="2" fill="{color_map[3]}" stroke="#00E5FF" stroke-width="0.5"/>
    <rect x="56" y="1" width="10" height="10" rx="2" fill="{color_map[4]}" stroke="#00E5FF" stroke-width="0.5"/>
    <text x="74" y="10" class="legend-text">More</text>
  </g>

  <!-- Scanline Overlay -->
  <rect x="4" y="4" width="{width - 8}" height="{height - 8}" rx="10" ry="10" class="scanline"/>
</svg>
"""

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content.strip())
    print(f"✅ Rendered contribution graph SVG: {output_path}")


if __name__ == "__main__":
    render_heatmap_svg()
