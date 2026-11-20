"""Focus-area cards: one animated card per area, the same seven the website shows.

Cards use the kit from Sagargupta16's profile design (MIT); the scenes, the
copy and the layout are my own.
"""

from __future__ import annotations

import kit

ORCHID = kit.BLUE_LIGHT
CREAM = kit.SKY
SLATE = kit.BLUE_EDGE
AMBER = kit.AMBER
GREEN = kit.GREEN
TONES = ["#ff8a5c", "#d9954f", "#ef562d"]

SHORT = {
    "forward-deployed": "MONITORING",
    "landing-zones": "BASELINES",
    "iac-cicd": "SUPPLY CHAIN",
    "cloud-networking": "AUTOMATION",
    "mlops-genai": "DETECTION",
    "agent-tooling": "FORENSICS",
    "full-stack": "WEB & BACKEND",
}

ICON_STROKES = {
    "forward-deployed": ["M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18Z", "M3 12h18", "M12 3c3 3 3 15 0 18", "M12 3c-3 3-3 15 0 18"],
    "landing-zones": ["M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z", "M8.5 12l2.5 2.5 4.5-5"],
    "iac-cicd": ["M3 3h8v8H3z", "M13 13h8v8h-8z", "M7 11v4a2 2 0 0 0 2 2h4"],
    "cloud-networking": ["M9 2h6v6H9z", "M2 16h6v6H2z", "M16 16h6v6h-6z", "M12 8v4", "M5 16v-4h14v4"],
    "mlops-genai": ["M3 12h4l3-8 4 16 3-8h4"],
    "agent-tooling": ["M11 4a7 7 0 1 0 0 14 7 7 0 0 0 0-14Z", "M21 21l-5-5"],
    "full-stack": ["M8 8l-5 4 5 4", "M16 8l5 4-5 4", "M14 4l-4 16"],
    "terminal": ["M4 17l6-6-6-6", "M12 19h8"],
    "browser": ["M3 5h18v14H3z", "M3 10h18", "M7 7.5h.01"],
    "database": ["M4 6c0-1.7 3.6-3 8-3s8 1.3 8 3-3.6 3-8 3-8-1.3-8-3Z", "M4 6v12c0 1.7 3.6 3 8 3s8-1.3 8-3V6", "M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"],
    "sparkles": ["M12 3l1.8 4.7L18.5 9.5 13.8 11.3 12 16l-1.8-4.7L5.5 9.5l4.7-1.8Z", "M19 16l.8 2.2L22 19l-2.2.8L19 22l-.8-2.2L16 19l2.2-.8Z"],
    "wrench": ["M14.7 6.3a4 4 0 0 0 5 5L11 20a2.1 2.1 0 0 1-3-3Z", "M14.7 6.3a4 4 0 0 1 5-3l-2.5 2.5.8 2.2 2.2.8 2.5-2.5"],
}


def stroke_icon(key: str, x: float, y: float, size: float, color: str) -> str:
    paths = "".join(f'<path d="{d}"/>' for d in ICON_STROKES.get(key, ICON_STROKES["full-stack"]))
    return (
        f'<g transform="translate({x:g} {y:g}) scale({size / 24:.4f})" fill="none" stroke="{color}" '
        f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{paths}</g>'
    )


def _seq(i: int, n: int, dur: float = 6.0) -> tuple[str, str]:
    a = i / n
    b = (i + 1) / n
    pts = sorted({0.0, round(a, 4), round(min(a + 0.04, 1), 4), 1.0})
    vals = ["1" if t >= a + 0.04 - 1e-6 or False else "0" for t in pts]
    return ";".join(vals), ";".join(f"{t:g}" for t in pts)


def _tick(x: float, y: float, color: str, i: int, n: int, dur: float = 6) -> str:
    a = i / n
    times = f"0;{a:.3f};{min(a + 0.05, 0.99):.3f};0.92;1"
    return (
        f'<path transform="translate({x:g} {y:g})" d="{kit.TICK}" fill="none" stroke="{color}" stroke-width="2.2" '
        f'stroke-linecap="round" stroke-linejoin="round" opacity="0">'
        + kit.loop("opacity", "0;0;1;1;0", times, dur)
        + "</path>"
    )


def scene(key: str, accent: str) -> str:
    """An animated 200 x 96 vignette showing a real artefact of the area."""
    import scenes

    return scenes.SCENES.get(key, scenes.web)(accent)


def card(area: dict, index: int, w: float = 410, wide: bool = False) -> tuple[str, float]:
    key = area["key"]
    accent = TONES[index % 3]
    aw = 280 if wide else w
    art_h = 150
    pad = 22
    bx = aw + pad if wide else pad
    bw = (w - aw - pad * 2) if wide else (w - pad * 2)
    items = area["list"]
    summary_lines = kit.wrap_text(area.get("summary", ""), bw, 13)
    if wide:
        h = 30 + 26 + 20 * len(summary_lines) + 6 + 24 * len(items) + 26
        h = max(h, 170)
        ay, ah = 0, h
    else:
        ay, ah = 0, art_h
        h = art_h + 26 + 26 + 22 * len(summary_lines) + 8 + 24 * len(items) + 24
    label = f"{area['title']}. {area.get('summary', '')} " + "; ".join(items) + "."
    body = [kit.card_open(w, h, label, defs=kit.dot_pattern("dots"))]
    clip = f'<g clip-path="url(#card)">'
    art = [
        f'<rect x="1" y="1" width="{aw - (1 if wide else 2):g}" height="{ah:g}" fill="{accent}" fill-opacity="0.06"/>',
        f'<rect x="1" y="1" width="{aw - (1 if wide else 2):g}" height="{ah:g}" fill="url(#dots)"/>',
        f'<path d="M{aw if wide else 0} {0 if wide else ah}{"V" + format(h, "g") if wide else "H" + format(w, "g")}" stroke="{kit.HAIR}"/>',
    ]
    sc = min((aw - 24) / 200, (ah - 20) / 96, 1.6)
    sx = (aw - 200 * sc) / 2
    sy = ay + (ah - 96 * sc) / 2
    art.append(f'<g transform="translate({sx:g} {sy:g}) scale({sc:.3f})">{scene(key, accent)}</g>')
    body.append(clip + "".join(art) + "</g>")
    ty = (30 if wide else art_h + 34)
    head = (
        stroke_icon(key, bx, ty - 17, 20, accent)
        + kit.text(bx + 30, ty, area["title"], 16, kit.INK, "s")
    )
    y = ty + 26
    lines = []
    for ln in summary_lines:
        lines.append(kit.text(bx, y, ln, 13, kit.BODY, "b"))
        y += 20
    y += 6
    cols = 1
    colw = bw / cols
    for i, it in enumerate(items):
        cx = bx + (i % cols) * colw
        cy = y + (i // cols) * 24
        lines.append(
            f'<path transform="translate({cx + 5:g} {cy - 4:g})" d="{kit.TICK}" fill="none" stroke="{accent}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'
            + kit.text(cx + 18, cy, it, 12.5, kit.META if False else kit.BODY, "b")
        )
    body.append(kit.group(0.15 + index * 0.05, head + "".join(lines), "0 6"))
    body.append(kit.SVG_CLOSE)
    return "".join(body), h
