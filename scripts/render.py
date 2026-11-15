"""Draw the profile README: SVG cards in assets/svg/ and README.md.

Profile design adapted from Sagargupta16 (https://github.com/Sagargupta16),
MIT licensed. scripts/kit.py and scripts/vendor/ come from that project and
keep its licence notices; the palette, content and this renderer are my own.

    python scripts/render.py            refresh GitHub and LeetCode, then draw
    python scripts/render.py --offline  draw from the cached data only

Stdlib only. A failed source keeps the last good values, so a flaky API never
blanks a card.
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kit  # noqa: E402
from vendor import github_stats_card, leetcode_card  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "svg"
DATA_FILE = OUT / "data.json"
ICONS = json.loads((OUT / "icons.json").read_text(encoding="utf-8"))

PROFILE = json.loads((ROOT / "profile.json").read_text(encoding="utf-8"))
W = 840

ORCHID = kit.BLUE_LIGHT
CREAM = kit.SKY
ORANGE = kit.AMBER
SLATE = kit.BLUE

# Hand-drawn 24 x 24 marks for the services Simple Icons does not carry.
EXTRA_ICONS = {
    "mail": "M3 6.5A2.5 2.5 0 0 1 5.5 4h13A2.5 2.5 0 0 1 21 6.5v11a2.5 2.5 0 0 1-2.5 2.5h-13A2.5 2.5 0 0 1 3 17.5Zm2.2.2L12 12.2l6.8-5.5v-.2H5.2Z",
    "globe": "M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20Zm0 2c.9 1 1.7 2.7 2.1 5H9.9C10.3 6.7 11.1 5 12 4Zm-3.6.7A11 11 0 0 0 7.8 9H4.3a8 8 0 0 1 4.1-4.3ZM4.1 11h3.6a20 20 0 0 0 0 2H4.1a8 8 0 0 1 0-2Zm.2 4h3.5c.2 1.7.6 3.2 1.2 4.3A8 8 0 0 1 4.3 15Zm5.6 0h4.2c-.4 2.3-1.2 4-2.1 5-.9-1-1.7-2.7-2.1-5Zm0-2a18 18 0 0 1 0-2h4.2a18 18 0 0 1 0 2Zm5.9 2h3.9a8 8 0 0 1-4.7 4.3c.6-1.1 1-2.6 1.2-4.3Zm.3-2a20 20 0 0 0 0-2h3.6a8 8 0 0 1 0 2Zm-.3-4c-.2-1.7-.6-3.2-1.2-4.3A8 8 0 0 1 19.7 9Z",
    "x": "M17.7 3h3.1l-6.8 7.7L22 21h-6.3l-4.9-6.4L5.2 21H2.1l7.3-8.3L2 3h6.4l4.4 5.9ZM16.6 19.1h1.7L7.4 4.8H5.6Z",
    "instagram": "M7.5 2h9A5.5 5.5 0 0 1 22 7.5v9a5.5 5.5 0 0 1-5.5 5.5h-9A5.5 5.5 0 0 1 2 16.5v-9A5.5 5.5 0 0 1 7.5 2Zm0 2A3.5 3.5 0 0 0 4 7.5v9A3.5 3.5 0 0 0 7.5 20h9a3.5 3.5 0 0 0 3.5-3.5v-9A3.5 3.5 0 0 0 16.5 4ZM12 7a5 5 0 1 1 0 10 5 5 0 0 1 0-10Zm0 2a3 3 0 1 0 0 6 3 3 0 0 0 0-6Zm5.3-3.3a1.2 1.2 0 1 1 0 2.4 1.2 1.2 0 0 1 0-2.4Z",
}


def icon_path(slug: str | None) -> str | None:
    if not slug:
        return None
    return EXTRA_ICONS.get(slug) or ICONS.get(slug)


def icon(slug: str, x: float, y: float, size: float, fill: str) -> str:
    path = icon_path(slug)
    if not path:
        return ""
    return f'<path transform="translate({x:g} {y:g}) scale({size / 24:.4f})" d="{path}" fill="{fill}"/>'


def write(name: str, svg: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(svg if svg.endswith("\n") else svg + "\n", encoding="utf-8")


# ---------------------------------------------------------------- the bot
BOT = (
    '<path d="M50 26V15" stroke="#a678b9" stroke-width="4.5" stroke-linecap="round"/>'
    '<circle cx="50" cy="10" r="9" fill="#f4a62a" opacity="0.25"><animate attributeName="r" values="9;13;9" dur="3s" repeatCount="indefinite"/>'
    '<animate attributeName="opacity" values="0.3;0.05;0.3" dur="3s" repeatCount="indefinite"/></circle>'
    '<circle cx="50" cy="10" r="6" fill="#f4a62a"/>'
    '<rect x="2" y="45" width="11" height="21" rx="5.5" fill="#6a5acd"/>'
    '<rect x="87" y="45" width="11" height="21" rx="5.5" fill="#6a5acd"/>'
    '<rect x="9" y="24" width="82" height="64" rx="26" fill="#a678b9"/>'
    '<path d="M20 40C22 31 30 28 40 28" stroke="#fff" stroke-opacity="0.35" stroke-width="3" stroke-linecap="round" fill="none"/>'
    '<rect x="18" y="33" width="64" height="46" rx="19" fill="#101014" stroke="#2d2b55" stroke-width="2"/>'
    '<g><rect x="33" y="46" width="11" height="18" rx="5.5" fill="#f0d9b5"/>'
    '<rect x="56" y="46" width="11" height="18" rx="5.5" fill="#f0d9b5"/>'
    '<circle cx="36.5" cy="50.5" r="1.8" fill="#fff"/><circle cx="59.5" cy="50.5" r="1.8" fill="#fff"/>'
    '<animateTransform attributeName="transform" type="scale" values="1 1;1 1;1 0.1;1 1;1 1" keyTimes="0;0.9;0.93;0.96;1" dur="5s" repeatCount="indefinite" additive="sum"/></g>'
    '<path d="M43 70Q50 75 57 70" stroke="#f0d9b5" stroke-width="2.8" stroke-linecap="round" fill="none"/>'
    '<circle cx="27" cy="68" r="3.2" fill="#f4a62a" opacity="0.55"/><circle cx="73" cy="68" r="3.2" fill="#f4a62a" opacity="0.55"/>'
)


def bot(x: float, y: float, size: float) -> str:
    return f'<g transform="translate({x:g} {y:g}) scale({size / 100:.4f})">{BOT}</g>'


# ---------------------------------------------------------------- hero
def hero() -> str:
    p = PROFILE
    h = 392
    label = (
        f"{p['name']}, {p['role']}, {p['employer_line']}, {p['location']}. "
        f"{p['availability']} {p['intro']}"
    )
    body = [kit.card_open(W, h, label, defs=kit.dot_pattern("dots"))]
    # diagram panel
    px, py, pw, ph = 500, 32, 308, 214
    body.append(
        f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="12" fill="{kit.CARD}" stroke="{kit.HAIR}"/>'
        f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="12" fill="url(#dots)"/>'
    )
    body.append(kit.eyebrow(px + 16, py + 26, "What I build"))
    cx, cy = px + pw / 2, py + 118
    nodes = [
        ("NETWORK TOOLS", px + 18, py + 52, "l"),
        ("WEBSITES", px + pw - 18 - 110, py + 52, "r"),
        ("SECURITY", px + 18, py + 150, "l"),
        ("BACKEND", px + pw - 18 - 110, py + 150, "r"),
    ]
    for i, (name, nx, ny, side) in enumerate(nodes):
        ex = nx + 110 if side == "l" else nx
        body.append(
            f'<path d="M{ex:g} {ny + 14:g}L{cx:g} {cy:g}" stroke="{kit.HAIR_STRONG}" stroke-width="1.2"/>'
            f'<circle r="2.6" fill="{CREAM}"><animateMotion dur="4s" begin="{i}s" repeatCount="indefinite" path="M{ex:g} {ny + 14:g}L{cx:g} {cy:g}"/>'
            f'<animate attributeName="opacity" values="0;1;1;0" dur="4s" begin="{i}s" repeatCount="indefinite"/></circle>'
        )
    for name, nx, ny, _ in nodes:
        body.append(
            f'<rect x="{nx:g}" y="{ny:g}" width="110" height="28" rx="8" fill="{kit.BG}" stroke="{kit.HAIR_STRONG}"/>'
            + kit.text(nx + 55, ny + 18, name, 10, kit.META, "m", "middle", ' letter-spacing="1"')
        )
    body.append(
        f'<circle cx="{cx:g}" cy="{cy:g}" r="36" fill="{kit.BG}" stroke="{kit.HAIR_STRONG}"/>'
        + bot(cx - 28, cy - 30, 56)
    )
    # left column
    body.append(kit.eyebrow(32, 46, "Hi, I am"))
    body.append(kit.eyebrow(466, 46, p["location"], kit.META, "end"))
    body.append(
        f'<path d="M110 42H{450}" stroke="{kit.HAIR_STRONG}" stroke-width="1"/>'
    )
    body.append(kit.text(30, 108, p["name"], 64, kit.INK, "t"))
    body.append(kit.text(32, 140, p["role"], 17, kit.INK, "s"))
    body.append(
        f'<rect x="32" y="152" width="3" height="18" rx="1.5" fill="{SLATE}"/>'
        + kit.text(44, 166, p["tagline"], 14.5, kit.INK, "s")
    )
    pill = f"{p['availability']}"
    pw_ = kit.text_width(pill, 12.5) + 44
    body.append(
        f'<rect x="32" y="180" width="{pw_:.0f}" height="26" rx="13" fill="{kit.CARD}" stroke="{kit.HAIR_STRONG}"/>'
        + kit.live_dot(48, 193, kit.GREEN, 4)
        + kit.text(60, 197, pill, 12.5, kit.INK, "b")
    )
    y = 226
    for line in kit.wrap_text(p["intro"], 440, 13.5):
        body.append(kit.text(32, y, line, 13.5, kit.BODY, "b"))
        y += 20
    # proof tiles
    tiles = p["proof"]
    tw = (W - 64 - 12 * (len(tiles) - 1)) / len(tiles)
    for i, t in enumerate(tiles):
        body.append(
            kit.tile(32 + i * (tw + 12), 312, tw, 64, t["value"], t["label"], size=21, color=CREAM if i == 0 else kit.INK)
        )
    body.append(kit.SVG_CLOSE)
    return "".join(body)


# ---------------------------------------------------------------- connect buttons
def button(label: str, slug: str, primary: bool = False) -> str:
    w, h = 128, 40
    stroke = ORANGE if primary else kit.HAIR_STRONG
    color = ORANGE if primary else kit.INK
    tw = kit.text_width(label.upper(), 11, True, 1.2)
    total = 16 + 8 + tw
    x0 = (w - total) / 2
    return (
        kit.svg_open(w, h, label)
        + kit.style()
        + f'<rect x="0.75" y="0.75" width="{w - 1.5}" height="{h - 1.5}" rx="9.25" fill="{kit.CARD}" stroke="{stroke}"/>'
        + icon(slug, x0, 12, 16, color)
        + kit.text(x0 + 24, 24.5, label.upper(), 11, color, "m")
        + kit.SVG_CLOSE
    )


# ---------------------------------------------------------------- section headers
def header(number: str, kicker: str, title: str, dark: bool) -> str:
    ink = "#f4f4f8" if dark else "#1f2328"
    meta = "rgba(255,255,255,0.62)" if dark else "rgba(31,35,40,0.7)"
    line = "rgba(255,255,255,0.12)" if dark else "rgba(31,35,40,0.15)"
    label_color = ORCHID if dark else "#6a5acd"
    return (
        kit.svg_open(W, 76, title)
        + kit.style()
        + f'<text class="k" x="0" y="27" font-size="11" fill="{meta}"><tspan fill="{label_color}">{number}</tspan> / {kit.escape(kicker.upper())}</text>'
        + f'<text class="t" x="0" y="57" font-size="24" fill="{ink}">{kit.escape(title)}</text>'
        + f'<path d="M0 69.5H{W}" stroke="{line}" stroke-width="1"/>'
        + f'<path d="M0 69.5H40" stroke="{SLATE}" stroke-width="2"/>'
        + f'<path d="M40 69.5H{W}" fill="none" stroke="{CREAM}" stroke-width="2" stroke-linecap="round" pathLength="100" stroke-dasharray="12 112" stroke-dashoffset="12">'
        + '<animate attributeName="stroke-dashoffset" values="12;-100;-100" keyTimes="0;0.333;1" dur="6s" repeatCount="indefinite"/></path>'
        + kit.SVG_CLOSE
    )


# ---------------------------------------------------------------- experience
def experience() -> str:
    items = PROFILE["experience"]
    h = 214
    label = "Career: " + "; ".join(
        f"{e['when']}, {e['title']}, {e['org']}, {e['where']}" for e in items
    )
    body = [kit.card_open(W, h, label)]
    body.append(kit.eyebrow(32, 38, PROFILE["experience_kicker"]))
    n = len(items)
    left, right = 120, W - 120
    ty = 70
    xs = [left + (right - left) * (i / max(n - 1, 1)) for i in range(n)] if n > 1 else [W / 2]
    if n > 1:
        body.append(f'<path d="M{xs[0]:g} {ty}H{xs[-1]:g}" stroke="{SLATE}" stroke-width="2"/>')
    for x, e in zip(xs, items):
        current = e.get("current")
        color = kit.GREEN if current else ORCHID
        body.append(
            kit.text(x, ty - 14, e["when"].upper(), kit.MICRO, color, "m", "middle")
            + f'<circle cx="{x:g}" cy="{ty}" r="6" fill="{kit.BG}" stroke="{color}" stroke-width="2"/>'
            + f'<circle cx="{x:g}" cy="{ty}" r="2.4" fill="{color}"/>'
            + kit.text(x, ty + 30, e["title"], 16, kit.INK, "s", "middle")
            + kit.text(x, ty + 50, e["org"], 13.5, kit.BODY, "b", "middle")
            + kit.text(x, ty + 70, e["where"].upper(), kit.MICRO, kit.META, "m", "middle")
        )
        tags = e.get("tags", [])
        widths = [kit.chip_width(t) for t in tags]
        cx0 = x - (sum(widths) + 8 * (len(tags) - 1)) / 2
        for t, wd in zip(tags, widths):
            svg, _ = kit.chip(cx0, ty + 92, t, ORCHID)
            body.append(svg)
            cx0 += wd + 8
    body.append(kit.SVG_CLOSE)
    return "".join(body)


# ---------------------------------------------------------------- stack
def stack() -> str:
    lanes = PROFILE["stack"]
    pad, label_w = 32, 150
    chip_h, gap = 30, 8
    area_w = W - pad * 2 - label_w - 24
    rows = []
    for lane in lanes:
        x, y, lines = 0, 0, 1
        placed = []
        for name, slug in lane["items"]:
            wd = kit.text_width(name, 12.5) + (38 if icon_path(slug) else 24)
            if x and x + wd > area_w:
                x, y, lines = 0, y + chip_h + gap, lines + 1
            placed.append((name, slug, x, y, wd))
            x += wd + gap
        rows.append((lane, placed, lines))
    heights = [r[2] * chip_h + (r[2] - 1) * gap + 24 for r in rows]
    h = 56 + sum(heights) + 10 * (len(rows) - 1) + 24
    total = sum(len(lane["items"]) for lane in lanes)
    label = f"Tech stack, {total} tools in {len(lanes)} lanes. " + " ".join(
        f"{lane['name']}: " + ", ".join(n for n, _ in lane["items"]) + "." for lane in lanes
    )
    body = [kit.card_open(W, h, label)]
    body.append(kit.eyebrow(pad, 38, f"{total} tools in {len(lanes)} lanes"))
    y = 56
    for idx, ((lane, placed, lines), lh) in enumerate(zip(rows, heights)):
        body.append(
            f'<rect x="{pad}" y="{y}" width="{W - pad * 2}" height="{lh}" rx="12" fill="{kit.HAIR_FILL}" stroke="{kit.HAIR_STRONG}"/>'
            + f'<circle cx="{pad + 22}" cy="{y + lh / 2:g}" r="10" fill="{kit.BG}" stroke="{ORCHID}"/>'
            + kit.text(pad + 22, y + lh / 2 + 3.6, str(idx + 1), 10.5, ORCHID, "m", "middle")
        )
        for li, part in enumerate(kit.wrap_text(lane["name"].upper(), label_w - 52, kit.MICRO, True, kit.TRACK)):
            body.append(kit.text(pad + 42, y + lh / 2 - 4 + li * 14, part, kit.MICRO, kit.META, "m"))
        for name, slug, cx, cy, wd in placed:
            x0 = pad + label_w + 24 + cx
            y0 = y + 12 + cy
            body.append(
                f'<rect x="{x0:g}" y="{y0:g}" width="{wd:.0f}" height="{chip_h}" rx="9" fill="{kit.CARD}" stroke="{kit.HAIR_STRONG}"/>'
            )
            tx = x0 + 10
            if icon_path(slug):
                body.append(icon(slug, x0 + 10, y0 + 7, 16, ORCHID))
                tx = x0 + 32
            body.append(kit.text(tx, y0 + 19.5, name, 12.5, kit.INK, "s"))
        y += lh + 10
    body.append(kit.SVG_CLOSE)
    return "".join(body)


# ---------------------------------------------------------------- footer
def footer() -> str:
    h = 112
    return (
        kit.card_open(W, h, PROFILE["footer"])
        + kit.eyebrow(32, 38, "Thanks for visiting")
        + kit.text(32, 72, PROFILE["footer"], 15, kit.INK, "s")
        + kit.text(32, 94, PROFILE["footer_note"], 12.5, kit.META, "b")
        + bot(W - 88, 28, 56)
        + kit.SVG_CLOSE
    )


# ---------------------------------------------------------------- data
def load_data() -> dict:
    data = {}
    if DATA_FILE.exists():
        data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    return data


def refresh(data: dict) -> None:
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    try:
        if token:
            data["github"] = github_stats_card.fetch_stats(PROFILE["github_user"], token, 6, set())
    except Exception as exc:  # keep the last good values
        print(f"github fetch failed, keeping cache: {exc}", file=sys.stderr)
    try:
        data["leetcode"] = leetcode_card.fetch_profile(PROFILE["leetcode_user"], heatmap=True)
    except Exception as exc:
        print(f"leetcode fetch failed, keeping cache: {exc}", file=sys.stderr)
    data["updated"] = datetime.datetime.now(datetime.UTC).isoformat(timespec="seconds")


def empty_github() -> dict:
    return {
        "contributions": 0, "commits": 0, "prs": 0, "stars": 0, "repo_stars": {},
        "followers": 0, "streak": 0, "longest": 0, "active_days": 0,
        "calendar": [[0] * 7 for _ in range(53)], "languages": [],
    }


def empty_leetcode() -> dict:
    return {
        "badge": "", "rating": 0, "top": 0.0, "contests": 0, "solved": 0,
        "by_difficulty": {"Easy": [0, 1], "Medium": [0, 1], "Hard": [0, 1]},
        "history": [], "calendar": {},
    }


def leetcode_for_card(lc: dict) -> dict:
    """The cache stores the calendar as text keys; the card wants dates."""
    lc = dict(lc)
    cal = lc.get("calendar") or {}
    lc["calendar"] = {
        datetime.date.fromisoformat(k) if isinstance(k, str) else k: v for k, v in cal.items()
    }
    return lc


def jsonable(data: dict) -> dict:
    out = json.loads(json.dumps(data, default=lambda o: o.isoformat() if hasattr(o, "isoformat") else str(o)))
    return out


# ---------------------------------------------------------------- README
def picture_header(key: str) -> str:
    return (
        f'<picture><source media="(prefers-color-scheme: light)" srcset="assets/svg/header-{key}-light.svg" />'
        f'<source media="(prefers-color-scheme: dark)" srcset="assets/svg/header-{key}-dark.svg" />'
        f'<img src="assets/svg/header-{key}-dark.svg" width="100%" alt="{kit.escape(PROFILE["headers"][key][2])}" /></picture>'
    )


def alt_of(name: str) -> str:
    text = (OUT / name).read_text(encoding="utf-8")
    start = text.index('aria-label="') + len('aria-label="')
    return text[start : text.index('"', start)]


def readme() -> str:
    p = PROFILE
    parts = [
        "<!-- Generated by scripts/render.py. Edit profile.json or the script, not this file. -->\n",
        f'<a href="{p["portfolio_url"]}"><picture><img src="assets/svg/hero.svg" width="100%" alt="{alt_of("hero.svg")}" /></picture></a>\n',
        '<p align="center">\n'
        + "\n".join(
            f'<a href="{b["url"]}"><picture><img src="assets/svg/connect-{b["key"]}.svg" width="128" alt="{b["label"]}" /></picture></a>'
            for b in p["connect"]
        )
        + "\n</p>\n",
    ]
    for key in ("experience", "stack", "stats"):
        parts.append(picture_header(key) + "\n")
        if key == "experience":
            parts.append(f'<picture><img src="assets/svg/experience.svg" width="100%" alt="{alt_of("experience.svg")}" /></picture>\n')
        if key == "stack":
            parts.append(f'<picture><img src="assets/svg/stack.svg" width="100%" alt="{alt_of("stack.svg")}" /></picture>\n')
        if key == "stats":
            parts.append(
                f'<a href="https://github.com/{p["github_user"]}"><picture><img src="assets/svg/github.svg" width="100%" alt="{alt_of("github.svg")}" /></picture></a>\n'
            )
            parts.append(
                f'<a href="https://leetcode.com/u/{p["leetcode_user"]}/"><picture><img src="assets/svg/leetcode.svg" width="100%" alt="{alt_of("leetcode.svg")}" /></picture></a>\n'
            )
    parts.append(
        f'<a href="{p["portfolio_url"]}"><picture><img src="assets/svg/footer.svg" width="100%" alt="{alt_of("footer.svg")}" /></picture></a>\n'
    )
    parts.append(
        '<p align="center"><sub>Profile design adapted from '
        '<a href="https://github.com/Sagargupta16">Sagargupta16</a> (MIT).</sub></p>\n'
    )
    return "\n".join(parts)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", action="store_true")
    args = ap.parse_args()
    data = load_data()
    if not args.offline:
        refresh(data)
    gh = data.get("github") or empty_github()
    lc = data.get("leetcode") or empty_leetcode()
    DATA_FILE.write_text(json.dumps(jsonable(data), indent=1) + "\n", encoding="utf-8")

    write("hero.svg", hero())
    for b in PROFILE["connect"]:
        write(f"connect-{b['key']}.svg", button(b["label"], b["icon"], b.get("primary", False)))
    for key, (num, kicker, title) in PROFILE["headers"].items():
        write(f"header-{key}-dark.svg", header(num, kicker, title, True))
        write(f"header-{key}-light.svg", header(num, kicker, title, False))
    write("experience.svg", experience())
    write("stack.svg", stack())
    write("footer.svg", footer())
    write(
        "github.svg",
        github_stats_card.render_card(gh, PROFILE["github_user"], f"GITHUB | @{PROFILE['github_user'].upper()}", ORCHID),
    )
    write("leetcode.svg", leetcode_card.render_card(leetcode_for_card(lc), PROFILE["leetcode_user"]))
    (ROOT / "README.md").write_text(readme(), encoding="utf-8")
    print("rendered")


if __name__ == "__main__":
    main()
