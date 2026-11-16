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
TONES = [ORCHID, CREAM, "#8576e0"]

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
    """An animated 200 x 96 vignette for the area."""
    hair, strong = kit.HAIR_STRONG, kit.META
    o = []
    if key == "forward-deployed":
        xs = [28, 72, 116, 160]
        o.append(f'<path d="M{xs[0]} 40H{xs[-1]}" stroke="{hair}" stroke-width="2"/>')
        o.append(kit.beam(f"M{xs[0]} 40H{xs[-1]}", 4, 0, 1.0, accent, 2.5, 14))
        for i, x in enumerate(xs):
            warn = i == 2
            col = AMBER if warn else accent
            o.append(f'<circle cx="{x}" cy="40" r="10" fill="{kit.BG}" stroke="{col}" stroke-width="2"/>')
            o.append(f'<circle cx="{x}" cy="40" r="3.4" fill="{col}"/>')
            if warn:
                o.append(
                    f'<circle cx="{x}" cy="40" r="10" fill="none" stroke="{AMBER}" stroke-width="1.5">'
                    '<animate attributeName="r" values="10;19" dur="2s" repeatCount="indefinite"/>'
                    '<animate attributeName="opacity" values="0.9;0" dur="2s" repeatCount="indefinite"/></circle>'
                )
        o.append(f'<rect x="28" y="66" width="132" height="8" rx="4" fill="{kit.HAIR_FILL}" stroke="{hair}"/>')
        o.append(
            f'<rect x="28" y="66" width="96" height="8" rx="4" fill="{AMBER}">'
            + kit.loop("width", "30;96;96;30", "0;0.5;0.9;1", 6)
            + "</rect>"
        )
    elif key == "landing-zones":
        for i in range(4):
            y = 10 + i * 21
            o.append(f'<rect x="34" y="{y}" width="14" height="14" rx="4" fill="{kit.BG}" stroke="{accent}" stroke-width="1.6"/>')
            o.append(_tick(41, y + 7.5, GREEN if i != 2 else AMBER, i, 5))
            w = [112, 86, 100, 70][i]
            o.append(f'<rect x="58" y="{y + 4}" width="{w}" height="6" rx="3" fill="{hair}"/>')
    elif key == "iac-cicd":
        xs = [10, 58, 106, 154]
        for i in range(3):
            o.append(f'<path d="M{xs[i] + 36} 48H{xs[i + 1]}" stroke="{hair}" stroke-width="2"/>')
        o.append(kit.beam("M46 48H154", 5, 0, 0.8, accent, 3, 12))
        for i, x in enumerate(xs):
            o.append(f'<rect x="{x}" y="30" width="36" height="36" rx="8" fill="{kit.CARD}" stroke="{hair}"/>')
            o.append(f'<rect x="{x + 8}" y="40" width="20" height="4" rx="2" fill="{hair}"/>')
            o.append(f'<rect x="{x + 8}" y="50" width="12" height="4" rx="2" fill="{hair}"/>')
            o.append(_tick(x + 18, 20, GREEN, i, 4))
    elif key == "cloud-networking":
        o.append(f'<rect x="10" y="14" width="68" height="68" rx="9" fill="{kit.BG}" stroke="{hair}"/>')
        for i, w in enumerate([40, 28, 46]):
            o.append(f'<rect x="20" y="{26 + i * 16}" width="{w}" height="5" rx="2.5" fill="{accent}" opacity="0.9"/>')
        for i in range(3):
            y = 14 + i * 26
            o.append(f'<path d="M78 48C100 48 100 {y + 10} 124 {y + 10}" fill="none" stroke="{hair}" stroke-width="1.6"/>')
            o.append(kit.beam(f"M78 48C100 48 100 {y + 10} 124 {y + 10}", 6, i * 0.9, 0.35, accent, 2.2, 14))
            o.append(f'<rect x="124" y="{y}" width="66" height="20" rx="6" fill="{kit.CARD}" stroke="{hair}"/>')
            o.append(
                f'<circle cx="178" cy="{y + 10}" r="3.6" fill="{AMBER}">'
                + kit.loop("fill", f"{AMBER};{AMBER};{GREEN};{GREEN}", "0;0.2;0.3;1", 6, i * 0.9)
                + "</circle>"
            )
    elif key == "mlops-genai":
        for i in range(5):
            y = 12 + i * 16
            w = [150, 120, 138, 104, 130][i]
            hot = i == 2
            o.append(f'<rect x="20" y="{y}" width="{w}" height="7" rx="3.5" fill="{AMBER if hot else hair}"' + (' opacity="0.9"' if hot else "") + "/>")
        o.append(
            f'<rect x="14" y="8" width="172" height="14" rx="4" fill="{accent}" opacity="0.18">'
            '<animateTransform attributeName="transform" type="translate" values="0 0;0 54;0 0" dur="6s" repeatCount="indefinite"/></rect>'
        )
        o.append(
            f'<g opacity="0">{kit.chip(128, 52, "ALERT", AMBER, 9, 18, 8)[0]}'
            + kit.loop("opacity", "0;0;1;1;0", "0;0.3;0.4;0.8;0.9", 6)
            + "</g>"
        )
    elif key == "agent-tooling":
        o.append(f'<rect x="38" y="8" width="96" height="80" rx="8" fill="{kit.CARD}" stroke="{hair}"/>')
        for i, w in enumerate([66, 52, 70, 44, 60]):
            o.append(f'<rect x="48" y="{20 + i * 13}" width="{w}" height="5" rx="2.5" fill="{hair}"/>')
        o.append(f'<rect x="48" y="46" width="70" height="5" rx="2.5" fill="{AMBER}" opacity="0.9"/>')
        o.append(
            f'<g><circle cx="0" cy="0" r="15" fill="{accent}" fill-opacity="0.14" stroke="{accent}" stroke-width="2.4"/>'
            f'<path d="M11 11L22 22" stroke="{accent}" stroke-width="3" stroke-linecap="round"/>'
            '<animateMotion dur="6s" repeatCount="indefinite" path="M58 28C84 28 100 40 118 58C100 70 84 70 58 56C84 40 70 30 58 28Z"/></g>'
        )
    else:
        o.append(f'<rect x="10" y="14" width="86" height="64" rx="8" fill="{kit.BG}" stroke="{hair}"/>')
        o.append(f'<path d="M10 28H96" stroke="{hair}"/>')
        for i, cx in enumerate([20, 28, 36]):
            o.append(f'<circle cx="{cx}" cy="21" r="2.2" fill="{hair}"/>')
        o.append(f'<rect x="20" y="38" width="50" height="6" rx="3" fill="{accent}" opacity="0.9"/>')
        o.append(f'<rect x="20" y="50" width="66" height="5" rx="2.5" fill="{hair}"/>')
        o.append(f'<rect x="20" y="60" width="38" height="5" rx="2.5" fill="{hair}"/>')
        for i in range(3):
            y = 14 + i * 24
            o.append(f'<rect x="128" y="{y}" width="62" height="18" rx="6" fill="{kit.CARD}" stroke="{hair}"/>')
            o.append(f'<circle cx="178" cy="{y + 9}" r="3" fill="{GREEN}"/>')
            o.append(f'<rect x="136" y="{y + 7}" width="26" height="4" rx="2" fill="{hair}"/>')
        o.append(f'<path d="M96 40H128" stroke="{hair}" stroke-width="1.6"/><path d="M96 62H128" stroke="{hair}" stroke-width="1.6"/>')
        o.append(kit.beam("M96 40H128", 4, 0, 0.5, accent, 2.4, 20))
        o.append(kit.beam("M128 62H96", 4, 2, 0.5, CREAM, 2.4, 20))
    return "".join(o)


def card(area: dict, index: int, w: float = 410, wide: bool = False) -> tuple[str, float]:
    key = area["key"]
    accent = TONES[index % 3]
    aw = 280 if wide else w
    art_h = 132
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
