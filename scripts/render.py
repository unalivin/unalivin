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
import hashlib
import re
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import areas  # noqa: E402
import kit  # noqa: E402
from vendor import github_stats_card, leetcode_card  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "svg"
DATA_FILE = OUT / "data.json"
ICONS = json.loads((OUT / "icons.json").read_text(encoding="utf-8"))

PROFILE = json.loads((ROOT / "profile.json").read_text(encoding="utf-8"))
W = 840
AREAS = PROFILE["areas"]

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
    '<g>'
    '<rect x="33" y="46" width="11" height="18" rx="5.5" fill="#f0d9b5">'
    '<animate attributeName="height" values="18;18;2;18;18" keyTimes="0;0.9;0.93;0.96;1" dur="5s" repeatCount="indefinite"/>'
    '<animate attributeName="y" values="46;46;54;46;46" keyTimes="0;0.9;0.93;0.96;1" dur="5s" repeatCount="indefinite"/></rect>'
    '<rect x="56" y="46" width="11" height="18" rx="5.5" fill="#f0d9b5">'
    '<animate attributeName="height" values="18;18;2;18;18" keyTimes="0;0.9;0.93;0.96;1" dur="5s" repeatCount="indefinite"/>'
    '<animate attributeName="y" values="46;46;54;46;46" keyTimes="0;0.9;0.93;0.96;1" dur="5s" repeatCount="indefinite"/></rect>'
    '<circle cx="36.5" cy="50.5" r="1.8" fill="#fff">'
    '<animate attributeName="opacity" values="1;1;0;1;1" keyTimes="0;0.9;0.93;0.96;1" dur="5s" repeatCount="indefinite"/></circle>'
    '<circle cx="59.5" cy="50.5" r="1.8" fill="#fff">'
    '<animate attributeName="opacity" values="1;1;0;1;1" keyTimes="0;0.9;0.93;0.96;1" dur="5s" repeatCount="indefinite"/></circle>'
    '</g>'
    '<path d="M43 70Q50 75 57 70" stroke="#f0d9b5" stroke-width="2.8" stroke-linecap="round" fill="none"/>'
    '<circle cx="27" cy="68" r="3.2" fill="#f4a62a" opacity="0.55"/><circle cx="73" cy="68" r="3.2" fill="#f4a62a" opacity="0.55"/>'
)


def bot(x: float, y: float, size: float) -> str:
    return f'<g transform="translate({x:g} {y:g}) scale({size / 100:.4f})">{BOT}</g>'


# ---------------------------------------------------------------- hero
def diagram(px: float, py: float, pw: float, ph: float) -> str:
    items = AREAS
    left, right = items[:4], items[4:]
    nw = 100 if pw < 330 else 108
    cx, cy = px + pw / 2, py + ph / 2 + 8
    panel = [
        f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="12" fill="{kit.CARD}" stroke="{kit.HAIR}"/>'
        f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="12" fill="url(#dots)"/>'
    ]
    panel.append(kit.eyebrow(px + 16, py + 26, "What I work on"))
    top, bottom = py + 44, py + ph - 14 - 26
    placed = []
    for col, group_items, side in ((0, left, "l"), (1, right, "r")):
        n = len(group_items)
        step = (bottom - top) / max(n - 1, 1) if n > 1 else 0
        for i, it in enumerate(group_items):
            ny = top + i * step if n > 1 else (top + bottom) / 2
            nx = px + 12 if side == "l" else px + pw - 12 - nw
            placed.append((it, nx, ny, side))
    for k, (it, nx, ny, side) in enumerate(placed):
        ex = nx + nw if side == "l" else nx
        path = f"M{ex:g} {ny + 13:g}L{cx:g} {cy:g}"
        panel.append(
            kit.group(
                0.5 + k * 0.25,
                f'<path d="{path}" stroke="{kit.HAIR_STRONG}" stroke-width="1.2"/>'
                f'<circle r="2.6" fill="{CREAM}"><animateMotion dur="4s" begin="{k * 0.6:g}s" repeatCount="indefinite" path="{path}"/>'
                f'<animate attributeName="opacity" values="0;1;1;0" dur="4s" begin="{k * 0.6:g}s" repeatCount="indefinite"/></circle>'
                f'<rect x="{nx:g}" y="{ny:g}" width="{nw}" height="26" rx="8" fill="{kit.BG}" stroke="{kit.HAIR_STRONG}"/>'
                + kit.text(nx + nw / 2, ny + 17, areas.SHORT.get(it["key"], it["title"].upper()), 9, kit.META, "m", "middle", ' letter-spacing="0.8"'),
                "0 0",
            )
        )
    panel.append(
        f'<circle cx="{cx:g}" cy="{cy:g}" r="32" fill="{kit.BG}" stroke="{kit.HAIR_STRONG}"/>' + bot(cx - 25, cy - 27, 50)
    )
    panel.append(
        kit.group(
            2.6,
            kit.live_dot(cx - 16, cy + 44, kit.GREEN, 3) + kit.text(cx - 8, cy + 47.5, "LIVE", 9, kit.INK, "m"),
            "0 0",
        )
    )
    return kit.group(0.3, "".join(panel), "12 0")


def hero(mobile: bool = False) -> str:
    p = PROFILE
    label = (
        f"{p['name']}, {p['role']}, {p['employer_line']}, {p['location']}. "
        f"{p['availability']} {p['intro']} Focus areas: "
        + ", ".join(a["title"] for a in AREAS)
        + "."
    )
    if not mobile:
        w, h = W, 404
        body = [kit.card_open(w, h, label, defs=kit.dot_pattern("dots"))]
        body.append(diagram(500, 32, 308, 262))
        text_w = 440
        left_x = 32
        y_intro = 226
    else:
        w = 400
        text_w = 336
        left_x = 32
        y_intro = 252
    parts = []
    if not mobile:
        parts.append(kit.eyebrow(32, 46, "Hi, I am") + kit.eyebrow(466, 46, p["location"], kit.META, "end") + f'<path d="M110 42H450" stroke="{kit.HAIR_STRONG}" stroke-width="1"/>')
        parts.append(kit.text(30, 108, p["name"], 64, kit.INK, "t"))
        parts.append(kit.text(32, 140, p["role"], 17, kit.INK, "s"))
        tag_y, pill_y = 166, 180
    else:
        parts.append(kit.eyebrow(32, 44, "Hi, I am") + kit.eyebrow(368, 44, p["location"], kit.META, "end"))
        parts.append(kit.text(30, 98, p["name"], 52, kit.INK, "t"))
        parts.append(kit.text(32, 128, p["role"], 15.5, kit.INK, "s"))
        tag_y, pill_y = 154, 168
    pill = p["availability"]
    pw_ = kit.text_width(pill, 12.5) + 44
    extra = (
        f'<rect x="32" y="{pill_y - 28}" width="3" height="18" rx="1.5" fill="{SLATE}"/>'
        + kit.rotating(p["taglines"], 44, tag_y, "s", 14.5, kit.INK, slot=3.0)
        + f'<rect x="32" y="{pill_y}" width="{pw_:.0f}" height="26" rx="13" fill="{kit.CARD}" stroke="{kit.HAIR_STRONG}"/>'
        + kit.live_dot(48, pill_y + 13, kit.GREEN, 4)
        + kit.text(60, pill_y + 17, pill, 12.5, kit.INK, "b")
    )
    lines = []
    y = pill_y + 46
    for line in kit.wrap_text(p["intro"], text_w, 13.5):
        lines.append(kit.text(32, y, line, 13.5, kit.BODY, "b"))
        y += 20
    if mobile:
        panel_y = y + 14
        ph = 262
        h_total = panel_y + ph + 14
        tiles_y = h_total
        tw = (w - 64 - 12) / 2
        tiles_h = 64 * 2 + 12
        h = tiles_y + tiles_h + 28
        body = [kit.card_open(w, h, label, defs=kit.dot_pattern("dots"))]
        body.append(diagram(16, panel_y, w - 32, ph))
        for i, t in enumerate(p["proof"]):
            body.append(kit.tile(32 + (i % 2) * (tw + 12), tiles_y + (i // 2) * 76, tw, 64, t["value"], t["label"], at=0.6 + i * 0.08, size=20, color=CREAM if i == 0 else kit.INK))
    else:
        tiles = p["proof"]
        tw = (W - 64 - 12 * (len(tiles) - 1)) / len(tiles)
        for i, t in enumerate(tiles):
            body.append(kit.tile(32 + i * (tw + 12), 318, tw, 64, t["value"], t["label"], at=0.6 + i * 0.08, size=21, color=CREAM if i == 0 else kit.INK))
    body.append(kit.group(0.0, "".join(parts)))
    body.append(kit.group(0.3, extra))
    body.append(kit.group(0.5, "".join(lines)))
    body.append(kit.SVG_CLOSE)
    return "".join(body)


# ---------------------------------------------------------------- connect buttons
def button(label: str, slug: str, primary: bool = False, index: int = 0) -> str:
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
        + f'<rect x="0.75" y="0.75" width="{w - 1.5}" height="{h - 1.5}" rx="9.25" fill="rgba(106,90,205,0.14)" stroke="{ORCHID}" stroke-width="1.5" opacity="0">'
        + kit.loop("opacity", "0;1;1;0;0", "0;0.0417;0.1917;0.2417;1", 6, 3 + index)
        + "</rect>"
        + icon(slug, x0, 12, 16, color)
        + kit.text(x0 + 24, 24.5, label.upper(), 11, color, "m")
        + kit.SVG_CLOSE
    )


# ---------------------------------------------------------------- section headers
def header(number: str, kicker: str, title: str, dark: bool, w: int = W) -> str:
    ink = "#f4f4f8" if dark else "#1f2328"
    meta = "rgba(255,255,255,0.62)" if dark else "rgba(31,35,40,0.7)"
    line = "rgba(255,255,255,0.12)" if dark else "rgba(31,35,40,0.15)"
    label_color = ORCHID if dark else "#6a5acd"
    return (
        kit.svg_open(w, 76, title)
        + kit.style()
        + f'<text class="k" x="0" y="27" font-size="11" fill="{meta}"><tspan fill="{label_color}">{number}</tspan> / {kit.escape(kicker.upper())}</text>'
        + f'<text class="t" x="0" y="57" font-size="24" fill="{ink}">{kit.escape(title)}</text>'
        + f'<path d="M0 69.5H{w}" stroke="{line}" stroke-width="1"/>'
        + f'<path d="M0 69.5H40" stroke="{SLATE}" stroke-width="2"/>'
        + f'<path d="M40 69.5H{w}" fill="none" stroke="{CREAM}" stroke-width="2" stroke-linecap="round" pathLength="100" stroke-dasharray="12 112" stroke-dashoffset="12">'
        + '<animate attributeName="stroke-dashoffset" values="12;-100;-100" keyTimes="0;0.333;1" dur="6s" repeatCount="indefinite"/></path>'
        + kit.SVG_CLOSE
    )


# ---------------------------------------------------------------- experience
def experience(mobile: bool = False) -> str:
    if mobile:
        return experience_mobile()
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
        pulse = kit.live_dot(x, ty, color, 3) if current else ""
        body.append(
            kit.group(
                0.2,
                kit.text(x, ty - 14, e["when"].upper(), kit.MICRO, color, "m", "middle")
                + f'<circle cx="{x:g}" cy="{ty}" r="6" fill="{kit.BG}" stroke="{color}" stroke-width="2"/>'
                + f'<circle cx="{x:g}" cy="{ty}" r="2.4" fill="{color}"/>'
                + pulse
                + kit.text(x, ty + 30, e["title"], 16, kit.INK, "s", "middle")
                + kit.text(x, ty + 50, e["org"], 13.5, kit.BODY, "b", "middle")
                + kit.text(x, ty + 70, e["where"].upper(), kit.MICRO, kit.META, "m", "middle"),
            )
        )
        tags = e.get("tags", [])
        widths = [kit.chip_width(t) for t in tags]
        cx0 = x - (sum(widths) + 8 * (len(tags) - 1)) / 2
        for t, wd in zip(tags, widths):
            svg, _ = kit.chip(cx0, ty + 92, t, ORCHID)
            body.append(kit.group(0.5, svg))
            cx0 += wd + 8
    body.append(kit.SVG_CLOSE)
    return "".join(body)


def experience_mobile() -> str:
    items = PROFILE["experience"]
    w = 400
    row = 150
    h = 56 + row * len(items) + 12
    label = "Career: " + "; ".join(f"{e['when']}, {e['title']}, {e['org']}, {e['where']}" for e in items)
    body = [kit.card_open(w, h, label), kit.eyebrow(24, 36, PROFILE["experience_kicker"])]
    for i, e in enumerate(items):
        y = 64 + i * row
        color = kit.GREEN if e.get("current") else ORCHID
        if len(items) > 1 and i < len(items) - 1:
            body.append(f'<path d="M30 {y + 8}V{y + row}" stroke="{SLATE}" stroke-width="2"/>')
        tags = e.get("tags", [])
        tag_svg, cx0 = "", 52
        for t in tags:
            svg, wd = kit.chip(cx0, y + 84, t, ORCHID)
            if cx0 + wd > w - 16:
                break
            tag_svg += svg
            cx0 += wd + 8
        body.append(
            kit.group(
                0.2,
                f'<circle cx="30" cy="{y + 8}" r="6" fill="{kit.BG}" stroke="{color}" stroke-width="2"/><circle cx="30" cy="{y + 8}" r="2.4" fill="{color}"/>'
                + (kit.live_dot(30, y + 8, color, 3) if e.get("current") else "")
                + kit.text(52, y + 12, e["when"].upper(), kit.MICRO, color, "m")
                + kit.text(52, y + 38, e["title"], 16, kit.INK, "s")
                + kit.text(52, y + 58, e["org"], 13.5, kit.BODY, "b")
                + kit.text(52, y + 76, e["where"].upper(), kit.MICRO, kit.META, "m")
                + tag_svg,
            )
        )
    body.append(kit.SVG_CLOSE)
    return "".join(body)


# ---------------------------------------------------------------- stack
def stack(mobile: bool = False) -> str:
    lanes = PROFILE["stack"]
    w = 400 if mobile else W
    pad = 24 if mobile else 32
    label_w = 0 if mobile else 150
    chip_h, gap = 30, 8
    area_w = w - pad * 2 - (24 if mobile else label_w + 24)
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
    head = 22 if mobile else 0
    heights = [r[2] * chip_h + (r[2] - 1) * gap + 24 + head for r in rows]
    h = 56 + sum(heights) + 10 * (len(rows) - 1) + 24
    total = sum(len(lane["items"]) for lane in lanes)
    label = f"Tools, {total} in {len(lanes)} groups. " + " ".join(
        f"{lane['name']}: " + ", ".join(n for n, _ in lane["items"]) + "." for lane in lanes
    )
    body = [kit.card_open(w, h, label)]
    body.append(kit.eyebrow(pad, 38, f"{total} tools in {len(lanes)} groups"))
    y = 56
    count = len(rows)
    for idx, ((lane, placed, lines), lh) in enumerate(zip(rows, heights)):
        parts = [
            f'<rect x="{pad}" y="{y}" width="{w - pad * 2}" height="{lh}" rx="12" fill="{kit.HAIR_FILL}" stroke="{kit.HAIR_STRONG}"/>',
        ]
        if mobile:
            parts.append(kit.text(pad + 14, y + 20, lane["name"].upper(), kit.MICRO, kit.META, "m"))
            ox, oy = pad + 12, y + 12 + head
        else:
            parts.append(f'<circle cx="{pad + 22}" cy="{y + lh / 2:g}" r="10" fill="{kit.BG}" stroke="{ORCHID}"/>')
            parts.append(kit.text(pad + 22, y + lh / 2 + 3.6, str(idx + 1), 10.5, ORCHID, "m", "middle"))
            parts.append(kit.text(pad + 42, y + lh / 2 + 4, lane["name"].upper(), kit.MICRO, kit.META, "m"))
            ox, oy = pad + label_w + 24, y + 12
        for name, slug, cx, cy, wd in placed:
            x0, y0 = ox + cx, oy + cy
            parts.append(f'<rect x="{x0:g}" y="{y0:g}" width="{wd:.0f}" height="{chip_h}" rx="9" fill="{kit.CARD}" stroke="{kit.HAIR_STRONG}"/>')
            tx = x0 + 10
            if icon_path(slug):
                parts.append(icon(slug, x0 + 10, y0 + 7, 16, ORCHID))
                tx = x0 + 32
            parts.append(kit.text(tx, y0 + 19.5, name, 12.5, kit.INK, "s"))
        a0, a1 = idx / count, (idx + 1) / count
        times = sorted({0.0, round(a0, 4), round(a0 + 0.02, 4), round(a1 - 0.02, 4), round(a1, 4), 1.0})
        vals = ["1" if a0 + 0.02 - 1e-6 <= t <= a1 - 0.02 + 1e-6 else "0" for t in times]
        parts.append(
            f'<rect x="{pad}" y="{y}" width="{w - pad * 2}" height="{lh}" rx="12" fill="rgba(106,90,205,0.12)" stroke="{ORCHID}" stroke-width="1.5" opacity="0">'
            + kit.loop("opacity", ";".join(vals), ";".join(f"{t:g}" for t in times), 12)
            + "</rect>"
        )
        body.append(kit.group(0.15 + idx * 0.1, "".join(parts)))
        y += lh + 10
    body.append(kit.SVG_CLOSE)
    return "".join(body)


def areas_cards() -> None:
    n = len(AREAS)
    for i, area in enumerate(AREAS):
        svg, _ = areas.card(area, i, 410)
        write(f"area-{area['key']}.svg", svg)
        if i == 0:
            wide, _ = areas.card(area, i, W, True)
            write(f"area-{area['key']}-wide.svg", wide)


# ---------------------------------------------------------------- footer
def footer(mobile: bool = False) -> str:
    h = 112
    w = 400 if mobile else W
    return (
        kit.card_open(w, h, PROFILE["footer"])
        + kit.group(
            0.1,
            kit.eyebrow(32, 38, "Thanks for visiting")
            + kit.text(32, 72, PROFILE["footer"], 14 if mobile else 15, kit.INK, "s")
            + kit.text(32, 94, PROFILE["footer_note"], 11.5 if mobile else 12.5, kit.META, "b"),
        )
        + kit.group(0.3, bot(w - 88, 28, 56), "0 0")
        + kit.SVG_CLOSE
    )


# ---------------------------------------------------------------- data
def load_data() -> dict:
    data = {}
    if DATA_FILE.exists():
        data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    return data


def sync_areas() -> None:
    import urllib.request

    try:
        with urllib.request.urlopen(PROFILE["site_data_url"], timeout=20) as r:
            fresh = json.loads(r.read().decode("utf-8"))
        ok = (
            isinstance(fresh, list)
            and fresh
            and all(isinstance(a, dict) and a.get("key") and a.get("title") and isinstance(a.get("list"), list) for a in fresh)
        )
        if ok:
            AREAS[:] = fresh
    except Exception as exc:
        print(f"site areas not fetched, using profile.json: {exc}", file=sys.stderr)


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
    t = kit.escape(PROFILE["headers"][key][2])
    return (
        f'<picture><source media="(prefers-color-scheme: light) and (min-width: 1012px)" srcset="assets/svg/header-{key}-light.svg" />'
        f'<source media="(prefers-color-scheme: dark) and (min-width: 1012px)" srcset="assets/svg/header-{key}-dark.svg" />'
        f'<source media="(prefers-color-scheme: light)" srcset="assets/svg/header-{key}-light-mobile.svg" />'
        f'<source media="(prefers-color-scheme: dark)" srcset="assets/svg/header-{key}-dark-mobile.svg" />'
        f'<img src="assets/svg/header-{key}-dark-mobile.svg" width="100%" alt="{t}" /></picture>'
    )


def responsive(name: str, mobile: str | None = None, width: str = "100%") -> str:
    mobile = mobile or name.replace(".svg", "-mobile.svg")
    return (
        f'<picture><source media="(min-width: 1012px)" srcset="assets/svg/{name}" />'
        f'<img src="assets/svg/{mobile}" width="{width}" alt="{alt_of(name)}" /></picture>'
    )


def alt_of(name: str) -> str:
    text = (OUT / name).read_text(encoding="utf-8")
    start = text.index('aria-label="') + len('aria-label="')
    return text[start : text.index('"', start)]


def readme() -> str:
    p = PROFILE
    first = AREAS[0]
    wide = f"area-{first['key']}-wide.svg"
    cards = []
    for i, area in enumerate(AREAS):
        if i == 0:
            continue
        name = f"area-{area['key']}.svg"
        cards.append(f'<picture><img src="assets/svg/{name}" width="400" alt="{alt_of(name)}" /></picture>')
    parts = [
        "<!-- Generated by scripts/render.py. Edit profile.json or the script, not this file. -->\n",
        f'<a href="{p["portfolio_url"]}">{responsive("hero.svg")}</a>\n',
        '<p align="center">\n'
        + "\n".join(
            f'<a href="{b["url"]}"><picture><img src="assets/svg/connect-{b["key"]}.svg" width="128" alt="{b["label"]}" /></picture></a>'
            for b in p["connect"]
        )
        + "\n</p>\n",
        picture_header("experience") + "\n",
        responsive("experience.svg") + "\n",
        picture_header("areas") + "\n",
        f'<picture><source media="(min-width: 1012px)" srcset="assets/svg/{wide}" /><img src="assets/svg/area-{first["key"]}.svg" width="100%" alt="{alt_of("area-" + first["key"] + ".svg")}" /></picture>\n',
        '<p align="center">\n' + "\n".join(cards) + "\n</p>\n",
        picture_header("stack") + "\n",
        responsive("stack.svg") + "\n",
        picture_header("stats") + "\n",
        f'<a href="https://github.com/{p["github_user"]}"><picture><img src="assets/svg/github.svg" width="100%" alt="{alt_of("github.svg")}" /></picture></a>\n',
        f'<a href="https://leetcode.com/u/{p["leetcode_user"]}/"><picture><img src="assets/svg/leetcode.svg" width="100%" alt="{alt_of("leetcode.svg")}" /></picture></a>\n',
        f'<a href="{p["portfolio_url"]}">{responsive("footer.svg")}</a>\n',
        '<p align="center"><sub>Profile design adapted from '
        '<a href="https://github.com/Sagargupta16">Sagargupta16</a> (MIT).</sub></p>\n',
    ]
    text = "\n".join(parts)

    def versioned(m: "re.Match[str]") -> str:
        f = OUT / m.group(1)
        tag = hashlib.sha1(f.read_bytes()).hexdigest()[:8] if f.exists() else "0"
        return f"assets/svg/{m.group(1)}?v={tag}"

    return re.sub(r"assets/svg/([\w.-]+\.svg)", versioned, text)


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

    if not args.offline:
        sync_areas()
    write("hero.svg", hero())
    write("hero-mobile.svg", hero(True))
    for i, b in enumerate(PROFILE["connect"]):
        write(f"connect-{b['key']}.svg", button(b["label"], b["icon"], b.get("primary", False), i))
    for key, (num, kicker, title) in PROFILE["headers"].items():
        for dark, tone in ((True, "dark"), (False, "light")):
            write(f"header-{key}-{tone}.svg", header(num, kicker, title, dark))
            write(f"header-{key}-{tone}-mobile.svg", header(num, kicker, title, dark, 400))
    write("experience.svg", experience())
    write("experience-mobile.svg", experience(True))
    areas_cards()
    write("stack.svg", stack())
    write("stack-mobile.svg", stack(True))
    write("footer.svg", footer())
    write("footer-mobile.svg", footer(True))
    write(
        "github.svg",
        github_stats_card.render_card(gh, PROFILE["github_user"], f"GITHUB | @{PROFILE['github_user'].upper()}", ORCHID),
    )
    write("leetcode.svg", leetcode_card.render_card(leetcode_for_card(lc), PROFILE["leetcode_user"]))
    (ROOT / "README.md").write_text(readme(), encoding="utf-8")
    print("rendered")


if __name__ == "__main__":
    main()
