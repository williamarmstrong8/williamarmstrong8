#!/usr/bin/env python3
"""Generate README SVGs matching williamarmstrong.vercel.app. Run: python3 scripts/build.py"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)
for old in OUT.glob("*.svg"):
    old.unlink()

# Tokens from the portfolio's :root
BG = "#F8FAFA"        # hsl(196 18% 98%)
CARD = "#F3F5F6"      # hsl(196 15% 96%)
FG = "#000000"
MUTED = "#737373"     # hsl(0 0% 45%)
BORDER = "#EDF0F1"    # hsl(196 10% 94%)
BLUE = "#0036B3"      # hsl(225 100% 35%)
TEAL = "#2894C0"      # hsl(196 67% 45%)
SANS = "Inter, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
SERIF = "Merriweather, Georgia, 'Times New Roman', serif"
W = 1200

GRAD = f'''<linearGradient id="g" x1="0" x2="1">
      <stop offset="0%" stop-color="{BLUE}"/><stop offset="100%" stop-color="{TEAL}"/>
    </linearGradient>'''


def hero():
    h = 420
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}">
  <defs>{GRAD}</defs>
  <rect x=".5" y=".5" width="{W-1}" height="{h-1}" fill="{BG}" stroke="{BORDER}"/>

  <!-- pill -->
  <rect x="72.5" y="72.5" width="196" height="33" rx="16.5" fill="none" stroke="{BORDER}"/>
  <circle cx="94" cy="89" r="4" fill="{BLUE}">
    <animate attributeName="opacity" values="1;.3;1" dur="2.4s" repeatCount="indefinite"/>
  </circle>
  <text x="108" y="94" font-family="{SANS}" font-size="13" font-weight="500" fill="{MUTED}">Engineer &amp; Entrepreneur</text>

  <text x="68" y="222" font-family="{SANS}" font-size="96" font-weight="700" letter-spacing="-4" fill="{FG}">William Armstrong</text>

  <!-- gradient rule that draws in and rests -->
  <rect x="72" y="256" width="0" height="3" fill="url(#g)">
    <animate attributeName="width" values="0;120;120" keyTimes="0;.25;1" dur="6s" repeatCount="indefinite"/>
  </rect>

  <text x="72" y="310" font-family="{SANS}" font-size="20" fill="{MUTED}">Launched 4 startups  •  automated a $50k workflow  •  2M+ community engagement</text>
  <text x="72" y="350" font-family="{SERIF}" font-style="italic" font-size="17" fill="{FG}">Solutions Engineer at Vercel. Human-centered, systems-first. San Francisco.</text>
</svg>
'''


WORK = [
    ("Club Pack", "Startup", "One place to run a social club: events, RSVPs, sites, analytics."),
    ("Happy Mile Run Club", "Startup", "A free, social San Francisco run club grown with local partners."),
    ("Mod Brew", "Startup", "A speakeasy-style campus coffee pop-up."),
    ("Cue", "iOS", "A teleprompter that follows your voice and records to camera roll."),
    ("Hearthboard", "iPad + Pi", "A native iPad command center for a Raspberry Pi homelab."),
    ("JARVIS", "Agent", "A personal home agent."),
]


def work():
    top, rh = 120, 64
    h = top + rh * len(WORK) + 48
    rows = []
    for i, (name, tag, desc) in enumerate(WORK):
        y = top + i * rh
        rows.append(f'''
  <path d="M72 {y+.5}H{W-72}" stroke="{BORDER}"/>
  <text x="72" y="{y+40}" font-family="{SANS}" font-size="13" fill="{MUTED}">0{i+1}</text>
  <text x="120" y="{y+40}" font-family="{SANS}" font-size="19" font-weight="600" fill="{FG}">{escape(name)}</text>
  <text x="400" y="{y+40}" font-family="{SANS}" font-size="16" fill="{MUTED}">{escape(desc)}</text>
  <text x="{W-72}" y="{y+40}" text-anchor="end" font-family="{SANS}" font-size="13" font-weight="500" fill="{BLUE}">{escape(tag)}</text>''')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}">
  <rect x=".5" y=".5" width="{W-1}" height="{h-1}" fill="{BG}" stroke="{BORDER}"/>
  <text x="72" y="84" font-family="{SANS}" font-size="32" font-weight="700" letter-spacing="-1" fill="{FG}">Selected work</text>
  <text x="{W-72}" y="84" text-anchor="end" font-family="{SERIF}" font-style="italic" font-size="15" fill="{MUTED}">Signal to solution.</text>
  {"".join(rows)}
  <path d="M72 {top+rh*len(WORK)+.5}H{W-72}" stroke="{BORDER}"/>
</svg>
'''


(OUT / "hero.svg").write_text(hero())
(OUT / "work.svg").write_text(work())
print("built", sorted(p.name for p in OUT.glob("*.svg")))
