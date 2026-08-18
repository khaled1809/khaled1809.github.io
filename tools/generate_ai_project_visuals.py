#!/usr/bin/env python3
"""Generate consistent visual documentation for the three AI/NLP case studies."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Iterable, Sequence

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "images" / "projects"
W, H = 1400, 850

BG = "#061321"
BG_ALT = "#0a1c2d"
SURFACE = "#102a43"
SURFACE_DARK = "#0b2137"
BORDER = "#315f85"
GRID = "#143049"
TEXT = "#f0f6ff"
MUTED = "#9eb2ca"
SUBTLE = "#718aa5"
TEAL = "#4fe2c9"
BLUE = "#61a2ff"
PURPLE = "#a47ef7"
YELLOW = "#f8c95b"
RED = "#ff7b84"
GREEN = "#71dfa0"
WHITE = "#ffffff"

FONT_REG = "/usr/share/fonts/opentype/inter/Inter-Regular.otf"
FONT_MED = "/usr/share/fonts/opentype/inter/Inter-Medium.otf"
FONT_SEMI = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
FONT_BOLD = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"


def font(size: int, weight: str = "regular", mono: bool = False) -> ImageFont.FreeTypeFont:
    if mono:
        return ImageFont.truetype(FONT_MONO, size)
    path = {
        "regular": FONT_REG,
        "medium": FONT_MED,
        "semibold": FONT_SEMI,
        "bold": FONT_BOLD,
    }[weight]
    return ImageFont.truetype(path, size)


F = {
    "title": font(44, "bold"),
    "subtitle": font(22),
    "h2": font(26, "semibold"),
    "h3": font(20, "semibold"),
    "body": font(17),
    "small": font(14),
    "tiny": font(12, "semibold"),
    "metric": font(34, "bold"),
    "mono": font(16, mono=True),
    "mono_small": font(13, mono=True),
}


def base_canvas() -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(image)
    for x in range(0, W + 1, 70):
        draw.line((x, 0, x, H), fill=GRID, width=1)
    for y in range(0, H + 1, 70):
        draw.line((0, y, W, y), fill=GRID, width=1)
    draw.rectangle((0, 0, W, H), fill="#07162680")
    # subtle top-right glow without an overlay on any image asset
    for r, alpha in [(410, 18), (330, 14), (250, 10)]:
        color = (21, 81, 91)
        draw.ellipse((W - r, -r // 2, W + r // 2, r), outline=color, width=max(1, alpha // 8))
    return image, draw


def text_size(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont) -> tuple[int, int]:
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0], box[3] - box[1]


def wrap_lines(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    words = text.split()
    if not words:
        return []
    lines: list[str] = []
    current = words[0]
    for word in words[1:]:
        trial = f"{current} {word}"
        if text_size(draw, trial, fnt)[0] <= max_width:
            current = trial
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines


def draw_wrapped(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    fnt: ImageFont.FreeTypeFont,
    fill: str,
    max_width: int,
    line_gap: int = 6,
    max_lines: int | None = None,
) -> int:
    x, y = xy
    lines = wrap_lines(draw, text, fnt, max_width)
    if max_lines is not None and len(lines) > max_lines:
        lines = lines[:max_lines]
        last = lines[-1]
        while text_size(draw, last + "…", fnt)[0] > max_width and last:
            last = last[:-1]
        lines[-1] = last.rstrip() + "…"
    line_h = text_size(draw, "Ag", fnt)[1]
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += line_h + line_gap
    return y


def panel(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], fill: str = SURFACE_DARK, outline: str = BORDER, radius: int = 24, width: int = 1) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def pill(draw: ImageDraw.ImageDraw, x: int, y: int, label: str, color: str = TEAL, *, fnt: ImageFont.FreeTypeFont | None = None) -> int:
    fnt = fnt or F["small"]
    tw, th = text_size(draw, label, fnt)
    w = tw + 30
    h = th + 18
    draw.rounded_rectangle((x, y, x + w, y + h), radius=h // 2, fill=SURFACE, outline=BORDER)
    draw.text((x + 15, y + 8), label, font=fnt, fill=color)
    return w


def arrow(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int], color: str = BORDER, width: int = 3) -> None:
    x1, y1 = start
    x2, y2 = end
    draw.line((x1, y1, x2, y2), fill=color, width=width)
    angle = math.atan2(y2 - y1, x2 - x1)
    size = 11
    p1 = (x2 - size * math.cos(angle - math.pi / 6), y2 - size * math.sin(angle - math.pi / 6))
    p2 = (x2 - size * math.cos(angle + math.pi / 6), y2 - size * math.sin(angle + math.pi / 6))
    draw.polygon([(x2, y2), p1, p2], fill=color)


def header(draw: ImageDraw.ImageDraw, title: str, subtitle: str, badge: str, accent: str = TEAL) -> None:
    draw.text((70, 52), title, font=F["title"], fill=TEXT)
    draw.text((70, 112), subtitle, font=F["subtitle"], fill=MUTED)
    bw, _ = text_size(draw, badge, F["small"])
    bx = W - bw - 120
    pill(draw, bx, 62, badge, accent)


def footer(draw: ImageDraw.ImageDraw, technologies: Sequence[tuple[str, str]]) -> None:
    x = 70
    for label, color in technologies:
        x += pill(draw, x, 740, label, color) + 14
    draw.ellipse((1286, 784, 1302, 800), fill=TEAL)
    draw.text((1316, 778), "KD", font=F["h3"], fill=TEXT)


def save(image: Image.Image, filename: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    image.save(OUT / filename, format="PNG", optimize=True)


def draw_step(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], index: str, title: str, body: str, accent: str) -> None:
    panel(draw, box)
    x1, y1, x2, y2 = box
    draw.rounded_rectangle((x1 + 18, y1 + 18, x1 + 58, y1 + 58), radius=12, fill=accent)
    draw.text((x1 + 31, y1 + 27), index, font=F["tiny"], fill=BG)
    draw.text((x1 + 76, y1 + 18), title, font=F["h3"], fill=TEXT)
    draw_wrapped(draw, (x1 + 24, y1 + 78), body, F["small"], MUTED, x2 - x1 - 48, line_gap=5, max_lines=4)


def csp_overview() -> None:
    image, draw = base_canvas()
    header(draw, "Moteur de déduction par contraintes", "CSP dynamique · AC-3 · scoring heuristique", "PROJET ALGORITHMIQUE", TEAL)

    panel(draw, (70, 180, 410, 660))
    draw.text((95, 205), "10 joueurs · 10 domaines", font=F["h2"], fill=TEXT)
    draw.text((95, 244), "Chaque nombre est unique dans [1, 100]", font=F["small"], fill=MUTED)
    positions = []
    for row in range(2):
        for col in range(5):
            x = 112 + col * 58
            y = 325 + row * 105
            positions.append((x, y))
    for idx, (x, y) in enumerate(positions):
        color = TEAL if idx == 0 else BLUE
        draw.ellipse((x - 23, y - 23, x + 23, y + 23), fill=SURFACE, outline=color, width=2)
        draw.text((x - 7, y - 10), chr(65 + idx), font=F["h3"], fill=TEXT)
        domain = "?" if idx == 0 else "1…100"
        dw, _ = text_size(draw, domain, F["tiny"])
        draw.text((x - dw // 2, y + 34), domain, font=F["tiny"], fill=MUTED)
    draw.text((96, 545), "Opérations observables", font=F["small"], fill=MUTED)
    x = 96
    for op, color in [("+", TEAL), ("× mod 10", BLUE), ("÷ entière", PURPLE), ("zéros", YELLOW)]:
        x += pill(draw, x, 575, op, color, fnt=F["tiny"]) + 8
        if x > 375:
            break

    steps = [
        ("01", "Générer", "Énumérer les questions possibles entre le joueur A et les autres.", BLUE),
        ("02", "Simuler", "Tester chaque réponse sur une copie de la base de connaissances.", PURPLE),
        ("03", "Propager", "Réduire les domaines avec AC-3 puis appliquer la contrainte all-different.", TEAL),
        ("04", "Classer", "Combiner gain personnel, utilité collective et risque de révélation.", YELLOW),
    ]
    y = 180
    for i, (num, title, body, color) in enumerate(steps):
        draw_step(draw, (470, y, 875, y + 100), num, title, body, color)
        if i < len(steps) - 1:
            arrow(draw, (672, y + 100), (672, y + 118), color=BORDER, width=2)
        y += 120

    panel(draw, (935, 180, 1330, 660), fill="#0d2840", outline=TEAL, width=2)
    draw.text((965, 210), "Question recommandée", font=F["h2"], fill=TEXT)
    draw.text((965, 270), "A  +  B", font=font(48, "bold"), fill=TEAL)
    draw.line((965, 340, 1295, 340), fill=BORDER, width=1)
    draw.text((965, 370), "Score", font=F["small"], fill=MUTED)
    draw.text((965, 404), "3·gainₐ + 0,8·gainₜ - 4·risque", font=F["h3"], fill=TEXT)
    components = [
        ("Réduction de mon domaine", "+", TEAL),
        ("Information collective", "+", BLUE),
        ("Révélation à l’adversaire", "−", RED),
    ]
    y = 470
    for label, sign, color in components:
        draw.ellipse((966, y + 4, 978, y + 16), fill=color)
        draw.text((990, y), label, font=F["small"], fill=MUTED)
        draw.text((1270, y), sign, font=F["h3"], fill=color)
        y += 45

    footer(draw, [("Python", TEAL), ("CSP", BLUE), ("AC-3", PURPLE), ("Backtracking", YELLOW), ("MRV", TEAL)])
    save(image, "csp-overview.png")


def csp_propagation() -> None:
    image, draw = base_canvas()
    header(draw, "Propagation des contraintes", "Réduire les domaines sans perdre de solution cohérente", "AC-3 + ALL-DIFFERENT", BLUE)

    panel(draw, (70, 180, 600, 665))
    draw.text((100, 208), "Avant la réponse", font=F["h2"], fill=TEXT)
    rows = [
        ("A", 100, TEAL), ("B", 100, BLUE), ("C", 100, PURPLE), ("D", 100, YELLOW)
    ]
    y = 285
    for name, size, color in rows:
        draw.text((100, y), name, font=F["h3"], fill=TEXT)
        draw.rounded_rectangle((145, y + 2, 500, y + 26), radius=12, fill="#0b1f33")
        draw.rounded_rectangle((145, y + 2, 500, y + 26), radius=12, fill=color)
        draw.text((520, y), f"{size} valeurs", font=F["small"], fill=MUTED)
        y += 78
    draw.text((100, 600), "Domaines initiaux Dᵢ = {1, …, 100}", font=F["small"], fill=MUTED)

    arrow(draw, (620, 410), (755, 410), color=TEAL, width=4)
    panel(draw, (628, 322, 748, 500), fill=SURFACE, outline=TEAL, width=2)
    draw.text((651, 350), "A + B", font=F["h3"], fill=TEXT)
    draw.text((652, 392), "= 27", font=F["metric"], fill=TEAL)
    draw.text((650, 448), "nouvelle\ncontrainte", font=F["tiny"], fill=MUTED)

    panel(draw, (780, 180, 1330, 665), fill="#0d2840")
    draw.text((810, 208), "Après propagation", font=F["h2"], fill=TEXT)
    after = [
        ("A", 24, TEAL), ("B", 24, BLUE), ("C", 76, PURPLE), ("D", 76, YELLOW)
    ]
    y = 285
    for name, size, color in after:
        draw.text((810, y), name, font=F["h3"], fill=TEXT)
        draw.rounded_rectangle((855, y + 2, 1210, y + 26), radius=12, fill="#0b1f33")
        width = int(355 * size / 100)
        draw.rounded_rectangle((855, y + 2, 855 + max(18, width), y + 26), radius=12, fill=color)
        draw.text((1230, y), f"{size}", font=F["small"], fill=MUTED)
        y += 78
    draw.text((810, 580), "1. REVISE supprime les valeurs sans support", font=F["small"], fill=MUTED)
    draw.text((810, 612), "2. Les arcs voisins sont remis dans la file", font=F["small"], fill=MUTED)
    draw.text((810, 644), "3. Une valeur singleton est retirée des autres domaines", font=F["small"], fill=MUTED)

    footer(draw, [("Copie de la KB", BLUE), ("File d’arcs", PURPLE), ("Support binaire", TEAL), ("Unicité", YELLOW)])
    save(image, "csp-propagation.png")


def csp_scoring() -> None:
    image, draw = base_canvas()
    header(draw, "Sélection de la meilleure question", "Évaluer l’information obtenue avant de modifier l’état réel", "HEURISTIQUE MULTI-CRITÈRES", YELLOW)

    cards = [
        (70, "Gain personnel", "Réduction attendue du domaine du joueur A après simulation de chaque réponse.", "× 3,0", TEAL),
        (480, "Utilité collective", "Somme des réductions attendues sur les dix domaines, après propagation globale.", "× 0,8", BLUE),
        (890, "Risque de révélation", "Probabilité que le domaine du partenaire devienne singleton et révèle le nombre de A.", "× −4,0", RED),
    ]
    for x, title, body, weight, color in cards:
        panel(draw, (x, 190, x + 370, 430), fill=SURFACE_DARK, outline=color, width=2)
        draw.text((x + 28, 220), title, font=F["h2"], fill=TEXT)
        draw_wrapped(draw, (x + 28, 270), body, F["body"], MUTED, 314, line_gap=7, max_lines=5)
        draw.text((x + 28, 370), weight, font=F["metric"], fill=color)

    panel(draw, (70, 460, 1330, 700), fill="#0d2840")
    draw.text((100, 487), "Classement simulé", font=F["h2"], fill=TEXT)
    columns = [(100, "Question"), (470, "Gain A"), (650, "Gain total"), (860, "Risque"), (1060, "Score")]
    for x, label in columns:
        draw.text((x, 535), label, font=F["tiny"], fill=SUBTLE)
    rows = [
        ("A + B", "18,4", "31,2", "0,04", "78,4", TEAL),
        ("A × F", "16,1", "29,5", "0,07", "68,9", BLUE),
        ("A ÷ C", "13,8", "25,1", "0,02", "60,7", PURPLE),
    ]
    y = 570
    for question, ga, gt, risk, score, color in rows:
        draw.line((100, y - 10, 1300, y - 10), fill=BORDER, width=1)
        draw.text((100, y), question, font=F["h3"], fill=color)
        draw.text((470, y), ga, font=F["body"], fill=TEXT)
        draw.text((650, y), gt, font=F["body"], fill=TEXT)
        draw.text((860, y), risk, font=F["body"], fill=RED if float(risk.replace(',', '.')) > 0.05 else GREEN)
        draw.text((1060, y), score, font=F["h3"], fill=TEXT)
        y += 40
    draw.text((1180, 487), "illustration", font=F["tiny"], fill=SUBTLE)

    footer(draw, [("Simulation", TEAL), ("Espérance", BLUE), ("Entropie", PURPLE), ("Compromis", YELLOW)])
    save(image, "csp-scoring.png")


def csp_console() -> None:
    image, draw = base_canvas()
    header(draw, "Interface console du moteur", "Explorer les domaines, tester une question et appliquer une réponse", "CLI PYTHON", TEAL)
    panel(draw, (70, 180, 1330, 685), fill="#07101b", outline=BORDER, radius=20)
    draw.rectangle((70, 180, 1330, 230), fill="#102338")
    for i, color in enumerate((RED, YELLOW, GREEN)):
        draw.ellipse((96 + i * 28, 198, 110 + i * 28, 212), fill=color)
    draw.text((590, 194), "python3 main.py", font=F["small"], fill=MUTED)
    lines = [
        ("Bienvenue dans le jeu. Tapez help pour voir les commandes", MUTED),
        ("", TEXT),
        ("Commande  > domaine", TEAL),
        ("A: [1, 2, 3, ...] (__size=100)", TEXT),
        ("B: [1, 2, 3, ...] (__size=100)", TEXT),
        ("", TEXT),
        ("Commande  > test + B", TEAL),
        ("Tester + avec B → gain attendu, utilité collective et niveau de risque", TEXT),
        ("", TEXT),
        ("Commande  > ask", TEAL),
        ("Les meilleures questions à poser sont classées par score.", TEXT),
        ("1. A collabore + avec B", GREEN),
        ("2. A collabore × avec F", BLUE),
        ("", TEXT),
        ("Commande  > askmanual + B 27", TEAL),
        ("Contrainte ajoutée → AC-3 relancé → domaines mis à jour", YELLOW),
    ]
    y = 258
    for line, color in lines:
        draw.text((105, y), line, font=F["mono"], fill=color)
        y += 25
    panel(draw, (980, 260, 1285, 610), fill="#0d2135", outline=TEAL)
    draw.text((1008, 286), "Commandes", font=F["h3"], fill=TEXT)
    commands = [
        ("ask", "recommander"),
        ("test OP CIBLE", "simuler"),
        ("domaine", "inspecter"),
        ("askmanual", "ajouter"),
        ("prune", "diagnostiquer"),
        ("exit", "quitter"),
    ]
    y = 338
    for cmd, desc in commands:
        draw.text((1008, y), cmd, font=F["mono_small"], fill=TEAL)
        draw.text((1165, y), desc, font=F["small"], fill=MUTED)
        y += 43

    footer(draw, [("État persistant", TEAL), ("Commandes explicites", BLUE), ("Diagnostic", PURPLE)])
    save(image, "csp-console.png")


def csp_search() -> None:
    image, draw = base_canvas()
    header(draw, "Recherche arborescente ciblée", "Utiliser MRV et le backtracking seulement lorsque la propagation ne suffit plus", "MRV + BACKTRACKING", PURPLE)

    panel(draw, (70, 180, 500, 675))
    draw.text((100, 210), "Pourquoi ne pas tout explorer ?", font=F["h2"], fill=TEXT)
    draw.text((100, 282), "100¹⁰", font=font(64, "bold"), fill=RED)
    draw.text((100, 355), "configurations dans le pire cas", font=F["body"], fill=MUTED)
    draw_wrapped(draw, (100, 420), "AC-3 et les inférences réduisent d’abord les domaines. Le backtracking n’intervient que sur l’espace résiduel.", F["body"], MUTED, 340, line_gap=8)
    pill(draw, 100, 565, "limite de solutions", YELLOW)
    pill(draw, 100, 615, "copie isolée de la KB", TEAL)

    panel(draw, (560, 180, 1330, 675), fill="#0d2840")
    draw.text((590, 210), "Arbre de recherche simplifié", font=F["h2"], fill=TEXT)
    nodes = {
        "root": (930, 280, "MRV : C\n|Dᶜ| = 3", TEAL),
        "a": (700, 420, "C = 14", BLUE),
        "b": (930, 420, "C = 27", PURPLE),
        "c": (1160, 420, "C = 51", YELLOW),
        "a1": (650, 565, "contradiction", RED),
        "b1": (900, 565, "solution", GREEN),
        "c1": (1160, 565, "domaine vide", RED),
    }
    for parent, child in [("root", "a"), ("root", "b"), ("root", "c"), ("a", "a1"), ("b", "b1"), ("c", "c1")]:
        px, py, _, _ = nodes[parent]
        cx, cy, _, _ = nodes[child]
        arrow(draw, (px, py + 38), (cx, cy - 38), color=BORDER, width=2)
    for key, (x, y, label, color) in nodes.items():
        w, h = (180, 78) if key == "root" else (170, 66)
        panel(draw, (x - w // 2, y - h // 2, x + w // 2, y + h // 2), fill=SURFACE_DARK, outline=color, radius=18, width=2)
        lines = label.split("\n")
        ty = y - (len(lines) * 12)
        for line in lines:
            tw, _ = text_size(draw, line, F["small"])
            draw.text((x - tw // 2, ty), line, font=F["small"], fill=TEXT if color != RED else color)
            ty += 25
    draw.text((590, 630), "MRV choisit le domaine non résolu le plus petit.", font=F["small"], fill=MUTED)

    footer(draw, [("MRV", PURPLE), ("Pruning", RED), ("Solutions cohérentes", GREEN), ("Limite 10 000", YELLOW)])
    save(image, "csp-search.png")


def oulipo_overview() -> None:
    image, draw = base_canvas()
    header(draw, "Réécriture créative sous contraintes OULIPO", "Transformer un texte tout en contrôlant sa dérive sémantique", "PROJET NLP", PURPLE)

    panel(draw, (70, 185, 425, 660), fill="#0d2840")
    draw.text((100, 215), "Texte source", font=F["h2"], fill=TEXT)
    draw_wrapped(draw, (100, 300), "« Le chat dort sur le canapé à Paris. »", font(30, "semibold"), TEXT, 290, line_gap=10)
    draw.text((100, 500), "Éléments protégés", font=F["small"], fill=MUTED)
    pill(draw, 100, 540, "Paris · entité LOC", BLUE)
    pill(draw, 100, 590, "déterminants", SUBTLE)

    steps = [
        ("01", "Analyser", "Tokens, lemmes, POS, dépendances et entités nommées.", BLUE),
        ("02", "Sélectionner", "Conserver les NOUN / VERB / ADJ modifiables.", TEAL),
        ("03", "Enrichir", "WordNet fournit synonymes, hyperonymes et co-hyponymes.", PURPLE),
        ("04", "Classer", "Les embeddings ordonnent les candidats par proximité.", YELLOW),
    ]
    y = 185
    for i, step in enumerate(steps):
        draw_step(draw, (480, y, 880, y + 100), *step)
        if i < len(steps) - 1:
            arrow(draw, (680, y + 100), (680, y + 118), color=BORDER, width=2)
        y += 120

    panel(draw, (935, 185, 1330, 660), fill="#10243a", outline=TEAL, width=2)
    draw.text((965, 215), "Texte réécrit", font=F["h2"], fill=TEXT)
    draw.text((965, 275), "Contrainte", font=F["small"], fill=MUTED)
    pill(draw, 965, 310, "hyperonymisation", TEAL)
    draw_wrapped(draw, (965, 390), "« L’animal dort sur le siège à Paris. »", font(30, "semibold"), TEXT, 320, line_gap=10)
    draw.text((965, 565), "Post-traitement", font=F["small"], fill=MUTED)
    draw.text((965, 600), "espaces · ponctuation · élision", font=F["body"], fill=TEAL)

    footer(draw, [("Python", TEAL), ("spaCy", BLUE), ("WordNet", PURPLE), ("Embeddings", YELLOW), ("Tkinter", TEAL)])
    save(image, "oulipo-overview.png")


def oulipo_analysis() -> None:
    image, draw = base_canvas()
    header(draw, "Analyse linguistique avec spaCy", "Préserver la structure utile avant toute transformation", "TOKENISATION + POS + DEP", BLUE)
    panel(draw, (70, 180, 1330, 675), fill="#0b2137")
    headers = [
        (100, "Mot"), (270, "Lemme"), (440, "POS"), (570, "Dépendance"), (770, "Tête"), (940, "Entité"), (1090, "Modifiable")
    ]
    for x, label in headers:
        draw.text((x, 220), label, font=F["tiny"], fill=SUBTLE)
    draw.line((95, 255, 1300, 255), fill=BORDER, width=1)
    rows = [
        ("Le", "le", "DET", "det", "chat", "—", "non"),
        ("chat", "chat", "NOUN", "nsubj", "dort", "—", "oui"),
        ("dort", "dormir", "VERB", "ROOT", "dort", "—", "oui"),
        ("sur", "sur", "ADP", "case", "canapé", "—", "non"),
        ("le", "le", "DET", "det", "canapé", "—", "non"),
        ("canapé", "canapé", "NOUN", "obl:arg", "dort", "—", "oui"),
        ("à", "à", "ADP", "case", "Paris", "—", "non"),
        ("Paris", "Paris", "PROPN", "nmod", "dort", "LOC", "protégé"),
    ]
    y = 280
    for idx, row in enumerate(rows):
        if idx % 2:
            draw.rounded_rectangle((90, y - 10, 1310, y + 30), radius=8, fill="#0f2a43")
        values = [(100, row[0]), (270, row[1]), (440, row[2]), (570, row[3]), (770, row[4]), (940, row[5]), (1090, row[6])]
        for x, value in values:
            color = TEAL if value == "oui" else BLUE if value == "protégé" else TEXT
            draw.text((x, y), value, font=F["body"], fill=color)
        y += 48
    draw.text((100, 635), "Règle de sélection : NOUN / VERB / ADJ · hors stop words · hors entités · hors noms propres", font=F["small"], fill=MUTED)
    footer(draw, [("fr_core_news_md", BLUE), ("lemmatisation", TEAL), ("dépendances", PURPLE), ("entités nommées", YELLOW)])
    save(image, "oulipo-analysis.png")


def oulipo_constraints() -> None:
    image, draw = base_canvas()
    header(draw, "Bibliothèque de contraintes", "Une même analyse linguistique alimente plusieurs stratégies de réécriture", "9 TRANSFORMATIONS", TEAL)
    cards = [
        ("Hyperonyme", "chat → animal", TEAL),
        ("Antonyme", "clair → sombre", RED),
        ("Voisin sémantique", "chat → chien", BLUE),
        ("Lipogramme", "exclure la lettre e", YELLOW),
        ("Même initiale", "candidat commençant pareil", PURPLE),
        ("Inversion syntaxique", "sujet ↔ objet", TEAL),
        ("Érosion", "synonyme proche et court", BLUE),
        ("Définition", "ajouter un hyperonyme", PURPLE),
        ("Dérive", "plage de similarité", YELLOW),
    ]
    for idx, (title, example, color) in enumerate(cards):
        col = idx % 3
        row = idx // 3
        x = 70 + col * 420
        y = 185 + row * 165
        panel(draw, (x, y, x + 380, y + 135), fill=SURFACE_DARK, outline=color, width=2)
        draw.ellipse((x + 24, y + 25, x + 42, y + 43), fill=color)
        draw.text((x + 60, y + 18), title, font=F["h3"], fill=TEXT)
        draw_wrapped(draw, (x + 24, y + 72), example, F["body"], MUTED, 330, line_gap=5, max_lines=2)
    footer(draw, [("WordNet FR", PURPLE), ("similarité", BLUE), ("fallback", YELLOW), ("règles composables", TEAL)])
    save(image, "oulipo-constraints.png")


def oulipo_drift() -> None:
    image, draw = base_canvas()
    header(draw, "Dérive sémantique contrôlée", "Réanalyser le texte à chaque itération pour maîtriser la distance", "EXPÉRIMENTATION ITÉRATIVE", PURPLE)
    steps = [
        ("Texte initial", "Le chat observe la ville.", "—", TEAL),
        ("Itération 1", "Le félin examine la cité.", "sim. 0,80–0,95", BLUE),
        ("Itération 2", "L’animal étudie la métropole.", "sim. 0,60–0,80", PURPLE),
        ("Itération 3", "L’organisme explore l’espace urbain.", "sim. 0,40–0,60", YELLOW),
    ]
    x_positions = [70, 390, 710, 1030]
    for idx, (label, sentence, sim, color) in enumerate(steps):
        x = x_positions[idx]
        panel(draw, (x, 225, x + 285, 575), fill=SURFACE_DARK, outline=color, width=2)
        draw.text((x + 25, 255), label, font=F["h3"], fill=color)
        draw_wrapped(draw, (x + 25, 325), f"« {sentence} »", font(24, "semibold"), TEXT, 235, line_gap=10, max_lines=5)
        if sim != "—":
            pill(draw, x + 25, 495, sim, color, fnt=F["tiny"])
        if idx < len(steps) - 1:
            arrow(draw, (x + 285, 400), (x + 310, 400), color=BORDER, width=3)
    draw.text((70, 620), "À chaque étape : analyse spaCy → nouveaux candidats → classement vectoriel → réécriture", font=F["body"], fill=MUTED)
    draw.text((1080, 620), "exemple conceptuel", font=F["tiny"], fill=SUBTLE)
    footer(draw, [("réanalyse", TEAL), ("plage min/max", BLUE), ("OOV fallback", PURPLE), ("cohérence", YELLOW)])
    save(image, "oulipo-drift.png")


def oulipo_interface() -> None:
    image, draw = base_canvas()
    header(draw, "Interface de démonstration Tkinter", "Reconstitution fidèle de la structure implémentée dans mainVisuel.py", "APPLICATION DESKTOP", BLUE)
    panel(draw, (70, 175, 1330, 690), fill="#edf2f7", outline="#60758b", radius=12)
    draw.rectangle((70, 175, 1330, 225), fill="#d9e2ec")
    draw.text((95, 190), "Projet TAL — Réécriture OULIPO", font=F["h3"], fill="#1b2a3a")

    # Input area
    draw.rounded_rectangle((95, 245, 1305, 330), radius=10, fill="#f8fafc", outline="#9aabba")
    draw.text((115, 258), "Entrée", font=F["small"], fill="#34495e")
    draw.rounded_rectangle((115, 285, 1080, 315), radius=6, fill=WHITE, outline="#aab7c4")
    draw.text((128, 290), "Le chat mange la souris.", font=F["small"], fill="#263645")
    draw.rounded_rectangle((1100, 282, 1275, 318), radius=7, fill="#315f85")
    draw.text((1145, 291), "1. Analyser", font=F["small"], fill=WHITE)

    # Table area
    draw.rounded_rectangle((95, 350, 1305, 500), radius=10, fill="#f8fafc", outline="#9aabba")
    draw.text((115, 364), "Analyse (spaCy)", font=F["small"], fill="#34495e")
    columns = ["Word", "Lemma", "POS", "Dep", "Head", "Entity", "Stop", "Modifiable"]
    x = 115
    for col in columns:
        draw.text((x, 395), col, font=F["tiny"], fill="#506478")
        x += 145
    draw.line((115, 420, 1280, 420), fill="#b8c5d1")
    rows = [
        ["Le", "le", "DET", "det", "chat", "None", "True", "False"],
        ["chat", "chat", "NOUN", "nsubj", "mange", "None", "False", "True"],
        ["mange", "manger", "VERB", "ROOT", "mange", "None", "False", "True"],
    ]
    y = 432
    for row in rows:
        x = 115
        for value in row:
            draw.text((x, y), value, font=font(11), fill="#263645")
            x += 145
        y += 21

    # Controls and logs
    draw.rounded_rectangle((95, 520, 450, 665), radius=10, fill="#f8fafc", outline="#9aabba")
    draw.text((115, 535), "Méthodes", font=F["small"], fill="#34495e")
    buttons = ["Hyperonymisation", "Lipogramme", "Inversion syntaxique", "Dérive sémantique"]
    y = 565
    for label in buttons:
        draw.rounded_rectangle((115, y, 420, y + 24), radius=5, fill="#e4ebf2", outline="#b4c1cc")
        draw.text((128, y + 4), label, font=font(11), fill="#263645")
        y += 28
    draw.rounded_rectangle((470, 520, 1305, 665), radius=10, fill="#101820", outline="#9aabba")
    draw.text((490, 535), "Résultats", font=F["small"], fill="#d8e4ee")
    logs = [
        "Analyse terminée. 6 tokens trouvés.",
        "Modifiables : ['chat', 'mange', 'souris']",
        "> Application contrainte : Hyperonymisation",
        "RÉSULTAT : « L'animal consomme le mammifère. »",
    ]
    y = 565
    for line in logs:
        draw.text((490, y), line, font=F["mono_small"], fill=TEAL if line.startswith("RÉSULTAT") else "#d8e4ee")
        y += 23

    footer(draw, [("Treeview", BLUE), ("deepcopy", PURPLE), ("logs", TEAL), ("actions", YELLOW)])
    save(image, "oulipo-interface.png")


def dna_overview() -> None:
    image, draw = base_canvas()
    header(draw, "Semantic DNA — provenance documentaire", "Comparer, regrouper et classer des documents selon plusieurs dimensions", "NLP + MACHINE LEARNING", TEAL)
    steps = [
        ("01", "Prétraitement NLP", "Entités, relations, thèmes, intentions, polarité et embedding de contexte.", BLUE),
        ("02", "Semantic DNA", "Concaténation de sous-vecteurs interprétables et d’un embedding SBERT.", TEAL),
        ("03", "Similarité", "Cinq scores séparés puis combinaison manuelle ou régression logistique.", PURPLE),
        ("04", "Clustering", "Regroupement hiérarchique avec un seuil appris sur les données.", YELLOW),
        ("05", "Provenance", "Ranker LightGBM pour placer la source probable en première position.", GREEN),
        ("06", "Mutations", "Différences d’entités, contexte, thème, sentiment et structure.", RED),
    ]
    for idx, step in enumerate(steps):
        col = idx % 3
        row = idx // 3
        x = 70 + col * 420
        y = 185 + row * 220
        draw_step(draw, (x, y, x + 380, y + 175), *step)
        if col < 2:
            arrow(draw, (x + 380, y + 88), (x + 410, y + 88), color=BORDER, width=2)
    arrow(draw, (1200, 360), (1200, 392), color=BORDER, width=2)
    draw.text((70, 650), "Objectif : identifier une source probable et expliquer comment un document a été transformé.", font=F["body"], fill=MUTED)
    footer(draw, [("spaCy", BLUE), ("Sentence-BERT", TEAL), ("scikit-learn", PURPLE), ("LightGBM", YELLOW), ("Streamlit", GREEN)])
    save(image, "semantic-dna-overview.png")


def dna_vector() -> None:
    image, draw = base_canvas()
    header(draw, "Construction du Semantic DNA", "Un vecteur composite qui sépare contenu, structure et contexte", "REPRÉSENTATION MULTI-DIMENSIONS", BLUE)
    dimensions = [
        ("Entités", "v_ent", "types + valeurs nommées", TEAL, 0.30),
        ("Relations", "v_rel", "dépendances syntaxiques", BLUE, 0.15),
        ("Thèmes", "v_theme", "scores zero-shot", PURPLE, 0.15),
        ("Intentions", "v_int", "news · opinion · fact…", YELLOW, 0.0),
        ("Polarité", "v_pol", "score −1 à +1", RED, 0.10),
        ("Contexte", "v_context", "Sentence-BERT · 384 dimensions", GREEN, 0.30),
    ]
    x = 70
    for idx, (name, symbol, desc, color, weight) in enumerate(dimensions):
        width = 180 if idx < 5 else 240
        panel(draw, (x, 215, x + width, 535), fill=SURFACE_DARK, outline=color, width=2)
        draw.text((x + 20, 245), name, font=F["h3"], fill=TEXT)
        draw.text((x + 20, 300), symbol, font=F["mono"], fill=color)
        draw_wrapped(draw, (x + 20, 350), desc, F["small"], MUTED, width - 40, line_gap=6, max_lines=4)
        if weight > 0:
            draw.text((x + 20, 465), f"poids {weight:.2f}", font=F["small"], fill=color)
        if idx < len(dimensions) - 1:
            draw.text((x + width + 2, 357), "+", font=F["metric"], fill=SUBTLE)
        x += width + 20
    panel(draw, (250, 580, 1150, 675), fill="#0d2840", outline=TEAL, width=2)
    draw.text((290, 608), "DNA(d) = [ v_ent | v_rel | v_theme | v_int | v_pol | v_context ]", font=font(27, "semibold"), fill=TEXT)
    draw.text((1000, 638), "concaténation", font=F["tiny"], fill=TEAL)
    footer(draw, [("Jaccard", TEAL), ("cosine", BLUE), ("scores séparés", PURPLE), ("interprétabilité", YELLOW)])
    save(image, "semantic-dna-vector.png")


def dna_learning() -> None:
    image, draw = base_canvas()
    header(draw, "Apprentissage supervisé de la similarité", "Remplacer des poids manuels par une régression logistique entraînée", "TEST CONTRÔLÉ", PURPLE)

    panel(draw, (70, 185, 675, 675), fill=SURFACE_DARK)
    draw.text((100, 215), "Matrice de confusion", font=F["h2"], fill=TEXT)
    draw.text((100, 252), "200 paires de test", font=F["small"], fill=MUTED)
    mx, my, cell = 205, 330, 130
    labels = [("103", TEAL), ("0", SURFACE), ("0", SURFACE), ("97", BLUE)]
    for idx, (value, color) in enumerate(labels):
        row, col = divmod(idx, 2)
        fill = color if value != "0" else "#142a3e"
        draw.rectangle((mx + col * cell, my + row * cell, mx + (col + 1) * cell, my + (row + 1) * cell), fill=fill, outline=BORDER, width=2)
        tw, th = text_size(draw, value, F["metric"])
        draw.text((mx + col * cell + (cell - tw) // 2, my + row * cell + (cell - th) // 2 - 4), value, font=F["metric"], fill=BG if value != "0" else MUTED)
    draw.text((190, 610), "Original", font=F["small"], fill=MUTED)
    draw.text((337, 610), "Copie", font=F["small"], fill=MUTED)
    draw.text((95, 372), "Original", font=F["small"], fill=MUTED)
    draw.text((110, 502), "Copie", font=F["small"], fill=MUTED)

    panel(draw, (725, 185, 1330, 675), fill="#0d2840")
    draw.text((755, 215), "Coefficients appris", font=F["h2"], fill=TEXT)
    draw.text((755, 252), "Importance relative dans le modèle", font=F["small"], fill=MUTED)
    bars = [
        ("Embeddings", 0.88, BLUE),
        ("Entités", 0.22, TEAL),
        ("Thèmes", 0.16, PURPLE),
        ("Relations", 0.04, YELLOW),
        ("Polarité", -0.08, RED),
    ]
    y = 315
    zero_x = 920
    draw.line((zero_x, 295, zero_x, 610), fill=BORDER, width=1)
    for label, value, color in bars:
        draw.text((755, y), label, font=F["small"], fill=TEXT)
        if value >= 0:
            x2 = zero_x + int(value * 330)
            draw.rounded_rectangle((zero_x, y + 2, x2, y + 22), radius=10, fill=color)
        else:
            x1 = zero_x + int(value * 330)
            draw.rounded_rectangle((x1, y + 2, zero_x, y + 22), radius=10, fill=color)
        draw.text((1260, y), f"{value:+.2f}", font=F["tiny"], fill=color)
        y += 58
    draw.text((755, 620), "Résultat à interpréter dans le cadre du jeu de données fourni.", font=F["tiny"], fill=SUBTLE)
    footer(draw, [("LogisticRegression", PURPLE), ("features", TEAL), ("matrice", BLUE), ("validation", YELLOW)])
    save(image, "semantic-dna-learning.png")


def dna_clustering() -> None:
    image, draw = base_canvas()
    header(draw, "Apprentissage du seuil de clustering", "Transformer les similarités en groupes cohérents sans fixer le nombre de clusters", "AGGLOMERATIVE CLUSTERING", YELLOW)
    panel(draw, (70, 185, 955, 675), fill=SURFACE_DARK)
    draw.text((100, 215), "Recherche du meilleur seuil", font=F["h2"], fill=TEXT)
    chart = (130, 300, 900, 610)
    x1, y1, x2, y2 = chart
    draw.line((x1, y2, x2, y2), fill=MUTED, width=2)
    draw.line((x1, y1, x1, y2), fill=MUTED, width=2)
    for i in range(5):
        yy = y2 - i * (y2 - y1) / 4
        draw.line((x1, yy, x2, yy), fill=GRID, width=1)
        draw.text((90, int(yy) - 8), f"{i/4:.2f}", font=F["tiny"], fill=SUBTLE)
    points = []
    for i in range(35):
        threshold = 0.05 + i * 0.025
        ari = max(0, 1 - ((threshold - 0.26) / 0.22) ** 2)
        ari = min(1, max(0, ari))
        px = x1 + int((threshold - 0.05) / 0.85 * (x2 - x1))
        py = y2 - int(ari * (y2 - y1))
        points.append((px, py))
    draw.line(points, fill=BLUE, width=4)
    for px, py in points[::3]:
        draw.ellipse((px - 4, py - 4, px + 4, py + 4), fill=TEAL)
    best_x = x1 + int((0.26 - 0.05) / 0.85 * (x2 - x1))
    draw.line((best_x, y1, best_x, y2), fill=YELLOW, width=3)
    draw.ellipse((best_x - 8, y1 - 8, best_x + 8, y1 + 8), fill=YELLOW)
    draw.text((best_x + 15, y1 + 5), "seuil ≈ 0,26", font=F["small"], fill=YELLOW)
    draw.text((x1, 625), "0,05", font=F["tiny"], fill=SUBTLE)
    draw.text((x2 - 30, 625), "0,90", font=F["tiny"], fill=SUBTLE)

    panel(draw, (1000, 185, 1330, 675), fill="#0d2840", outline=YELLOW, width=2)
    draw.text((1030, 220), "Point retenu", font=F["h2"], fill=TEXT)
    draw.text((1030, 300), "0,26", font=font(64, "bold"), fill=YELLOW)
    draw.text((1030, 390), "ARI", font=F["small"], fill=MUTED)
    draw.text((1030, 425), "1,000", font=F["metric"], fill=TEAL)
    draw.text((1030, 500), "Clusters prédits", font=F["small"], fill=MUTED)
    draw.text((1030, 535), "100", font=F["metric"], fill=BLUE)
    draw_wrapped(draw, (1030, 595), "Résultat obtenu sur le jeu d’entraînement contrôlé.", F["tiny"], SUBTLE, 255, line_gap=4)
    footer(draw, [("distance = 1 − sim", BLUE), ("ARI", TEAL), ("seuil appris", YELLOW), ("pas de k fixé", PURPLE)])
    save(image, "semantic-dna-clustering.png")


def dna_ranking() -> None:
    image, draw = base_canvas()
    header(draw, "Ranking de provenance", "Classer la source probable avant ses dérivés dans chaque cluster", "LIGHTGBM RANKER", GREEN)
    panel(draw, (70, 185, 940, 675), fill=SURFACE_DARK)
    draw.text((100, 215), "Importance des caractéristiques", font=F["h2"], fill=TEXT)
    features = [
        ("relation_count", 510, TEAL),
        ("avg_sentence_length", 170, BLUE),
        ("centrality", 150, PURPLE),
        ("structure", 125, YELLOW),
        ("coverage", 100, GREEN),
        ("entity_density", 20, RED),
        ("unique_entities", 8, SUBTLE),
    ]
    y = 285
    max_val = max(v for _, v, _ in features)
    for label, value, color in features:
        draw.text((100, y), label, font=F["small"], fill=TEXT)
        width = int(560 * value / max_val)
        draw.rounded_rectangle((300, y + 2, 300 + max(8, width), y + 24), radius=11, fill=color)
        draw.text((880, y), str(value), font=F["tiny"], fill=color)
        y += 50

    panel(draw, (990, 185, 1330, 675), fill="#0d2840", outline=GREEN, width=2)
    draw.text((1020, 220), "Évaluation Top-1", font=F["h2"], fill=TEXT)
    draw.text((1020, 300), "98 / 100", font=font(54, "bold"), fill=GREEN)
    draw.text((1020, 370), "clusters correctement classés", font=F["small"], fill=MUTED)
    cx, cy = 1160, 510
    draw.ellipse((1075, 425, 1245, 595), fill="#122b40", outline=BORDER, width=18)
    draw.arc((1075, 425, 1245, 595), start=-90, end=-90 + 352.8, fill=GREEN, width=18)
    draw.text((1123, 486), "98%", font=F["metric"], fill=TEXT)
    draw_wrapped(draw, (1020, 610), "Résultat sur le jeu de test provenance fourni ; généralisation à confirmer.", F["tiny"], SUBTLE, 270, line_gap=4)
    footer(draw, [("coverage", TEAL), ("centrality", BLUE), ("structure", PURPLE), ("Top-1", GREEN)])
    save(image, "semantic-dna-ranking.png")


def dna_mutations() -> None:
    image, draw = base_canvas()
    header(draw, "Analyse des mutations et de la réutilisation", "Expliquer ce qui change entre une source et un document dérivé", "ANALYSE INTERPRÉTABLE", RED)

    panel(draw, (70, 185, 700, 675), fill=SURFACE_DARK)
    draw.text((100, 215), "Mutation = 1 − similarité", font=F["h2"], fill=TEXT)
    dims = [
        ("Entités", 0.18, TEAL),
        ("Contexte", 0.27, BLUE),
        ("Thème", 0.08, PURPLE),
        ("Sentiment", 0.55, RED),
        ("Style", 0.31, YELLOW),
    ]
    y = 300
    for label, value, color in dims:
        draw.text((100, y), label, font=F["body"], fill=TEXT)
        draw.rounded_rectangle((235, y + 3, 610, y + 27), radius=12, fill="#0a1b2c")
        draw.rounded_rectangle((235, y + 3, 235 + int(375 * value), y + 27), radius=12, fill=color)
        draw.text((625, y), f"{value:.2f}", font=F["small"], fill=color)
        y += 62
    draw.text((100, 620), "Conclusion : orientation du discours modifiée", font=F["small"], fill=RED)

    panel(draw, (750, 185, 1330, 675), fill="#0d2840")
    draw.text((780, 215), "Type de réutilisation", font=F["h2"], fill=TEXT)
    types = [
        ("COPY", "similarité très forte", TEAL),
        ("PARAPHRASE", "sens conservé", BLUE),
        ("OPINION_REWRITE", "polarité modifiée", RED),
        ("SUMMARY", "perte d’entités", YELLOW),
        ("DERIVATIVE", "lien partiel", PURPLE),
        ("UNRELATED", "similarité faible", SUBTLE),
    ]
    y = 290
    for label, rule, color in types:
        pill(draw, 780, y, label, color, fnt=F["tiny"])
        draw.text((1010, y + 8), rule, font=F["small"], fill=MUTED)
        y += 58
    draw.text((780, 630), "Règles heuristiques documentées et inspectables", font=F["tiny"], fill=SUBTLE)
    footer(draw, [("faits ajoutés", GREEN), ("faits supprimés", RED), ("dimensions", BLUE), ("explicabilité", YELLOW)])
    save(image, "semantic-dna-mutations.png")


def main() -> None:
    generators = [
        csp_overview,
        csp_propagation,
        csp_scoring,
        csp_console,
        csp_search,
        oulipo_overview,
        oulipo_analysis,
        oulipo_constraints,
        oulipo_drift,
        oulipo_interface,
        dna_overview,
        dna_vector,
        dna_learning,
        dna_clustering,
        dna_ranking,
        dna_mutations,
    ]
    for generator in generators:
        generator()
    print(f"Generated {len(generators)} visuals in {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
