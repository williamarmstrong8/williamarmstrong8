#!/usr/bin/env python3
"""Generate light and dark README SVGs. Run: python3 scripts/build.py"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

FONT = "Geist, 'Geist Sans', Inter, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "'Geist Mono', ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

THEMES = {
    "dark": dict(bg="#000000", fg="#EDEDED", muted="#A1A1A1", subtle="#1F1F1F", line="#2E2E2E", btn_bg="#EDEDED", btn_fg="#0A0A0A"),
    "light": dict(bg="#FFFFFF", fg="#171717", muted="#666666", subtle="#F2F2F2", line="#EBEBEB", btn_bg="#171717", btn_fg="#FFFFFF"),
}

W = 1200


def grid(t, h, step=60):
    lines = [f'<path d="M{x} 0V{h}" />' for x in range(0, W + 1, step)]
    lines += [f'<path d="M0 {y}H{W}" />' for y in range(0, h + 1, step)]
    return f'<g stroke="{t["line"]}" stroke-width="1" opacity=".55">{"".join(lines)}</g>'


def hero(t):
    h = 480
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}">
  <defs>
    <radialGradient id="fade" cx="50%" cy="45%" r="60%">
      <stop offset="0%" stop-color="{t["bg"]}" stop-opacity="0"/>
      <stop offset="100%" stop-color="{t["bg"]}" stop-opacity="1"/>
    </radialGradient>
    <linearGradient id="beam" x1="0" x2="1">
      <stop offset="0%" stop-color="{t["fg"]}" stop-opacity="0"/>
      <stop offset="50%" stop-color="{t["fg"]}" stop-opacity=".9"/>
      <stop offset="100%" stop-color="{t["fg"]}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="vbeam" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{t["fg"]}" stop-opacity="0"/>
      <stop offset="50%" stop-color="{t["fg"]}" stop-opacity=".9"/>
      <stop offset="100%" stop-color="{t["fg"]}" stop-opacity="0"/>
    </linearGradient>
    <style>
    </style>
  </defs>
  <rect width="{W}" height="{h}" fill="{t["bg"]}"/>
  {grid(t, h)}
  <rect width="{W}" height="{h}" fill="url(#fade)"/>

  <!-- light travelling along the grid -->
  <rect y="119.5" width="180" height="1.5" fill="url(#beam)">
    <animate attributeName="x" values="-180;{W}" dur="6s" repeatCount="indefinite"/>
  </rect>
  <rect y="359.5" width="180" height="1.5" fill="url(#beam)">
    <animate attributeName="x" values="{W};-180" dur="7s" begin="1.5s" repeatCount="indefinite"/>
  </rect>
  <rect x="179.5" width="1.5" height="140" fill="url(#vbeam)">
    <animate attributeName="y" values="-140;{h}" dur="5s" begin="1s" repeatCount="indefinite"/>
  </rect>
  <rect x="1019.5" width="1.5" height="140" fill="url(#vbeam)">
    <animate attributeName="y" values="{h};-140" dur="5.5s" begin="2.5s" repeatCount="indefinite"/>
  </rect>

  <!-- grid-intersection crosses -->
  <g stroke="{t["muted"]}" stroke-width="1">
    <path d="M174 120h12M180 114v12"/><path d="M1014 360h12M1020 354v12"/>
  </g>

  <g text-anchor="middle">
    <g class="in d1">
      <rect x="490" y="104" width="220" height="32" rx="16" fill="{t["bg"]}" stroke="{t["line"]}"/>
      <circle cx="514" cy="120" r="4" fill="#45DEC4"><animate attributeName="opacity" values="1;.35;1" dur="2s" repeatCount="indefinite"/></circle>
      <text x="610" y="125" font-family="{MONO}" font-size="13" fill="{t["muted"]}">williamarmstrong8</text>
    </g>
    <g class="in d2" font-family="{FONT}" font-weight="600" fill="{t["fg"]}" letter-spacing="-3.2">
      <text x="600" y="222" font-size="68">Build the idea.</text>
      <text x="600" y="300" font-size="68">Ship the product.</text>
    </g>
    <g class="in d3" font-family="{FONT}" font-size="20" fill="{t["muted"]}">
      <text x="600" y="358">William Armstrong — builder and engineer, from idea to shipped.</text>
    </g>
  </g>
</svg>
'''


def button(t, label, primary, width):
    h = 48
    bg = t["btn_bg"] if primary else t["bg"]
    fg = t["btn_fg"] if primary else t["fg"]
    stroke = "none" if primary else t["line"]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{h}" viewBox="0 0 {width} {h}">
  <rect x=".5" y=".5" width="{width-1}" height="{h-1}" rx="24" fill="{bg}" stroke="{stroke}"/>
  <text x="{width/2}" y="30" text-anchor="middle" font-family="{FONT}" font-size="16" font-weight="500" fill="{fg}">{label}</text>
</svg>
'''


FEATURES = [
    ("01", "Idea", "Start with the problem.", "Find the sharpest version", "worth building."),
    ("02", "Design", "Interfaces that feel obvious.", "Clear hierarchy, nothing", "extra."),
    ("03", "Build", "Full stack, end to end.", "Frontend, backend, data,", "and everything between."),
    ("04", "AI", "Products with intelligence.", "Models and agents wired into", "real workflows."),
    ("05", "Ship", "Zero to production, fast.", "Small releases, short loops,", "real users early."),
    ("06", "Scale", "Grow without rewrites.", "Foundations that hold up", "from MVP onward."),
]


def features(t):
    cols, cw, ch, top = 3, 400, 200, 140
    h = top + ch * 2 + 1
    cells = []
    for i, (num, title, lead, l1, l2) in enumerate(FEATURES):
        x, y = (i % cols) * cw, top + (i // cols) * ch
        delay = 0.1 + i * 0.12
        cells.append(f'''
  <g class="cell" style="animation-delay:{delay:.2f}s">
    <text x="{x+32}" y="{y+48}" font-family="{MONO}" font-size="13" fill="{t["muted"]}">{num}</text>
    <text x="{x+32}" y="{y+92}" font-family="{FONT}" font-size="22" font-weight="600" letter-spacing="-.6" fill="{t["fg"]}">{title}</text>
    <text x="{x+32}" y="{y+124}" font-family="{FONT}" font-size="16" fill="{t["fg"]}">{lead}</text>
    <text x="{x+32}" y="{y+150}" font-family="{FONT}" font-size="16" fill="{t["muted"]}">{l1}</text>
    <text x="{x+32}" y="{y+172}" font-family="{FONT}" font-size="16" fill="{t["muted"]}">{l2}</text>
  </g>''')
    g = t["line"]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}">
  <style>
  </style>
  <rect width="{W}" height="{h}" fill="{t["bg"]}"/>
  <text x="0" y="56" font-family="{FONT}" font-size="40" font-weight="600" letter-spacing="-2" fill="{t["fg"]}">A unified approach for 0 → shipped</text>
  <text x="0" y="96" font-family="{FONT}" font-size="18" fill="{t["muted"]}">One person across the whole loop, so nothing gets lost in handoff.</text>
  <g fill="none" stroke="{g}">
    <rect x=".5" y="{top+.5}" width="{W-1}" height="{ch*2}"/>
    <path d="M400 {top}V{h}M800 {top}V{h}M0 {top+ch+.5}H{W}"/>
  </g>
  <rect x="0" y="{top}" width="120" height="1.5" fill="{t["fg"]}" opacity=".8">
    <animate attributeName="x" values="-120;{W}" dur="5s" repeatCount="indefinite"/>
  </rect>
  {"".join(cells)}
</svg>
'''


def cta(t):
    h = 220
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}">
  <rect x=".5" y=".5" width="{W-1}" height="{h-1}" rx="12" fill="{t["bg"]}" stroke="{t["line"]}"/>
  <g opacity=".6">{grid(t, h, 40).replace('opacity=".55"', 'opacity=".35"')}</g>
  <rect x=".5" y=".5" width="{W-1}" height="{h-1}" rx="12" fill="none" stroke="{t["line"]}"/>
  <g text-anchor="middle" font-family="{FONT}">
    <text x="600" y="100" font-size="40" font-weight="600" letter-spacing="-2" fill="{t["fg"]}">Building something?</text>
    <text x="600" y="142" font-size="18" fill="{t["muted"]}">I'd love to hear about it. The fastest way to reach me is LinkedIn.</text>
  </g>
</svg>
'''


for name, t in THEMES.items():
    (OUT / f"hero-{name}.svg").write_text(hero(t))
    (OUT / f"features-{name}.svg").write_text(features(t))
    (OUT / f"cta-{name}.svg").write_text(cta(t))
    (OUT / f"btn-linkedin-{name}.svg").write_text(button(t, "Connect on LinkedIn", True, 200))
    (OUT / f"btn-github-{name}.svg").write_text(button(t, "View GitHub", False, 140))

print("built", sorted(p.name for p in OUT.glob("*.svg")))
