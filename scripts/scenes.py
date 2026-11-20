"""Focus-area vignettes: one short story per area, drawn from the real work.

200 x 96 canvas, one 8 s loop. Every state change is keyed on the same
timeline, so the story reads in order: something happens, the system reacts,
the result lands. `animated=False` renders the state at 90% of the loop
(the finished frame) with no SMIL, for reduced-motion and static previews.
"""

from __future__ import annotations

D = 8.0
FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
BG, CARD = "#050505", "#0e0e0e"
HAIR, META, BODY = "rgba(255,255,255,0.16)", "rgba(255,255,255,0.55)", "rgba(255,255,255,0.88)"
ACC, GREEN, AMBER, RED = "#ff7a45", "#2fd58a", "#f29a38", "#ef4444"
END = 0.9  # the frame static mode shows


# ── primitives ────────────────────────────────────────────────────────────
def pts_attr(pts):
    pts = sorted(pts)
    if pts[0][0] > 0:
        pts = [(0.0, pts[0][1])] + pts
    if pts[-1][0] < 1:
        pts = pts + [(1.0, pts[-1][1])]
    return ";".join(f"{t:.3f}" for t, _ in pts), ";".join(str(v) for _, v in pts)


def tr(attr, pts):
    kt, vs = pts_attr(pts)
    return f'<animate attributeName="{attr}" values="{vs}" keyTimes="{kt}" dur="{D}s" repeatCount="indefinite"/>'


def tr_t(kind, pts):
    kt, vs = pts_attr(pts)
    return (f'<animateTransform attributeName="transform" type="{kind}" values="{vs}" '
            f'keyTimes="{kt}" dur="{D}s" repeatCount="indefinite"/>')


def vis(content, a, b, animated, f=0.02):
    """Show `content` from a to b (fractions of the loop)."""
    if not animated:
        return f"<g>{content}</g>" if a <= END < b else ""
    pts = []
    pts.append((0, 1 if a <= 0.001 else 0))
    if a > 0.001:
        pts += [(a, 0), (a + f, 1)]
    if b < 0.999:
        pts += [(b - f, 1), (b, 0)]
    return f'<g opacity="0">{content}{tr("opacity", pts)}</g>'


def t(x, y, s, fill=BODY, size=6.4, anchor="start", weight=""):
    w = f' font-weight="{weight}"' if weight else ""
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}"{w}>{s}</text>')


def tick(x, y, c, w=1.7):
    return (f'<path transform="translate({x} {y})" d="M-3 0.3l2.1 2.2 4-4.4" fill="none" stroke="{c}" '
            f'stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')


def cross(x, y, c, w=1.7):
    return (f'<path transform="translate({x} {y})" d="M-2.4-2.4l4.8 4.8M2.4-2.4l-4.8 4.8" fill="none" '
            f'stroke="{c}" stroke-width="{w}" stroke-linecap="round"/>')


def chip(x, y, label, c, anchor="start", size=6, h=11):
    w = len(label) * size * 0.6 + 12
    x0 = x if anchor == "start" else x - w / 2 if anchor == "middle" else x - w
    return (f'<rect x="{x0:.1f}" y="{y}" width="{w:.1f}" height="{h}" rx="{h/2}" fill="{c}" fill-opacity="0.13" '
            f'stroke="{c}" stroke-opacity="0.75"/>' + t(f"{x0 + w/2:.1f}", y + h / 2 + size * 0.34, label, c, size, "middle"))


def packet(path, a, b, color, animated, r=1.9):
    if not animated:
        return ""
    dot = (f'<circle r="{r}" fill="{color}"><animateMotion dur="{D}s" repeatCount="indefinite" '
           f'calcMode="linear" keyPoints="0;0;1;1" keyTimes="0;{a:.3f};{b:.3f};1" path="{path}"/></circle>'
           f'<circle r="{r*2.4}" fill="{color}" opacity="0.18"><animateMotion dur="{D}s" repeatCount="indefinite" '
           f'calcMode="linear" keyPoints="0;0;1;1" keyTimes="0;{a:.3f};{b:.3f};1" path="{path}"/></circle>')
    return vis(dot, a - 0.005, b + 0.03, True, 0.005)


def pulse(cx, cy, c, animated, r0=4, r1=15, dur=2.0, delay=0):
    if not animated:
        return ""
    return (f'<circle cx="{cx}" cy="{cy}" r="{r0}" fill="none" stroke="{c}" stroke-width="1">'
            f'<animate attributeName="r" values="{r0};{r1}" dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0.7;0" dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/></circle>')


def frame(title, right=""):
    dots = "".join(f'<circle cx="{14 + i * 6.5}" cy="10.5" r="1.7" fill="{HAIR}"/>' for i in range(3))
    return (f'<rect x="3.5" y="3.5" width="193" height="89" rx="8" fill="{BG}" stroke="{HAIR}"/>'
            f'<path d="M3.5 17H196.5" stroke="{HAIR}"/>{dots}{t(100, 12.6, title, META, 5.8, "middle")}{right}')


def live_dot(x, y, c, animated):
    ring = (f'<circle cx="{x}" cy="{y}" r="2" fill="none" stroke="{c}" stroke-width="0.8">'
            f'<animate attributeName="r" values="2;5" dur="1.8s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0.8;0" dur="1.8s" repeatCount="indefinite"/></circle>') if animated else ""
    return f'<circle cx="{x}" cy="{y}" r="2" fill="{c}"/>{ring}'


def node(cx, cy, w, h, label, stroke, fill=CARD, size=5.6, tc=BODY):
    return (f'<rect x="{cx - w/2}" y="{cy - h/2}" width="{w}" height="{h}" rx="4" fill="{fill}" stroke="{stroke}" stroke-width="1"/>'
            + t(cx, cy + size * 0.35, label, tc, size, "middle"))


# ── 1. network monitoring ─────────────────────────────────────────────────
def monitoring(an=True):
    gw = (100, 52)
    nodes = {"nas": (36, 34), "pc": (36, 70), "cam-01": (164, 34), "ap-02": (164, 70)}
    o = frame("network · live")
    o += vis(live_dot(150, 10.5, GREEN, an) + t(155, 12.6, "4/4 up", GREEN, 5.8), 0, 0.47, an)
    o += vis(live_dot(150, 10.5, AMBER, an) + t(155, 12.6, "3/4 up", AMBER, 5.8), 0.47, 0.999, an)
    for name, (x, y) in nodes.items():
        bad = name == "cam-01"
        line = f'<path d="M{gw[0]} {gw[1]}L{x} {y}" stroke="{HAIR}" stroke-width="1.2"/>'
        o += line
        if bad:
            o += vis(f'<path d="M{gw[0]} {gw[1]}L{x} {y}" stroke="{GREEN}" stroke-opacity="0.55" stroke-width="1.2"/>', 0, 0.47, an)
            o += vis(f'<path d="M{gw[0]} {gw[1]}L{x} {y}" stroke="{AMBER}" stroke-width="1.2" stroke-dasharray="2.5 2.5"/>' + cross((gw[0] + x) / 2, (gw[1] + y) / 2, AMBER, 1.5), 0.47, 0.999, an)
        else:
            o += f'<path d="M{gw[0]} {gw[1]}L{x} {y}" stroke="{GREEN}" stroke-opacity="0.55" stroke-width="1.2"/>'
        # outbound + return probes
        path = f"M{gw[0]} {gw[1]}L{x} {y}"
        back = f"M{x} {y}L{gw[0]} {gw[1]}"
        if an:
            for k, (pa, pb) in enumerate([(0.02, 0.1), (0.14, 0.22), (0.26, 0.34), (0.38, 0.46)]):
                o += packet(path, pa, pb, ACC, True, 1.5)
                o += packet(back, pa + 0.05, pb + 0.05, GREEN, True, 1.5) if not (bad and pa >= 0.38) else ""
            if not bad:
                for k, (pa, pb) in enumerate([(0.5, 0.58), (0.62, 0.7), (0.74, 0.82)]):
                    o += packet(path, pa, pb, ACC, True, 1.5)
                    o += packet(back, pa + 0.05, pb + 0.05, GREEN, True, 1.5)
            else:
                for pa, pb in [(0.5, 0.58), (0.66, 0.74), (0.82, 0.9)]:
                    o += packet(path, pa, pb, AMBER, True, 1.5)
        if bad:
            o += vis(node(x, y, 34, 15, name, GREEN), 0, 0.47, an)
            o += vis(node(x, y, 34, 15, name, AMBER, "#1a1105", tc=AMBER) + pulse(x, y, AMBER, an, 9, 20), 0.47, 0.999, an)
        else:
            o += node(x, y, 34, 15, name, "rgba(255,255,255,0.28)")
    # gateway
    o += pulse(gw[0], gw[1], ACC, an, 8, 22, 2.0, 0) + pulse(gw[0], gw[1], ACC, an, 8, 22, 2.0, 1.0)
    o += f'<circle cx="{gw[0]}" cy="{gw[1]}" r="9" fill="{CARD}" stroke="{ACC}" stroke-width="1.4"/>'
    o += f'<path d="M95 54h10M97 51.5h6M99 49h2" stroke="{ACC}" stroke-width="1.3" stroke-linecap="round"/>'
    # alert
    o += vis(chip(100, 79, "ALERT  cam-01: 3 probes lost", AMBER, "middle", 5.4, 10), 0.55, 0.999, an)
    return o


# ── 2. security baselines ─────────────────────────────────────────────────
def baselines(an=True):
    C = 2 * 3.14159 * 17
    rows = ["SSH root login: off", "Firewall: default deny", "Auto security updates", "Disk encryption"]
    o = frame("baseline audit · host-07")
    for i, label in enumerate(rows):
        y = 30 + i * 11.5
        o += t(12, y, label)
        at = 0.08 + i * 0.09
        if i < 3:
            o += vis(tick(115, y - 2.2, GREEN), at, 0.999, an)
        else:
            o += vis(f'<rect x="8" y="{y - 7.5}" width="116" height="10.5" rx="3" fill="{AMBER}" fill-opacity="0.1"/>' + t(122, y, "FAIL", AMBER, 5.6, "end"), at, 0.6, an)
            o += vis(tick(115, y - 2.2, GREEN) + t(122, y, "", GREEN), 0.64, 0.999, an)
    # ring
    cx, cy = 160, 52
    o += f'<circle cx="{cx}" cy="{cy}" r="17" fill="none" stroke="{HAIR}" stroke-width="4.5"/>'
    if an:
        o += (f'<circle cx="{cx}" cy="{cy}" r="17" fill="none" stroke="{AMBER}" stroke-width="4.5" stroke-linecap="round" '
              f'stroke-dasharray="{C:.1f}" stroke-dashoffset="{C:.1f}" transform="rotate(-90 {cx} {cy})">'
              + tr("stroke-dashoffset", [(0.1, C), (0.42, C * 0.25), (0.6, C * 0.25), (0.78, 0)])
              + tr("stroke", [(0, AMBER), (0.6, AMBER), (0.64, GREEN)]).replace('attributeName="stroke"', 'attributeName="stroke"')
              + "</circle>")
    else:
        o += (f'<circle cx="{cx}" cy="{cy}" r="17" fill="none" stroke="{GREEN}" stroke-width="4.5" stroke-linecap="round" '
              f'transform="rotate(-90 {cx} {cy})"/>')
    o += vis(t(cx, cy + 3, "75%", AMBER, 9, "middle", "700"), 0.42, 0.66, an)
    o += vis(t(cx, cy + 3, "100%", GREEN, 8.4, "middle", "700"), 0.78 if an else 0, 0.999, an) if an else t(cx, cy + 3, "100%", GREEN, 8.4, "middle", "700")
    o += t(cx, 79, "compliance", META, 4.8, "middle")
    o += vis(chip(12, 77, "fix applied · rollback saved", GREEN, "start", 5.4, 10), 0.68, 0.999, an)
    o += vis(chip(12, 77, "remediation prepared", AMBER, "start", 5.4, 10), 0.4, 0.6, an)
    return o


# ── 3. pipeline & supply chain ────────────────────────────────────────────
def supply(an=True):
    xs = [28, 64, 100, 136, 172]
    names = ["source", "build", "scan", "sign", "ship"]
    o = frame("pipeline · release")
    for i in range(4):
        o += f'<path d="M{xs[i] + 15} 40H{xs[i + 1] - 15}" stroke="{HAIR}" stroke-width="1.4"/>'
    for x, n in zip(xs, names):
        o += node(x, 40, 30, 18, n, "rgba(255,255,255,0.28)")
    # rejected package
    bad = f'<rect x="-4" y="-4" width="8" height="8" rx="2" fill="{RED}"/><path d="M-4 -1H4" stroke="#000" stroke-opacity="0.45"/>'
    good = f'<rect x="-4" y="-4" width="8" height="8" rx="2" fill="{GREEN}"/><path d="M-4 -1H4" stroke="#000" stroke-opacity="0.45"/>'
    # rejection and pass highlights first, so the packages ride on top
    o += vis(node(100, 40, 30, 18, "scan", RED, "#1a0707", tc=RED) + pulse(100, 40, RED, an, 10, 20), 0.2, 0.4, an)
    for x, n, a in [(64, "build", 0.5), (100, "scan", 0.64), (136, "sign", 0.76), (172, "ship", 0.9)]:
        o += vis(node(x, 40, 30, 18, n, GREEN), a, 0.999, an)
    if an:
        o += (f'<g opacity="0">{bad}'
              + tr_t("translate", [(0.04, "14 25"), (0.2, "100 25"), (0.3, "100 25"), (0.38, "100 25")])
              + tr("opacity", [(0.03, 0), (0.05, 1), (0.3, 1), (0.38, 0)]) + "</g>")
        o += (f'<g opacity="0">{good}'
              + tr_t("translate", [(0.4, "14 25"), (0.5, "64 25"), (0.56, "64 25"), (0.64, "100 25"), (0.7, "100 25"),
                                   (0.76, "136 25"), (0.8, "136 25"), (0.9, "172 25")])
              + tr("opacity", [(0.39, 0), (0.41, 1), (0.95, 1), (0.99, 0)]) + "</g>")
    else:
        o += f'<g transform="translate(172 25)">{good}</g>'
    # status log
    o += vis(cross(14, 63, RED) + t(21, 65, "evil-pkg@9.9 blocked: not in lockfile", RED, 5.6), 0.3, 0.999, an)
    o += vis(tick(14, 74, GREEN) + t(21, 76, "sha256 verified · SBOM attached", GREEN, 5.6), 0.66, 0.999, an)
    o += vis(tick(14, 85, GREEN) + t(21, 87, "signed · provenance attached", GREEN, 5.6), 0.8, 0.999, an)
    return o


# ── 4. network automation ─────────────────────────────────────────────────
def automation(an=True):
    o = frame("change · vlan 20")
    diff = [("vlan 20", BODY, ""), ("+ name guest-iot", ACC, "+"), ("+ ports 12-16", ACC, "+"), ("+ ssid iot-net", ACC, "+")]
    for i, (s, c, p) in enumerate(diff):
        o += vis(t(12, 30 + i * 10.5, s, c, 6), 0.04 + i * 0.07, 0.999, an)
    o += vis(f'<rect x="8" y="{30 + 10.5 - 8}" width="100" height="31.5" rx="3" fill="{ACC}" fill-opacity="0.07"/>', 0.15, 0.999, an)
    # dry-run badge, then applied
    o += vis(chip(12, 76, "DRY-RUN · 3 changes · 0 applied", AMBER, "start", 5.2, 10), 0.3, 0.5, an)
    o += vis(chip(12, 76, "APPLIED 3/3 · rollback saved", GREEN, "start", 5.2, 10), 0.82, 0.999, an)
    # apply button
    btn = f'<rect x="118" y="26" width="26" height="12" rx="6" fill="{ACC}"/>' + t(131, 34, "apply", "#000", 5.8, "middle", "700")
    o += vis(btn, 0.46, 0.999, an)
    o += vis(f'<rect x="118" y="26" width="26" height="12" rx="6" fill="none" stroke="{ACC}"><animate attributeName="opacity" values="1;0" dur="0.6s" repeatCount="3"/></rect>' if an else "", 0.5, 0.62, an)
    # devices
    devs = [("sw1", 32), ("sw2", 47), ("ap1", 62)]
    o += f'<path d="M131 40V{devs[0][1]}M131 {devs[0][1]}V{devs[2][1]}" stroke="{HAIR}" stroke-width="1.2" fill="none"/>' if False else ""
    o += f'<path d="M131 38V62" stroke="{HAIR}" stroke-width="1.2"/>'
    for i, (n, y) in enumerate(devs):
        o += f'<path d="M131 {y}H150" stroke="{HAIR}" stroke-width="1.2"/>'
        o += f'<rect x="150" y="{y - 7}" width="40" height="14" rx="4" fill="{CARD}" stroke="rgba(255,255,255,0.28)"/>'
        o += t(156, y + 2.2, n, BODY, 5.8) + f'<circle cx="182" cy="{y}" r="2" fill="{AMBER}" fill-opacity="0.8"/>'
        at = 0.6 + i * 0.07
        o += vis(f'<rect x="150" y="{y - 7}" width="40" height="14" rx="4" fill="{CARD}" stroke="{GREEN}"/>' + t(156, y + 2.2, n, BODY, 5.8) + tick(182, y - 0.3, GREEN, 1.5), at, 0.999, an)
        o += packet(f"M131 38V{y}H150", at - 0.1, at, ACC, an, 1.6)
    o += packet("M144 32H131V38", 0.54, 0.6, ACC, an, 1.6)
    return o


# ── 5. detection & incident response ──────────────────────────────────────
def detection(an=True):
    ip = "203.0.113.9"
    lines = [("02:14", "ssh ok      alice", False), ("02:15", f"failed root {ip}", True),
             ("02:15", f"failed root {ip}", True), ("02:16", f"failed root {ip}", True),
             ("02:16", f"failed root {ip}", True)]
    o = frame("auth.log · detection")
    fails = 0
    for i, (tm, s, bad) in enumerate(lines):
        y = 29 + i * 9
        at = 0.04 + i * 0.075
        row = t(10, y, tm, META, 5.6) + t(32, y, s.replace(ip, ""), AMBER if bad else BODY, 5.6)
        if bad:
            row += t(32 + 12 * 3.36, y, ip, AMBER, 5.6, weight="700")
        o += vis(row, at, 0.999, an)
        if bad:
            o += vis(f'<rect x="8" y="{y - 6.2}" width="112" height="8.8" rx="2" fill="{AMBER}" fill-opacity="0.1"/>', at, 0.999, an)
    # rule card
    o += f'<rect x="128" y="22" width="62" height="40" rx="5" fill="{CARD}" stroke="rgba(255,255,255,0.28)"/>'
    o += t(134, 31, "brute_force", BODY, 5.6) + t(134, 38, ">= 4 / 60s", META, 5)
    fails_at = [0.04 + i * 0.075 for i, l in enumerate(lines) if l[2]]
    for k, at in enumerate(fails_at):
        o += f'<circle cx="{138 + k * 11}" cy="48" r="3.2" fill="none" stroke="{HAIR}"/>'
        o += vis(f'<circle cx="{138 + k * 11}" cy="48" r="3.2" fill="{AMBER}"/>', at + 0.02, 0.999, an)
    o += vis(f'<rect x="128" y="22" width="62" height="40" rx="5" fill="{RED}" fill-opacity="0.12" stroke="{RED}"/>' + t(159, 58.5, "TRIGGERED", RED, 5.4, "middle", "700") + (pulse(159, 42, RED, an, 20, 30, 1.6) if False else ""), 0.5, 0.999, an)
    # response
    shield = f'<path d="M14 71l6-2.4 6 2.4v5.4c0 3.4-2.6 5.4-6 6.6-3.4-1.2-6-3.2-6-6.6z" fill="{GREEN}" fill-opacity="0.15" stroke="{GREEN}" stroke-width="1.2"/>'
    o += vis(shield + tick(20, 76, GREEN, 1.4) + t(32, 77, f"BLOCKED {ip}", GREEN, 6, weight="700") + t(32, 85, "firewall rule added · analyst alerted", META, 5), 0.66, 0.999, an)
    return o


# ── 6. analysis & forensics ───────────────────────────────────────────────
def forensics(an=True):
    xs = [32, 76, 120, 164]
    ev = [("02:14", "ssh login", False, "alice"), ("02:16", "new user", True, "svc_bk"), ("02:19", "outbound", True, ":4444"), ("02:25", "logs wiped", True, "auth.log")]
    hashes = ["a3f9", "7c21", "e08b", "5d4e"]
    o = frame("timeline · host-07")
    o += vis(t(186, 12.6, "analyzing…", META, 5.6, "end"), 0, 0.8, an)
    o += vis(tick(150, 10.5, GREEN, 1.4) + t(186, 12.6, "sealed", GREEN, 5.8, "end"), 0.8, 0.999, an)
    o += f'<path d="M16 42H184" stroke="{HAIR}" stroke-width="1.4"/>'
    for i, ((tm, s, bad, sub), x) in enumerate(zip(ev, xs)):
        at = [0.12, 0.3, 0.46, 0.62][i]
        o += t(x, 33, tm, META, 5.6, "middle")
        o += f'<circle cx="{x}" cy="42" r="3.2" fill="{BG}" stroke="rgba(255,255,255,0.4)" stroke-width="1.3"/>'
        c = AMBER if bad else GREEN
        o += vis(f'<circle cx="{x}" cy="42" r="3.2" fill="{c}"/>' + t(x, 53, s, c if bad else BODY, 5.4, "middle") + t(x, 60, sub, META, 4.8, "middle"), at, 0.999, an)
        # hash chain block
        o += f'<rect x="{x - 12}" y="68" width="24" height="12" rx="3" fill="{CARD}" stroke="{HAIR}"/>'
        o += vis(f'<rect x="{x - 12}" y="68" width="24" height="12" rx="3" fill="{CARD}" stroke="{GREEN}" stroke-opacity="0.8"/>' + t(x, 76.2, hashes[i], GREEN, 5.4, "middle"), at + 0.04, 0.999, an)
        if i:
            o += f'<path d="M{xs[i - 1] + 12} 74H{x - 12}" stroke="{HAIR}" stroke-width="1.2"/>'
            o += vis(f'<path d="M{xs[i - 1] + 12} 74H{x - 12}" stroke="{GREEN}" stroke-opacity="0.8" stroke-width="1.2"/>', at + 0.04, 0.999, an)
    o += t(100, 90, "sha256 chain of custody", META, 4.8, "middle")
    # flagged banner
    o += vis(chip(100, 20.5, "pivot: svc_bk created at 02:16", AMBER, "middle", 5, 9), 0.34, 0.999, an) if False else ""
    lens = (f'<circle r="8" fill="{ACC}" fill-opacity="0.12" stroke="{ACC}" stroke-width="1.6"/>'
            f'<path d="M5.8 5.8L10.5 10.5" stroke="{ACC}" stroke-width="2" stroke-linecap="round"/>')
    if an:
        o += (f'<g>{lens}' + tr_t("translate", [(0.06, "32 42"), (0.14, "32 42"), (0.24, "76 42"), (0.32, "76 42"),
                                                  (0.4, "120 42"), (0.48, "120 42"), (0.56, "164 42"), (0.7, "164 42"),
                                                  (0.8, "164 42")]) + tr("opacity", [(0.04, 0), (0.06, 1), (0.8, 1), (0.86, 0)]) + "</g>")
    return o


# ── 7. websites & backends ────────────────────────────────────────────────
def web(an=True):
    o = (f'<rect x="4" y="6" width="94" height="84" rx="8" fill="{BG}" stroke="{HAIR}"/><path d="M4 19H98" stroke="{HAIR}"/>'
         + "".join(f'<circle cx="{12 + i * 6}" cy="12.5" r="1.6" fill="{HAIR}"/>' for i in range(3))
         + f'<rect x="32" y="9" width="58" height="7" rx="3.5" fill="rgba(255,255,255,0.06)"/>' + t(61, 14.2, "unalivin.dev", META, 4.8, "middle"))
    # page skeleton fills in after the response
    o += f'<rect x="11" y="26" width="30" height="5" rx="2.5" fill="{HAIR}"/>'
    bars = [(11, 36, 76, 3.6), (11, 43, 64, 3.6), (11, 50, 70, 3.6)]
    for i, (x, y, w, h) in enumerate(bars):
        o += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="1.8" fill="{HAIR}" opacity="0.5"/>'
        if an:
            o += (f'<rect x="{x}" y="{y}" width="0" height="{h}" rx="1.8" fill="{ACC}" opacity="0.8">'
                  + tr("width", [(0.66 + i * 0.05, 0), (0.74 + i * 0.05, w)]) + "</rect>")
        else:
            o += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="1.8" fill="{ACC}" opacity="0.8"/>'
    o += f'<rect x="11" y="26" width="30" height="5" rx="2.5" fill="{ACC}"/>' if not an else vis(f'<rect x="11" y="26" width="30" height="5" rx="2.5" fill="{ACC}"/>', 0.64, 0.999, an)
    # button + press
    o += f'<rect x="11" y="72" width="34" height="13" rx="6.5" fill="{ACC}"/>' + t(28, 80.8, "Send", "#000", 6, "middle", "700")
    o += vis(f'<rect x="9" y="70" width="38" height="17" rx="8.5" fill="none" stroke="{ACC}" stroke-width="1.2"/>', 0.05, 0.14, an)
    o += vis(chip(90, 58, "200 OK · 42 ms", GREEN, "end", 5, 10), 0.66, 0.999, an)
    # services
    svc = [("API", 12, "200"), ("DB", 38, "12ms"), ("cache", 64, "hit")]
    o += f'<path d="M98 75H116V25H98M116 51H128M116 25H128M116 77H128" stroke="{HAIR}" stroke-width="1.2" fill="none"/>' if False else ""
    o += f'<path d="M98 75H112" stroke="{HAIR}" stroke-width="1.3"/><path d="M112 75V25H128" stroke="{HAIR}" stroke-width="1.3" fill="none"/><path d="M112 51H128M112 75H128" stroke="{HAIR}" stroke-width="1.3"/>'
    for n, y, v in svc:
        o += f'<rect x="128" y="{y + 6}" width="66" height="20" rx="6" fill="{CARD}" stroke="rgba(255,255,255,0.28)"/>' + t(136, y + 19, n, BODY, 6.2)
    st = [("200", 0.36), ("12ms", 0.5), ("hit", 0.5)]
    for (n, y, v), (_, at) in zip(svc, st):
        o += vis(t(186, y + 19, v, GREEN, 6.2, "end") + f'<rect x="128" y="{y + 6}" width="66" height="20" rx="6" fill="none" stroke="{GREEN}" stroke-opacity="0.8"/>', at, 0.999, an)
    o += packet("M98 75H112V25H128", 0.1, 0.24, ACC, an) + packet("M112 51H128", 0.26, 0.36, ACC, an) + packet("M112 75H128", 0.26, 0.36, ACC, an)
    o += packet("M128 75H112V75H98", 0.52, 0.62, GREEN, an) + packet("M128 51H112V75", 0.5, 0.6, GREEN, an)
    return o


def _wrap(fn):
    def scene(accent=ACC, animated=True):
        return fn(animated)
    return scene


SCENES = {"forward-deployed": _wrap(monitoring), "landing-zones": _wrap(baselines), "iac-cicd": _wrap(supply),
          "cloud-networking": _wrap(automation), "mlops-genai": _wrap(detection), "agent-tooling": _wrap(forensics),
          "full-stack": _wrap(web)}
