#!/usr/bin/env python3
"""Generate the README SVGs (amber CRT terminal theme). Run: python3 scripts/build.py"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)
for old in OUT.glob("*.svg"):
    old.unlink()

MONO = "'JetBrains Mono', 'SF Mono', SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
BG, PANEL, AMBER, DIM, FAINT, GREEN = "#0E0B07", "#15110A", "#FFB547", "#B9843A", "#5C4423", "#7CFFB2"
W = 1200

DEFS = f'''<defs>
    <filter id="glow" x="-20%" y="-50%" width="140%" height="200%">
      <feGaussianBlur stdDeviation="2.2" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="bigglow" x="-20%" y="-50%" width="140%" height="200%">
      <feGaussianBlur stdDeviation="7" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse">
      <rect width="4" height="2" fill="#000" opacity=".28"/>
    </pattern>
    <radialGradient id="vignette" cx="50%" cy="50%" r="75%">
      <stop offset="60%" stop-color="#000" stop-opacity="0"/>
      <stop offset="100%" stop-color="#000" stop-opacity=".65"/>
    </radialGradient>
  </defs>'''


def crt_overlay(h):
    return f'''<rect width="{W}" height="{h}" fill="url(#scan)" pointer-events="none"/>
  <rect width="{W}" height="{h}" fill="url(#vignette)" pointer-events="none"/>
  <rect y="-80" width="{W}" height="80" fill="{AMBER}" opacity=".035">
    <animate attributeName="y" values="-80;{h}" dur="7s" repeatCount="indefinite"/>
  </rect>'''


# ---------------------------------------------------------------- hero terminal
CYCLE = 18.0  # seconds for one full boot loop

LINES = [
    # (kind, text) kinds: cmd = typed prompt, out = printed, ok = boot line, gap
    ("cmd", "whoami"),
    ("out", "william armstrong · solutions engineer @ vercel · founder · san francisco"),
    ("gap", ""),
    ("cmd", "./boot --fleet"),
    ("ok", ("JARVIS", "personal home agent", "online")),
    ("ok", ("ALFRED", "chat + task bot", "online")),
    ("ok", ("TARS", "humor setting 75%", "online")),
    ("ok", ("HEARTHBOARD", "raspberry pi homelab, ipad cmd center", "online")),
    ("gap", ""),
    ("cmd", "cat ~/receipts.txt"),
    ("out", "4 startups launched  ·  $50k workflow automated  ·  2M+ community engagement"),
]


def hero():
    top, lh, x0 = 268, 30, 64
    h = top + lh * (len(LINES) + 1) + 70
    css, body = [], []
    t = 0.6
    for i, (kind, text) in enumerate(LINES):
        y = top + i * lh
        if kind == "gap":
            t += 0.3
            continue
        start = t / CYCLE * 100
        cls = f"l{i}"
        if kind == "cmd":
            dur = 0.07 * len(text) + 0.2
            end = (t + dur) / CYCLE * 100
            chars = len(text)
            # typed reveal: clip width grows in character steps
            css.append(
                f".{cls} {{ animation: k{i} {CYCLE}s steps(1) infinite; }}"
                f"@keyframes k{i} {{ 0%,{start:.2f}% {{ opacity:0 }} {start+0.01:.2f}%,94% {{ opacity:1 }} 96%,100% {{ opacity:0 }} }}"
                f".c{i} {{ animation: w{i} {CYCLE}s linear infinite; }}"
                f"@keyframes w{i} {{ 0%,{start:.2f}% {{ width:0 }} {end:.2f}%,100% {{ width:{chars*10.9+4:.0f}px }} }}"
            )
            body.append(
                f'<clipPath id="cp{i}"><rect class="c{i}" x="{x0+164}" y="{y-20}" height="28" width="0"/></clipPath>'
                f'<g class="{cls}"><text x="{x0}" y="{y}" fill="{GREEN}">william@sf</text>'
                f'<text x="{x0+118}" y="{y}" fill="{DIM}">~</text><text x="{x0+140}" y="{y}" fill="{AMBER}">$</text>'
                f'<text x="{x0+164}" y="{y}" fill="{AMBER}" clip-path="url(#cp{i})">{escape(text)}</text></g>'
            )
            t += dur + 0.35
        else:
            css.append(
                f".{cls} {{ animation: k{i} {CYCLE}s steps(1) infinite; }}"
                f"@keyframes k{i} {{ 0%,{start:.2f}% {{ opacity:0 }} {start+0.01:.2f}%,94% {{ opacity:1 }} 96%,100% {{ opacity:0 }} }}"
            )
            if kind == "ok":
                name, desc, status = text
                dots = "." * max(3, 44 - len(name) - len(desc))
                body.append(
                    f'<g class="{cls}"><text x="{x0}" y="{y}" fill="{DIM}">[ <tspan fill="{GREEN}">ok</tspan> ]</text>'
                    f'<text x="{x0+110}" y="{y}" fill="{AMBER}" font-weight="700">{name}</text>'
                    f'<text x="{x0+280}" y="{y}" fill="{DIM}">{escape(desc)} <tspan fill="{FAINT}">{dots}</tspan> <tspan fill="{GREEN}">{status}</tspan></text></g>'
                )
                t += 0.45
            else:
                body.append(f'<g class="{cls}"><text x="{x0}" y="{y}" fill="{AMBER}">{escape(text)}</text></g>')
                t += 0.5
    # final prompt + blinking block cursor
    y = top + len(LINES) * lh
    start = t / CYCLE * 100
    css.append(
        f".lend {{ animation: kend {CYCLE}s steps(1) infinite; }}"
        f"@keyframes kend {{ 0%,{start:.2f}% {{ opacity:0 }} {start+0.01:.2f}%,94% {{ opacity:1 }} 96%,100% {{ opacity:0 }} }}"
        ".blink { animation: blink 1s steps(1) infinite; } @keyframes blink { 50% { opacity: 0 } }"
    )
    body.append(
        f'<g class="lend"><text x="{x0}" y="{y}" fill="{GREEN}">william@sf</text>'
        f'<text x="{x0+118}" y="{y}" fill="{DIM}">~</text><text x="{x0+140}" y="{y}" fill="{AMBER}">$</text>'
        f'<rect class="blink" x="{x0+164}" y="{y-19}" width="11" height="24" fill="{AMBER}"/></g>'
    )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}">
  {DEFS}
  <style>
    text {{ font-family: {MONO}; white-space: pre; }}
    .flicker {{ animation: flicker 5s infinite; }}
    @keyframes flicker {{ 0%,100% {{ opacity: 1 }} 47% {{ opacity: 1 }} 48% {{ opacity: .82 }} 49% {{ opacity: 1 }} 72% {{ opacity: .93 }} 73% {{ opacity: 1 }} }}
    @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; opacity: 1 !important; }} }}
    {"".join(css)}
  </style>
  <rect width="{W}" height="{h}" rx="18" fill="{BG}"/>
  <!-- window chrome -->
  <rect width="{W}" height="44" rx="18" fill="{PANEL}"/><rect y="26" width="{W}" height="18" fill="{PANEL}"/>
  <circle cx="30" cy="22" r="6" fill="{FAINT}"/><circle cx="52" cy="22" r="6" fill="{FAINT}"/><circle cx="74" cy="22" r="6" fill="{FAINT}"/>
  <text x="{W/2}" y="28" text-anchor="middle" font-size="14" fill="{DIM}">william@sf: ~ — tty1 — 37.77°N 122.42°W</text>

  <g class="flicker" filter="url(#glow)" font-size="18">
    <text x="64" y="104" font-size="14" fill="{FAINT}">ARMSTRONG-OS v8.0  ·  engineer &amp; entrepreneur</text>
    <g filter="url(#bigglow)">
      <text x="60" y="190" font-size="84" font-weight="800" letter-spacing="-2" fill="{AMBER}">WILLIAM ARMSTRONG</text>
    </g>
    <rect x="64" y="216" width="{W-128}" height="1" fill="{FAINT}"/>
    {"".join(body)}
  </g>
  {crt_overlay(h)}
</svg>
'''


# ---------------------------------------------------------------- shipped modules
MODULES = [
    ("CUE", "ios · swift", "Teleprompter that follows", "your voice as you read."),
    ("HEARTHBOARD", "ipados · python", "iPad command center for", "a Raspberry Pi homelab."),
    ("JARVIS", "agent · python", "Personal home agent that", "runs the house."),
    ("CLUB PACK", "saas · founder", "Everything a social club", "needs, in one place."),
    ("HAPPY MILE", "community · sf", "Viral free SF run club", "built on local partners."),
    ("MOD BREW", "pop-up · founder", "Speakeasy campus coffee", "that sold out in a week."),
]


def modules():
    cols, cw, ch, gap, top = 3, 368, 168, 24, 92
    h = top + ch * 2 + gap + 40
    x_off = (W - (cols * cw + (cols - 1) * gap)) / 2
    cards = []
    for i, (name, tag, l1, l2) in enumerate(MODULES):
        x = x_off + (i % cols) * (cw + gap)
        y = top + (i // cols) * (ch + gap)
        d = (i * 0.37) % 2
        cards.append(f'''
  <g>
    <rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="10" fill="{PANEL}" stroke="{FAINT}"/>
    <path d="M{x+cw-36} {y}h36v0" stroke="{AMBER}"/>
    <g fill="{FAINT}">{"".join(f'<rect x="{x+18+k*9}" y="{y+ch-12}" width="5" height="12"/>' for k in range(10))}</g>
    <circle cx="{x+cw-24}" cy="{y+26}" r="5" fill="{GREEN}">
      <animate attributeName="opacity" values="1;.25;1" dur="2s" begin="{d:.2f}s" repeatCount="indefinite"/>
    </circle>
    <text x="{x+24}" y="{y+34}" font-size="12" fill="{FAINT}">MOD-0{i+1}  ·  {escape(tag)}</text>
    <text x="{x+24}" y="{y+74}" font-size="26" font-weight="800" fill="{AMBER}" filter="url(#glow)">{escape(name)}</text>
    <text x="{x+24}" y="{y+106}" font-size="15" fill="{DIM}">{escape(l1)}</text>
    <text x="{x+24}" y="{y+128}" font-size="15" fill="{DIM}">{escape(l2)}</text>
  </g>''')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}">
  {DEFS}
  <style>text {{ font-family: {MONO}; white-space: pre; }}</style>
  <rect width="{W}" height="{h}" rx="18" fill="{BG}"/>
  <text x="{x_off}" y="56" font-size="18" fill="{GREEN}">william@sf <tspan fill="{DIM}">~</tspan> <tspan fill="{AMBER}">$ ls ~/shipped</tspan></text>
  <text x="{W-x_off}" y="56" text-anchor="end" font-size="13" fill="{FAINT}">6 modules · all systems nominal</text>
  {"".join(cards)}
  {crt_overlay(h)}
</svg>
'''


# ---------------------------------------------------------------- sign-off strip
def signoff():
    h = 120
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}">
  {DEFS}
  <style>text {{ font-family: {MONO}; white-space: pre; }}</style>
  <rect width="{W}" height="{h}" rx="18" fill="{BG}"/>
  <g filter="url(#glow)" text-anchor="middle">
    <text x="600" y="54" font-size="20" fill="{AMBER}">off-screen: running with Happy Mile, shooting photos, rebooting JARVIS.</text>
    <text x="600" y="86" font-size="14" fill="{DIM}">systems-first · human-centered · built in san francisco</text>
  </g>
  {crt_overlay(h)}
</svg>
'''


(OUT / "terminal.svg").write_text(hero())
(OUT / "shipped.svg").write_text(modules())
(OUT / "signoff.svg").write_text(signoff())
print("built", sorted(p.name for p in OUT.glob("*.svg")))
