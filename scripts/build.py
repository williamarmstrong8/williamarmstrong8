#!/usr/bin/env python3
"""Build the storytelling README chapters as animated SVGs.

Run: python3 scripts/build.py
Preview a moment:  python3 scripts/build.py --at 9  (writes /tmp/preview-<t>.svg frozen at t seconds)
"""
import base64
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"
OUT.mkdir(exist_ok=True)

W, H = 1200, 630
T = 18.0  # loop length, seconds

YELLOW = "#FFC72C"
INK = "#111111"
HEATHER = "#E9E8E6"
WHITE = "#FFFFFF"
HEAVY = "'Archivo Black', 'Arial Black', 'Helvetica Neue', Arial, sans-serif"
SERIF = "Georgia, 'Times New Roman', serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

FADE = 0.45  # seconds


def pct(s):
    return f"{max(0.0, min(100.0, s / T * 100)):.3f}%"


def window(name, a, b, fade=FADE):
    """opacity 1 between a..b seconds, fading in/out."""
    if a <= 0:
        return (f"@keyframes {name} {{ 0%,{pct(b - fade)} {{ opacity:1 }} {pct(b)},{pct(T - fade)} {{ opacity:0 }} 100% {{ opacity:1 }} }}")
    return (f"@keyframes {name} {{ 0%,{pct(a)} {{ opacity:0 }} {pct(a + fade)},{pct(b - fade)} {{ opacity:1 }} {pct(b)},100% {{ opacity:0 }} }}")


def enter(name, a, b, frm, to="translate(0,0)", dur=0.6):
    """element moves in at a, stays until b, then resets (hidden by its scene)."""
    return (f"@keyframes {name} {{ 0%,{pct(a)} {{ opacity:0; transform:{frm} }} "
            f"{pct(a + dur)},{pct(b)} {{ opacity:1; transform:{to} }} 100% {{ opacity:0; transform:{frm} }} }}")


def anim(cls, name):
    return f".{cls} {{ animation: {name} {T}s linear infinite; }}"


def smiley(r=110):
    """Happy Mile smiley: yellow face, slanted eyes, wide grin, sparkles."""
    return f'''
    <circle r="{r}" fill="{YELLOW}" stroke="{INK}" stroke-width="{r*0.06:.1f}"/>
    <path d="M{-r*.42:.1f} {-r*.42:.1f} l{r*.18:.1f} {-r*.04:.1f} l{-r*.02:.1f} {r*.42:.1f} l{-r*.16:.1f} {-r*.08:.1f}z" fill="{INK}" transform="rotate(-18)"/>
    <path d="M{r*.10:.1f} {-r*.50:.1f} l{r*.18:.1f} {-r*.04:.1f} l{-r*.02:.1f} {r*.42:.1f} l{-r*.16:.1f} {-r*.08:.1f}z" fill="{INK}" transform="rotate(-18)"/>
    <path d="M{-r*.62:.1f} {r*.05:.1f} Q{-r*.05:.1f} {r*.95:.1f} {r*.66:.1f} {-r*.12:.1f}" fill="none" stroke="{INK}" stroke-width="{r*.09:.1f}" stroke-linecap="round"/>
    <path d="M{r*.78:.1f} {-r*.95:.1f} l6 14 14 6 -14 6 -6 14 -6 -14 -14 -6 14 -6z" fill="{WHITE}" stroke="{INK}" stroke-width="2"/>
    <path d="M{-r*1.02:.1f} {r*.55:.1f} l4 10 10 4 -10 4 -4 10 -4 -10 -10 -4 10 -4z" fill="{WHITE}" stroke="{INK}" stroke-width="2"/>'''


def chapter_one(at=None):
    tee = base64.b64encode((ROOT / "scripts" / "media" / "happymile-tee.jpg").read_bytes()).decode()
    css = []
    scenes = [  # (class, start, end)
        ("s1", 0.0, 3.4),
        ("s2", 3.4, 7.4),
        ("s3", 7.4, 11.0),
        ("s4", 11.0, 14.6),
        ("s5", 14.6, T),
    ]
    for cls, a, b in scenes:
        css += [window(f"k{cls}", a, b), anim(cls, f"k{cls}")]

    # scene 1 beats
    css += [enter("k1a", 0.2, 3.4, "translate(0,14px)"), anim("b1a", "k1a"),
            enter("k1b", 0.8, 3.4, "translate(0,14px)"), anim("b1b", "k1b"),
            enter("k1c", 1.5, 3.4, "translate(0,14px)"), anim("b1c", "k1c")]
    # scene 2 beats: price tags appear, then get struck, then the answer
    for i in range(3):
        css += [enter(f"k2t{i}", 4.0 + i * 0.3, 7.4, "translate(0,16px)"), anim(f"b2t{i}", f"k2t{i}")]
        css.append(f"@keyframes k2s{i} {{ 0%,{pct(5.2 + i*0.2)} {{ transform:scaleX(0) }} {pct(5.6 + i*0.2)},{pct(7.4)} {{ transform:scaleX(1) }} 100% {{ transform:scaleX(0) }} }}")
        css.append(f".b2s{i} {{ transform-box: fill-box; transform-origin: left center; animation: k2s{i} {T}s linear infinite; }}")
    css += [enter("k2z", 5.9, 7.4, "translate(0,16px)"), anim("b2z", "k2z")]
    # scene 3: smiley rolls in, wordmark slams
    css.append(f"@keyframes kroll {{ 0%,{pct(7.5)} {{ transform: translate(-560px,0) rotate(-540deg) }} "
               f"{pct(8.6)} {{ transform: translate(14px,0) rotate(12deg) }} {pct(8.9)},{pct(11)} {{ transform: translate(0,0) rotate(0deg) }} "
               f"100% {{ transform: translate(-560px,0) rotate(-540deg) }} }}")
    css.append(f".roll {{ transform-box: fill-box; transform-origin: center; animation: kroll {T}s linear infinite; }}")
    css += [enter("k3w", 8.7, 11.0, "scale(1.35)", "scale(1)", 0.25), anim("b3w", "k3w"),
            enter("k3r", 9.2, 11.0, "translate(0,16px)"), anim("b3r", "k3r")]
    css.append(".b3w { transform-box: fill-box; transform-origin: left center; }")
    # scene 4: three facts, staggered
    for i in range(3):
        css += [enter(f"k4{i}", 11.4 + i * 0.7, 14.6, "translate(-24px,0)"), anim(f"b4{i}", f"k4{i}")]
    # scene 5: tee + tagline
    css += [enter("k5p", 14.9, T + 1, "translate(0,20px)"), anim("b5p", "k5p"),
            enter("k5a", 15.4, T + 1, "translate(0,14px)"), anim("b5a", "k5a"),
            enter("k5b", 15.9, T + 1, "translate(0,14px)"), anim("b5b", "k5b"),
            enter("k5c", 16.4, T + 1, "translate(0,14px)"), anim("b5c", "k5c")]
    # progress scrubber + chapter dots
    css.append(f"@keyframes kbar {{ from {{ width:0 }} to {{ width:{W - 120}px }} }} .bar {{ animation: kbar {T}s linear infinite; }}")
    for i, (_, a, b) in enumerate(scenes):
        css.append(f"@keyframes kd{i} {{ 0%,{pct(a)} {{ opacity:.25 }} {pct(a + .01)},{pct(b - .01)} {{ opacity:1 }} {pct(b)},100% {{ opacity:.25 }} }} .d{i} {{ animation: kd{i} {T}s linear infinite; }}")
    if at is not None:
        css.append(f"* {{ animation-delay: -{at}s !important; animation-play-state: paused !important; }}")

    dots = "".join(
        f'<rect class="d{i}" x="{W - 60 - (len(scenes) - i) * 34}" y="{H - 48}" width="26" height="4" rx="2" fill="{WHITE}" opacity=".25"/>'
        for i in range(len(scenes)))

    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <clipPath id="frame"><rect width="{W}" height="{H}" rx="20"/></clipPath>
    <clipPath id="photo"><rect x="90" y="95" width="400" height="400" rx="16"/></clipPath>
  </defs>
  <style>
    text {{ white-space: pre; }}
    .s1,.s2,.s3,.s4,.s5 {{ opacity: 0; }}
    {chr(10).join("    " + c for c in css)}
  </style>
  <g clip-path="url(#frame)">
  <rect width="{W}" height="{H}" fill="{INK}"/>

  <!-- 01 · cold open -->
  <g class="s1">
    <rect width="{W}" height="{H}" fill="{INK}"/>
    <text class="b1a" x="600" y="230" text-anchor="middle" font-family="{MONO}" font-size="16" letter-spacing="6" fill="{YELLOW}">CHAPTER 01</text>
    <text class="b1b" x="600" y="330" text-anchor="middle" font-family="{HEAVY}" font-weight="900" font-size="72" fill="{WHITE}">HAPPY MILE</text>
    <text class="b1c" x="600" y="390" text-anchor="middle" font-family="{SERIF}" font-style="italic" font-size="24" fill="#BDBDBD">san francisco, california</text>
  </g>

  <!-- 02 · the problem -->
  <g class="s2">
    <rect width="{W}" height="{H}" fill="{HEATHER}"/>
    <text x="100" y="170" font-family="{HEAVY}" font-weight="900" font-size="48" fill="{INK}">MOST RUN CLUBS COST MONEY.</text>
    {"".join(f"""<g class="b2t{i}">
      <rect x="{100 + i*290}" y="230" width="260" height="76" rx="38" fill="none" stroke="{INK}" stroke-width="3"/>
      <text x="{230 + i*290}" y="279" text-anchor="middle" font-family="{HEAVY}" font-weight="900" font-size="26" fill="{INK}">{label}</text>
      <rect class="b2s{i}" x="{112 + i*290}" y="266" width="236" height="5" fill="#E5484D"/>
    </g>""" for i, label in enumerate(["$ MEMBERSHIP", "$ EVENTS", "$ ENTRY"]))}
    <g class="b2z">
      <text x="100" y="420" font-family="{SERIF}" font-style="italic" font-size="40" fill="{INK}">so we started one anyone could join.</text>
      <text x="100" y="475" font-family="{MONO}" font-size="16" letter-spacing="3" fill="#6B6B6B">FREE · EVERY SUNDAY</text>
    </g>
  </g>

  <!-- 03 · the brand -->
  <g class="s3">
    <rect width="{W}" height="{H}" fill="{YELLOW}"/>
    <g transform="translate(250 315)"><g class="roll">{smiley(130)}</g></g>
    <g class="b3w"><text x="440" y="330" font-family="{HEAVY}" font-weight="900" font-size="100" letter-spacing="-2" fill="{INK}">HAPPY MILE</text></g>
    <g class="b3r">
      <text x="446" y="390" font-family="{HEAVY}" font-weight="900" font-size="34" letter-spacing="10" fill="{INK}">RUN CLUB</text>
      <rect x="446" y="420" width="128" height="40" rx="20" fill="none" stroke="{INK}" stroke-width="2.5"/>
      <text x="510" y="447" text-anchor="middle" font-family="{SERIF}" font-style="italic" font-size="22" fill="{INK}">let's run</text>
    </g>
  </g>

  <!-- 04 · what made it different -->
  <g class="s4">
    <rect width="{W}" height="{H}" fill="{INK}"/>
    <text x="100" y="120" font-family="{MONO}" font-size="15" letter-spacing="5" fill="{YELLOW}">WHY IT WORKED</text>
    {"".join(f"""<g class="b4{i}">
      <text x="100" y="{230 + i*120}" font-family="{HEAVY}" font-weight="900" font-size="72" fill="{YELLOW}">{big}</text>
      <text x="420" y="{208 + i*120}" font-family="{HEAVY}" font-weight="900" font-size="26" fill="{WHITE}">{head}</text>
      <text x="420" y="{242 + i*120}" font-family="{SERIF}" font-style="italic" font-size="22" fill="#A8A8A8">{sub}</text>
      <rect x="100" y="{262 + i*120}" width="1000" height="1" fill="#2A2A2A"/>
    </g>""" for i, (big, head, sub) in enumerate([
        ("$0", "ACCESSIBLE FOR ALL", "free to join every sunday run"),
        ("18–22", "YOUTHFUL SPIRIT", "the age of our run leaders"),
        (":)", "RELAXED ATMOSPHERE", "running as a celebration, not a workout"),
    ]))}
  </g>

  <!-- 05 · enjoy every step -->
  <g class="s5">
    <rect width="{W}" height="{H}" fill="{HEATHER}"/>
    <g class="b5p">
      <image x="90" y="95" width="400" height="400" clip-path="url(#photo)" preserveAspectRatio="xMidYMid slice" href="data:image/jpeg;base64,{tee}" xlink:href="data:image/jpeg;base64,{tee}"/>
    </g>
    <g class="b5a"><text x="580" y="250" font-family="{SERIF}" font-style="italic" font-size="64" fill="{INK}">enjoy every step.</text></g>
    <g class="b5b"><text x="584" y="310" font-family="{HEAVY}" font-weight="900" font-size="22" letter-spacing="2" fill="{INK}">LAUNCHED BY WILLIAM ARMSTRONG</text></g>
    <g class="b5c">
      <rect x="584" y="350" width="236" height="48" rx="24" fill="{INK}"/>
      <text x="702" y="381" text-anchor="middle" font-family="{MONO}" font-size="16" fill="{YELLOW}">happymilerc.com →</text>
    </g>
  </g>

  <!-- scrubber -->
  <g style="mix-blend-mode: difference">
  <rect x="60" y="{H - 24}" width="{W - 120}" height="3" rx="1.5" fill="{WHITE}" opacity=".18"/>
  <rect class="bar" x="60" y="{H - 24}" width="0" height="3" rx="1.5" fill="{YELLOW}"/>
  <text x="60" y="{H - 42}" font-family="{MONO}" font-size="12" letter-spacing="3" fill="{WHITE}" opacity=".55">CH.01 · HAPPY MILE</text>
  {dots}
  </g>
  </g>
</svg>
'''


if __name__ == "__main__":
    if "--at" in sys.argv:
        t = float(sys.argv[sys.argv.index("--at") + 1])
        p = Path(f"/tmp/preview-{t:g}.svg")
        p.write_text(chapter_one(at=t))
        print("preview", p)
    else:
        (OUT / "ch01-happy-mile.svg").write_text(chapter_one())
        print("built", sorted(x.name for x in OUT.glob("*.svg")))
