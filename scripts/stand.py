"""PR-Stand: stempelt die Zahlen aus pr-stand.json in Web, Druck und ATS; prüft Konsistenz und Frische.

Warum: Die PR-Zahl stand von Hand an 13 Stellen und war nach jedem Merge veraltet (29.09.2026: 57 statt 58).
Aufruf:  py -3 scripts/stand.py stempeln | pruefen | frische TAGE
"""
import datetime
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DATEN = REPO / "pr-stand.json"
WEB = REPO / "index.html"
DRUCK = [REPO / n for n in ("cv-print.html", "cv-print-en.html", "cv-print-marketing.html")] + \
        [REPO / "ats-cv" / n for n in ("Jason_Roschmann_CV_ATS.md", "Jason_Roschmann_CV_ATS_EN.md",
                                        "Jason_Roschmann_CV_Marketing_ATS.md")]
BADGE = REPO / "badge-prs.svg"
MON_DE = ["Jan.", "Feb.", "März", "Apr.", "Mai", "Juni", "Juli", "Aug.", "Sep.", "Okt.", "Nov.", "Dez."]
MON_EN = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
SPAN = re.compile(r'(<span data-pr="([a-z-]+)">)([^<]*)(</span>)')
FLEX = re.compile(r'(data-pr-flex="([a-z]+)" style="flex:)(\d+)(")')
JS = re.compile(r"(/\*pr-daten\*/)(.*?)(/\*pr-daten-ende\*/)", re.S)
DIA = re.compile(r"(<!-- pr-diagramm:start -->)(.*?)(<!-- pr-diagramm:end -->)", re.S)


def _tag(iso: str) -> datetime.date:
    return datetime.date.fromisoformat(iso[:10])


def werte(d: dict, druck: bool) -> dict:
    """Anzeige-Werte; Web datiert auf die letzte Zählung, Druck/ATS auf die letzte Zahlenänderung."""
    g, t, s = d["gemergt"], _tag(d["zahlen_stand"] if druck else d["stand"]), _tag(d["erster_merge"])
    return {"gesamt": str(g["gesamt"]), "flowki": str(g["flowki"]), "eigen": str(g["eigen"]),
            "kunden": str(g["kunden"]), "flowki-eroeffnet": str(d["eroeffnet"]["flowki"]),
            "stand-de": t.strftime("%d.%m.%Y"), "stand-en": f"{t.day} {MON_EN[t.month - 1]} {t.year}",
            "seit-de": f"{MON_DE[s.month - 1]} {s.year}", "seit-en": f"{MON_EN[s.month - 1]} {s.year}"}


def stempel_text(text: str, w: dict, d: dict) -> str:
    text = SPAN.sub(lambda m: m.group(1) + w[m.group(2)] + m.group(4), text)
    text = FLEX.sub(lambda m: m.group(1) + str(d["gemergt"][m.group(2)]) + m.group(4), text)
    g = d["gemergt"]
    js = json.dumps({"gesamt": g["gesamt"], "flowki": g["flowki"], "eigen": g["eigen"], "kunden": g["kunden"],
                     "flowkiEroeffnet": d["eroeffnet"]["flowki"]})
    text = JS.sub(lambda m: m.group(1) + js + m.group(3), text)
    return DIA.sub(lambda m: m.group(1) + diagramm(d) + m.group(3), text)


def diagramm(d: dict) -> str:
    """Summenlinie (Treppe) seit dem ersten Merge + Aufschlüsselung; statisches SVG, ohne JavaScript."""
    W, H, L, R, O, U = 640, 170, 36, 64, 14, 26   # R: Platz für eine dreistellige Endzahl (mobil 26er Schrift)
    start, ende, g = _tag(d["erster_merge"]), _tag(d["stand"]), d["gemergt"]
    tage, hoch = max(1, (ende - start).days), max(1, g["gesamt"])
    x = lambda t: L + (t - start).days / tage * (W - L - R)
    y = lambda v: O + (1 - v / hoch) * (H - O - U)
    pfad = f"M{x(start):.1f},{y(0):.1f}"
    for tag, summe in d["verlauf"]:
        pfad += f" H{x(_tag(tag)):.1f} V{y(summe):.1f}"
    pfad += f" H{x(ende):.1f}"
    ticks, m = [], datetime.date(start.year, start.month, 1)
    while m <= ende:
        if m >= start:
            ticks.append(f'<text x="{x(m):.1f}" y="{H - 8}" text-anchor="middle">1.{m.month}.</text>'
                         f'<line x1="{x(m):.1f}" x2="{x(m):.1f}" y1="{O}" y2="{H - U}" class="gl"/>')
        m = datetime.date(m.year + (m.month == 12), m.month % 12 + 1, 1)
    w = werte(d, druck=False)
    label = (f"Gemergte Pull Requests, aufsummiert seit {start.day}. {MON_DE[start.month - 1]} {start.year}: "
             f"{g['gesamt']} bis {w['stand-de']} – Flowki Studio {g['flowki']}, eigene Repos {g['eigen']}, "
             f"Kundenprojekte {g['kunden']}")
    return (f'<figure class="ghsum" role="img" aria-label="{label}"><svg viewBox="0 0 {W} {H}" aria-hidden="true">'
            f'<line x1="{L}" x2="{W - R}" y1="{y(0):.1f}" y2="{y(0):.1f}" class="gl"/>{"".join(ticks)}'
            f'<path d="{pfad} V{y(0):.1f} H{x(start):.1f}Z" class="fl-a"/><path d="{pfad}" class="fl-l"/>'
            f'<circle cx="{x(ende):.1f}" cy="{y(g["gesamt"]):.1f}" r="4" class="fl-p"/>'
            f'<text x="{x(ende) + 8:.1f}" y="{y(g["gesamt"]) + 4:.1f}" class="end">{g["gesamt"]}</text>'
            f'<text x="{L}" y="{H - 8}" text-anchor="start">{start.day}.{start.month}.</text></svg></figure>'
            f'<div class="ghbar" aria-hidden="true"><i class="fl" style="flex:{g["flowki"]}"></i>'
            f'<i class="cv" style="flex:{g["eigen"]}"></i><i class="ku" style="flex:{g["kunden"]}"></i></div>'
            f'<div class="ghl"><span class="fl">Flowki Studio {g["flowki"]}</span>'
            f'<span class="cv">eigene Repos {g["eigen"]}</span><span class="ku">Kundenprojekte {g["kunden"]}</span></div>')


def badge(d: dict) -> str:
    n = str(d["gemergt"]["gesamt"])
    lw, rw = 104, 12 + 7 * len(n)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{lw + rw}" height="20" role="img" '
            f'aria-label="gemergte Pull Requests: {n}"><rect width="{lw}" height="20" fill="#20262d"/>'
            f'<rect x="{lw}" width="{rw}" height="20" fill="#17784a"/><g fill="#fff" font-family="Verdana,sans-serif" '
            f'font-size="11"><text x="8" y="14">gemergte PRs</text>'
            f'<text x="{lw + rw / 2}" y="14" text-anchor="middle">{n}</text></g></svg>')


def veraltet(d: dict, tage: int, heute: str | None = None) -> bool:
    h = _tag(heute) if heute else datetime.datetime.now(datetime.timezone.utc).date()
    return not 0 <= (h - _tag(d["stand"])).days <= tage   # auch ein Stand in der Zukunft ist unplausibel


def fehlende_marker(name: str, text: str) -> list[str]:
    """Zerstörte Marker (z. B. beim Bearbeiten) ließen die Zahl still stehen – deshalb Mindestbestand je Datei."""
    if name != WEB.name:
        return [] if SPAN.search(text) else ["data-pr-Marker"]
    da = {m.group(2) for m in SPAN.finditer(text)}
    fehlt = [f"data-pr=\"{k}\"" for k in ("gesamt", "flowki", "flowki-eroeffnet", "stand-de", "seit-de") if k not in da]
    return fehlt + [n for n, rx in (("/*pr-daten*/", JS), ("<!-- pr-diagramm -->", DIA)) if not rx.search(text)]


def _ziele() -> list[tuple[Path, bool]]:
    return [(WEB, False)] + [(p, True) for p in DRUCK]


def main(argv: list[str]) -> int:
    d = json.loads(DATEN.read_text(encoding="utf-8"))
    befehl = argv[1] if len(argv) > 1 else ""
    if befehl == "frische":
        if veraltet(d, int(argv[2])):
            print(f"PR-Stand veraltet oder in der Zukunft: letzte Zählung {d['stand']}"); return 1
        print("PR-Stand frisch:", d["stand"]); return 0
    abweichend, kaputt = [], []
    for pfad, druck in _ziele():
        alt = pfad.read_bytes().decode("utf-8")
        kaputt += [f"{pfad.name}: {m}" for m in fehlende_marker(pfad.name, alt)]
        neu = stempel_text(alt, werte(d, druck), d)
        if neu != alt:
            abweichend.append(pfad.name)
            if befehl == "stempeln":
                pfad.write_bytes(neu.encode("utf-8"))
    if kaputt:
        print("Marker fehlen:", "; ".join(kaputt)); return 1
    b = badge(d)
    if not BADGE.exists() or BADGE.read_text(encoding="utf-8") != b:
        abweichend.append(BADGE.name)
        if befehl == "stempeln":
            BADGE.write_text(b, encoding="utf-8")
    if befehl == "stempeln":
        print("gestempelt:", ", ".join(abweichend) or "nichts geändert"); return 0
    if befehl == "pruefen":
        print("abweichend:", ", ".join(abweichend) if abweichend else "keine"); return 1 if abweichend else 0
    print(__doc__); return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
