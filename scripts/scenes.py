"""Vignettes for the focus-area cards. Each shows a real artefact of the work
(a ping sweep, a hardening checklist, a log with a brute-force burst) rather
than abstract shapes. 200 x 96 canvas, animated on a 6 s loop."""

from __future__ import annotations

import kit

AMBER, GREEN, RED = kit.AMBER, kit.GREEN, "#ef4444"
HAIR, META, BODY = kit.HAIR_STRONG, kit.META, kit.BODY


def t(x, y, s, fill=BODY, size=7.2, anchor=""):
    return kit.text(x, y, s, size, fill, "c", anchor)


def appear(content: str, at: float, hold: float = 0.92) -> str:
    """Fade a group in at `at` (0..1 of the loop) and out at the end."""
    a = max(at, 0.01)
    times = f"0;{a:.3f};{min(a + 0.05, 0.95):.3f};{hold:.3f};1"
    return f'<g opacity="0">{content}{kit.loop("opacity", "0;0;1;1;0", times, 6)}</g>'


def window(title: str) -> str:
    return (
        f'<rect x="6" y="4" width="188" height="88" rx="7" fill="{kit.BG}" stroke="{HAIR}"/>'
        f'<path d="M6 17H194" stroke="{HAIR}"/>'
        + "".join(f'<circle cx="{15 + i * 7}" cy="10.5" r="1.8" fill="{HAIR}"/>' for i in range(3))
        + t(100, 12.5, title, META, 6.2, "middle")
    )


def monitoring(ac):
    rows = [("gw     192.168.1.1", "2 ms", GREEN, "ok"), ("nas    192.168.1.20", "4 ms", GREEN, "ok"),
            ("cam    192.168.1.31", "timeout", AMBER, "!!"), ("pc     192.168.1.44", "1 ms", GREEN, "ok")]
    o = [window("ping sweep")]
    for i, (h, r, c, _) in enumerate(rows):
        y = 30 + i * 13
        o.append(appear(t(14, y, h) + t(186, y, r, c, anchor="end") + f'<circle cx="177" cy="{y - 2.4}" r="0" fill="{c}"/>', 0.08 + i * 0.14))
    chip, w = kit.chip(100, 74, "ALERT: cam down", AMBER, 6.4, 12, 6)
    o.append(appear(chip, 0.7))
    return "".join(o)


def baselines(ac):
    rows = [("sshd  PermitRootLogin no", GREEN, "pass"), ("ufw   default deny in", GREEN, "pass"),
            ("disk  encryption off", AMBER, "fix"), ("pkgs  unattended-upgrades", GREEN, "pass")]
    o = [window("baseline audit")]
    for i, (s, c, v) in enumerate(rows):
        y = 30 + i * 13
        mark = (f'<path transform="translate(179 {y - 2.5})" d="{kit.TICK}" fill="none" stroke="{c}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'
                if v == "pass" else t(186, y, "FIX", c, 6.6, "end"))
        o.append(appear(t(14, y, s) + mark, 0.08 + i * 0.15))
    o.append(appear(t(14, 86, "score 3/4 · remediation prepared", META, 6.2), 0.72))
    return "".join(o)


def supply(ac):
    st = [("build", 12), ("scan", 58), ("sign", 104), ("ship", 150)]
    o = []
    for i, (n, x) in enumerate(st):
        if i:
            o.append(f'<path d="M{st[i-1][1]+36} 34H{x}" stroke="{HAIR}" stroke-width="1.6"/>')
        o.append(f'<rect x="{x}" y="22" width="36" height="24" rx="6" fill="{kit.CARD}" stroke="{HAIR}"/>')
        o.append(t(x + 18, 37, n, BODY, 7, "middle"))
    o.append(kit.beam("M48 34H150", 6, 0, 0.85, ac, 3, 12))
    o.append(t(14, 64, "lockfile pinned · sha256 ok", META, 6.4))
    o.append(appear(t(14, 76, "evil-pkg@9.9  not in lockfile", AMBER, 6.4) + t(186, 76, "BLOCKED", RED, 6.4, "end"), 0.3))
    o.append(appear(t(14, 87, "artifact signed · provenance attached", GREEN, 6.4), 0.62))
    return "".join(o)


def automation(ac):
    o = [window("plan --dry-run")]
    o.append(t(14, 29, "vlan 20  guest-iot"))
    o.append(appear(t(14, 41, "sw1   + vlan 20", ac) + t(14, 52, "sw2   + vlan 20", ac) + t(14, 63, "ap1   + ssid iot", ac), 0.15))
    o.append(appear(t(14, 76, "3 changes · nothing applied yet", META, 6.4), 0.4))
    o.append(appear(t(14, 87, "apply", BODY, 7) + f'<path transform="translate(44 84.5)" d="{kit.TICK}" fill="none" stroke="{GREEN}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>' + t(52, 87, "rollback saved", GREEN, 6.4), 0.62))
    return "".join(o)


def detection(ac):
    o = [window("auth.log")]
    ip = "203.0.113.9"
    for i in range(4):
        y = 29 + i * 11
        o.append(appear(t(14, y, f"02:1{i} failed root from ") + t(118, y, ip, AMBER), 0.06 + i * 0.1))
    o.append(appear(t(14, 74, "rule: 4 failures / 60 s", META, 6.4), 0.5))
    chip, w = kit.chip(128, 78, "BLOCKED", RED, 6.6, 12, 7)
    o.append(appear(chip, 0.62))
    return "".join(o)


def forensics(ac):
    ev = [("02:14", "ssh login", BODY), ("02:16", "new user: svc_bk", AMBER), ("02:19", "outbound :4444", AMBER), ("02:25", "logs cleared", AMBER)]
    o = [window("timeline · host-07")]
    o.append('<path d="M26 24V80" stroke="%s" stroke-width="1.4"/>' % HAIR)
    for i, (tm, s, c) in enumerate(ev):
        y = 30 + i * 14
        o.append(f'<circle cx="26" cy="{y - 2.4}" r="2.4" fill="{kit.BG}" stroke="{c}" stroke-width="1.4"/>')
        o.append(t(34, y, tm, META) + t(62, y, s, c))
    o.append(
        f'<g><circle cx="0" cy="0" r="9" fill="{ac}" fill-opacity="0.15" stroke="{ac}" stroke-width="1.8"/>'
        f'<path d="M6.5 6.5L12 12" stroke="{ac}" stroke-width="2.2" stroke-linecap="round"/>'
        '<animateMotion dur="6s" repeatCount="indefinite" calcMode="linear" keyPoints="0;0;0.33;0.33;0.66;0.66;1;1;0" keyTimes="0;0.1;0.25;0.4;0.55;0.7;0.85;0.95;1" path="M150 24V66"/></g>'
    )
    o.append(t(186, 87, "sha256 ✓ evidence intact", GREEN, 6, "end"))
    return "".join(o)


def web(ac):
    o = [f'<rect x="6" y="10" width="92" height="76" rx="7" fill="{kit.BG}" stroke="{HAIR}"/><path d="M6 24H98" stroke="{HAIR}"/>']
    o += [f'<circle cx="{14 + i * 7}" cy="17" r="1.8" fill="{HAIR}"/>' for i in range(3)]
    o.append(f'<rect x="12" y="32" width="46" height="6" rx="3" fill="{ac}" opacity="0.9"/><rect x="12" y="44" width="72" height="4" rx="2" fill="{HAIR}"/><rect x="12" y="53" width="60" height="4" rx="2" fill="{HAIR}"/>')
    o.append(f'<rect x="12" y="66" width="30" height="11" rx="5.5" fill="{ac}" opacity="0.85"/>' + t(27, 73.5, "Send", "#000", 6.4, "middle"))
    for i, (n, c) in enumerate([("API", "200"), ("DB", "ok"), ("cache", "hit")]):
        y = 12 + i * 25
        o.append(f'<rect x="130" y="{y}" width="64" height="20" rx="6" fill="{kit.CARD}" stroke="{HAIR}"/>')
        o.append(t(138, y + 13, n) + t(186, y + 13, c, GREEN, 7, "end"))
    o.append(f'<path d="M98 30H130M98 60H130" stroke="{HAIR}" stroke-width="1.5"/>')
    o.append(t(114, 26, "POST", META, 5.6, "middle"))
    o.append(kit.beam("M98 30H130", 4, 0, 0.5, ac, 2.2, 20))
    o.append(kit.beam("M130 60H98", 4, 2, 0.5, GREEN, 2.2, 20))
    return "".join(o)


SCENES = {"forward-deployed": monitoring, "landing-zones": baselines, "iac-cicd": supply,
          "cloud-networking": automation, "mlops-genai": detection, "agent-tooling": forensics, "full-stack": web}
