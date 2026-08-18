#!/usr/bin/env python3
"""Generate documentation visuals for the Java 2D occupation game.

The diagrams use the same dark visual language as the other portfolio case
studies. The application image is based on a real execution screenshot.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "images" / "projects"
SOURCE_CAPTURE = OUT / "java-occupation-source-capture.png"
WIDTH, HEIGHT = 1400, 850

BG = (7, 22, 38)
PANEL = (11, 33, 55)
PANEL_ALT = (13, 43, 70)
BORDER = (48, 116, 166)
TEXT = (240, 246, 255)
MUTED = (164, 184, 210)
ACCENT = (67, 226, 202)
BLUE = (89, 159, 255)
PURPLE = (157, 112, 255)
YELLOW = (255, 198, 71)
RED = (255, 91, 96)
WHITE = (255, 255, 255)

FONT_REGULAR = "/usr/share/fonts/opentype/inter/Inter-Regular.otf"
FONT_MEDIUM = "/usr/share/fonts/opentype/inter/Inter-Medium.otf"
FONT_SEMIBOLD = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
FONT_BOLD = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"


def font(size: int, weight: str = "regular") -> ImageFont.FreeTypeFont:
    path = {
        "regular": FONT_REGULAR,
        "medium": FONT_MEDIUM,
        "semibold": FONT_SEMIBOLD,
        "bold": FONT_BOLD,
    }[weight]
    return ImageFont.truetype(path, size)


def rounded(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], radius: int = 22,
            fill: tuple[int, int, int] = PANEL, outline: tuple[int, int, int] = BORDER,
            width: int = 1) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def text_width(draw: ImageDraw.ImageDraw, value: str, fnt: ImageFont.FreeTypeFont) -> int:
    box = draw.textbbox((0, 0), value, font=fnt)
    return box[2] - box[0]


def wrap(draw: ImageDraw.ImageDraw, value: str, fnt: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    words = value.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = word if not current else f"{current} {word}"
        if text_width(draw, candidate, fnt) <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def paragraph(draw: ImageDraw.ImageDraw, xy: tuple[int, int], value: str,
              fnt: ImageFont.FreeTypeFont, fill: tuple[int, int, int], max_width: int,
              line_gap: int = 8) -> int:
    x, y = xy
    for line in wrap(draw, value, fnt, max_width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + line_gap
    return y


def arrow(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int],
          color: tuple[int, int, int] = ACCENT, width: int = 4) -> None:
    draw.line([start, end], fill=color, width=width)
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    length = 12
    for delta in (2.55, -2.55):
        tip = (end[0] + length * math.cos(angle + delta), end[1] + length * math.sin(angle + delta))
        draw.line([end, tip], fill=color, width=width)


def tag(draw: ImageDraw.ImageDraw, x: int, y: int, label: str,
        color: tuple[int, int, int] = ACCENT) -> int:
    fnt = font(14, "medium")
    w = text_width(draw, label, fnt) + 28
    draw.rounded_rectangle((x, y, x + w, y + 32), radius=16, fill=PANEL_ALT, outline=BORDER, width=1)
    draw.text((x + 14, y + 7), label, font=fnt, fill=color)
    return x + w + 12


def header(draw: ImageDraw.ImageDraw, title: str, subtitle: str, badge: str,
           title_size: int = 44) -> None:
    draw.text((70, 54), title, font=font(title_size, "bold"), fill=TEXT)
    draw.text((70, 116), subtitle, font=font(23), fill=MUTED)
    badge_font = font(14, "medium")
    badge_w = text_width(draw, badge, badge_font) + 30
    draw.rounded_rectangle((1310 - badge_w, 62, 1310, 94), radius=16, fill=PANEL_ALT, outline=BORDER)
    draw.text((1325 - badge_w, 70), badge, font=badge_font, fill=ACCENT)



def decorative_grid(draw: ImageDraw.ImageDraw) -> None:
    for radius in (150, 230, 320):
        draw.arc((1120 - radius, -105 - radius, 1120 + radius, -105 + radius), 0, 360, fill=(19, 118, 143), width=1)
    draw.ellipse((1285, 780, 1303, 798), fill=ACCENT)
    draw.text((1315, 778), "KD", font=font(22, "semibold"), fill=TEXT)


def base(title: str, subtitle: str, badge: str, title_size: int = 44) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(image)
    decorative_grid(draw)
    header(draw, title, subtitle, badge, title_size)
    return image, draw


def crop_application(source: Image.Image) -> Image.Image:
    """Crop the centred 800×600 Swing window from a 1280×900 root screenshot."""
    if source.size == (1280, 900):
        return source.crop((240, 150, 1040, 750))
    # Fallback: remove uniform black margins using the non-black bounding box.
    rgb = source.convert("RGB")
    bbox = rgb.getbbox()
    return rgb.crop(bbox) if bbox else rgb


def contain(image: Image.Image, size: tuple[int, int], background: tuple[int, int, int] = PANEL) -> Image.Image:
    target = Image.new("RGB", size, background)
    copy = image.copy().convert("RGB")
    copy.thumbnail(size, Image.Resampling.LANCZOS)
    x = (size[0] - copy.width) // 2
    y = (size[1] - copy.height) // 2
    target.paste(copy, (x, y))
    return target


def save(image: Image.Image, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    image.save(OUT / name, optimize=True)


def generate_application(capture: Image.Image) -> None:
    image, draw = base(
        "Application exécutée — capture réelle",
        "Création, déplacement et suppression de formes dans une interface Java Swing",
        "JAVA SWING",
        42,
    )
    rounded(draw, (70, 174, 1330, 738), radius=26, fill=PANEL_ALT, outline=BORDER, width=2)
    app = contain(crop_application(capture), (1160, 500), background=(3, 10, 18))
    image.paste(app, (120, 204))
    draw.rounded_rectangle((120, 204, 1280, 704), radius=12, outline=(83, 151, 195), width=2)
    x = 70
    for label, color in (("JAR compilé avec Ant", ACCENT), ("4 formes maximum", BLUE), ("Score par surface", YELLOW), ("Événements souris", PURPLE)):
        x = tag(draw, x, 770, label, color)
    save(image, "java-occupation-application.png")


def generate_overview(capture: Image.Image) -> None:
    image, draw = base(
        "Jeu 2D d’occupation maximale",
        "Architecture logicielle, géométrie 2D et interactions souris",
        "LOGICIEL JAVA",
        46,
    )
    # Screenshot card
    rounded(draw, (70, 176, 865, 728), radius=28, fill=PANEL_ALT, outline=BORDER, width=2)
    app = contain(crop_application(capture), (735, 500), background=(3, 10, 18))
    image.paste(app, (100, 204))
    draw.rounded_rectangle((100, 204, 835, 704), radius=12, outline=(83, 151, 195), width=2)

    # Technical summary
    rounded(draw, (900, 176, 1330, 728), radius=28, fill=PANEL, outline=ACCENT, width=2)
    draw.text((934, 210), "Objectif", font=font(18, "semibold"), fill=MUTED)
    draw.text((934, 242), "Maximiser", font=font(36, "bold"), fill=ACCENT)
    draw.text((934, 286), "la surface occupée", font=font(26, "semibold"), fill=TEXT)
    paragraph(draw, (934, 334), "Le joueur place jusqu’à quatre cercles ou rectangles au milieu d’obstacles générés aléatoirement.", font(18), MUTED, 350, 7)

    metrics = [
        ("04", "modes souris", "Créer cercle · rectangle · déplacer · supprimer", BLUE),
        ("03", "patterns structurants", "Observer · State · Strategy", PURPLE),
        ("03", "collisions", "cercle/cercle · rectangle/rectangle · mixte", YELLOW),
    ]
    y = 448
    for number, title, caption, color in metrics:
        draw.rounded_rectangle((934, y, 990, y + 54), radius=14, fill=color)
        draw.text((949, y + 15), number, font=font(16, "bold"), fill=BG)
        draw.text((1008, y + 2), title, font=font(18, "semibold"), fill=TEXT)
        paragraph(draw, (1008, y + 28), caption, font(14), MUTED, 285, 3)
        y += 78

    x = 70
    for label, color in (("Java", BLUE), ("Swing / Java2D", ACCENT), ("MVC", PURPLE), ("Design patterns", YELLOW), ("Géométrie", RED)):
        x = tag(draw, x, 770, label, color)
    save(image, "java-occupation-overview.png")


def card(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], number: str, title: str,
         body: str, color: tuple[int, int, int]) -> None:
    x0, y0, x1, y1 = box
    rounded(draw, box, radius=24, fill=PANEL_ALT, outline=BORDER, width=1)
    draw.rounded_rectangle((x0 + 18, y0 + 18, x0 + 60, y0 + 60), radius=11, fill=color)
    draw.text((x0 + 30, y0 + 31), number, font=font(13, "bold"), fill=BG)
    draw.text((x0 + 76, y0 + 19), title, font=font(21, "semibold"), fill=TEXT)
    paragraph(draw, (x0 + 24, y0 + 82), body, font(16), MUTED, x1 - x0 - 48, 6)


def generate_architecture() -> None:
    image, draw = base(
        "Architecture — responsabilités séparées",
        "Le modèle géométrique reste indépendant du rendu et des modes d’interaction",
        "MVC + PATTERNS",
        43,
    )

    card(draw, (70, 180, 365, 360), "01", "Main / composition", "Crée le GameModel, le GamePanel, le MouseController et les boutons Swing qui sélectionnent le mode actif.", YELLOW)
    card(draw, (445, 180, 760, 360), "02", "MouseController", "Délègue chaque événement à un MouseState : création, déplacement ou suppression, sans chaîne de conditions centrale.", PURPLE)
    card(draw, (840, 180, 1330, 360), "03", "GamePanel / Java2D", "Dessine les obstacles rouges, les formes bleues, l’aperçu semi-transparent et le HUD avec anti-aliasing.", BLUE)

    arrow(draw, (365, 270), (445, 270))
    arrow(draw, (760, 270), (840, 270))

    card(draw, (70, 430, 455, 670), "04", "GameModel", "Conserve deux ShapeGroup, limite le joueur à quatre formes, calcule le score et délègue la génération des obstacles.", ACCENT)
    card(draw, (505, 430, 900, 670), "05", "Domaine géométrique", "Shape définit area() et intersects(). Circle, Rectangle, Point et ShapeGroup portent les calculs de surface et de collision.", RED)
    card(draw, (950, 430, 1330, 670), "06", "Observer & Strategy", "ModelListener déclenche les rafraîchissements ; ShapeGenerationStrategy rend la génération aléatoire remplaçable.", YELLOW)

    arrow(draw, (650, 360), (650, 430))
    arrow(draw, (455, 550), (505, 550))
    arrow(draw, (900, 550), (950, 550))

    x = 70
    for label, color in (("Faible couplage", ACCENT), ("Polymorphisme", BLUE), ("État remplaçable", PURPLE), ("Rendu observable", YELLOW)):
        x = tag(draw, x, 752, label, color)
    save(image, "java-occupation-architecture.png")


def generate_states() -> None:
    image, draw = base(
        "Pattern State — une souris, quatre comportements",
        "MouseController transmet les événements au mode sélectionné par les boutons de l’interface",
        "INTERACTIONS",
        41,
    )

    # central controller
    rounded(draw, (515, 315, 885, 530), radius=30, fill=PANEL_ALT, outline=ACCENT, width=3)
    draw.text((557, 350), "MouseController", font=font(29, "bold"), fill=TEXT)
    paragraph(draw, (557, 402), "setState(MouseState) puis délégation de mousePressed, mouseMoved, mouseDragged et mouseReleased.", font(17), MUTED, 285, 7)

    states = [
        ((70, 190, 430, 345), "Créer un cercle", "1er clic : centre\nMouvement : rayon + preview\n2e clic : ajout au modèle", BLUE),
        ((970, 190, 1330, 345), "Créer un rectangle", "1er clic : origine\nmin/abs : toutes directions\n2e clic : validation", PURPLE),
        ((70, 530, 430, 685), "Déplacer", "Sélection par hit-test\nConservation de l’offset\nDrag : nouvelle position", ACCENT),
        ((970, 530, 1330, 685), "Supprimer", "Clic à l’intérieur\nRecherche dans les formes joueur\nSuppression + notification", RED),
    ]
    for idx, (box, title, body, color) in enumerate(states, 1):
        x0, y0, x1, y1 = box
        rounded(draw, box, radius=24, fill=PANEL_ALT, outline=BORDER)
        draw.rounded_rectangle((x0 + 18, y0 + 18, x0 + 58, y0 + 58), radius=10, fill=color)
        draw.text((x0 + 30, y0 + 30), f"0{idx}", font=font(12, "bold"), fill=BG)
        draw.text((x0 + 74, y0 + 20), title, font=font(21, "semibold"), fill=TEXT)
        y = y0 + 72
        for line in body.split("\n"):
            draw.ellipse((x0 + 24, y + 7, x0 + 32, y + 15), fill=color)
            draw.text((x0 + 44, y), line, font=font(16), fill=MUTED)
            y += 27

    arrow(draw, (430, 280), (515, 365), BLUE)
    arrow(draw, (970, 280), (885, 365), PURPLE)
    arrow(draw, (430, 600), (515, 485), ACCENT)
    arrow(draw, (970, 600), (885, 485), RED)

    rounded(draw, (445, 590, 955, 700), radius=22, fill=PANEL, outline=BORDER)
    draw.text((478, 616), "Bénéfice architectural", font=font(18, "semibold"), fill=ACCENT)
    paragraph(draw, (478, 650), "Ajouter un nouveau mode ne modifie pas le contrôleur : il suffit d’implémenter MouseState.", font(17), MUTED, 440, 6)

    x = 70
    for label, color in (("Prévisualisation", BLUE), ("Hit-testing", ACCENT), ("Offset de déplacement", PURPLE), ("Délégation", YELLOW)):
        x = tag(draw, x, 752, label, color)
    save(image, "java-occupation-states.png")


def generate_collisions() -> None:
    image, draw = base(
        "Géométrie de collision — trois cas spécialisés",
        "Chaque sous-classe de Shape implémente intersects(Shape) avec la formule adaptée",
        "ALGORITHMES 2D",
        41,
    )

    panels = [
        (70, 185, 435, 680, "Cercle – cercle", BLUE),
        (518, 185, 883, 680, "Rectangle – rectangle", YELLOW),
        (965, 185, 1330, 680, "Cercle – rectangle", PURPLE),
    ]
    for x0, y0, x1, y1, title, color in panels:
        rounded(draw, (x0, y0, x1, y1), radius=26, fill=PANEL_ALT, outline=BORDER, width=2)
        draw.text((x0 + 28, y0 + 28), title, font=font(22, "semibold"), fill=TEXT)
        draw.line((x0 + 28, y0 + 68, x1 - 28, y0 + 68), fill=BORDER, width=1)

    # circle-circle
    draw.ellipse((118, 290, 270, 442), outline=BLUE, width=5)
    draw.ellipse((230, 330, 382, 482), outline=RED, width=5)
    draw.line((194, 366, 306, 406), fill=ACCENT, width=3)
    draw.ellipse((190, 362, 198, 370), fill=TEXT)
    draw.ellipse((302, 402, 310, 410), fill=TEXT)
    draw.text((105, 520), "distance(centres)", font=font(18, "semibold"), fill=TEXT)
    draw.text((116, 554), "≤ rayon₁ + rayon₂", font=font(22, "bold"), fill=ACCENT)
    paragraph(draw, (105, 604), "La distance euclidienne suffit pour déterminer le chevauchement.", font(15), MUTED, 290, 5)

    # rectangle-rectangle
    draw.rectangle((565, 290, 735, 445), outline=YELLOW, width=5)
    draw.rectangle((680, 355, 835, 505), outline=RED, width=5)
    draw.line((565, 530, 835, 530), fill=BORDER, width=2)
    draw.text((552, 552), "Séparation impossible sur X", font=font(16, "semibold"), fill=TEXT)
    draw.text((552, 580), "ET séparation impossible sur Y", font=font(16, "semibold"), fill=TEXT)
    paragraph(draw, (552, 620), "Test AABB avec quatre comparaisons strictes sur les bords.", font(15), MUTED, 300, 5)

    # circle-rectangle
    draw.rectangle((1010, 300, 1210, 485), outline=PURPLE, width=5)
    draw.ellipse((1160, 370, 1280, 490), outline=BLUE, width=5)
    draw.ellipse((1205, 425, 1217, 437), fill=ACCENT)
    draw.line((1211, 431, 1220, 430), fill=ACCENT, width=3)
    draw.text((998, 530), "closestX / closestY", font=font(18, "semibold"), fill=TEXT)
    draw.text((998, 562), "obtenus avec clamp()", font=font(19, "bold"), fill=ACCENT)
    paragraph(draw, (998, 606), "Le point le plus proche du rectangle est comparé au rayon du cercle.", font(15), MUTED, 295, 5)

    rounded(draw, (260, 712, 1140, 775), radius=20, fill=PANEL, outline=RED)
    draw.text((290, 731), "Limite actuelle : ces calculs protègent la génération des obstacles, mais ne bloquent pas encore toutes les superpositions du joueur.", font=font(16, "medium"), fill=TEXT)
    save(image, "java-occupation-collisions.png")


def generate_score() -> None:
    image, draw = base(
        "Score et règles de placement",
        "GameModel limite le joueur à quatre formes et additionne leur surface",
        "MODÈLE DE JEU",
        43,
    )

    rounded(draw, (70, 180, 820, 690), radius=28, fill=PANEL_ALT, outline=BORDER, width=2)
    draw.text((105, 214), "Surface totale", font=font(24, "semibold"), fill=TEXT)
    draw.text((105, 258), "score = Σ area(forme)", font=font(34, "bold"), fill=ACCENT)

    # Shape examples
    shapes = [
        ("circle", (160, 405), 62, BLUE, "πr²"),
        ("rect", (345, 350, 490, 460), None, PURPLE, "largeur × hauteur"),
        ("circle", (610, 405), 48, YELLOW, "πr²"),
        ("rect", (560, 520, 735, 615), None, RED, "largeur × hauteur"),
    ]
    for index, (kind, geom, size, color, formula) in enumerate(shapes, 1):
        if kind == "circle":
            cx, cy = geom
            r = int(size or 0)
            draw.ellipse((cx-r, cy-r, cx+r, cy+r), fill=color)
            label_x, label_y = cx-r, cy+r+15
        else:
            x0, y0, x1, y1 = geom
            draw.rounded_rectangle((x0, y0, x1, y1), radius=12, fill=color)
            label_x, label_y = x0, y1+15
        draw.text((label_x, label_y), f"forme {index} · {formula}", font=font(15, "medium"), fill=MUTED)

    rounded(draw, (860, 180, 1330, 690), radius=28, fill=PANEL, outline=ACCENT, width=2)
    draw.text((898, 218), "Règles implémentées", font=font(24, "semibold"), fill=TEXT)
    rules = [
        ("4", "formes maximum", "getRemainingShapes() suit le quota restant.", BLUE),
        ("5", "obstacles visés", "RandomShapeStrategy tente de les placer sans intersection.", RED),
        ("300", "tentatives bornées", "La boucle s’arrête même dans une configuration saturée.", YELLOW),
        ("1", "score agrégé", "ShapeGroup.computeTotalArea() additionne le polymorphisme.", ACCENT),
    ]
    y = 285
    for number, title, caption, color in rules:
        draw.rounded_rectangle((898, y, 958, y + 56), radius=15, fill=color)
        draw.text((916, y + 14), number, font=font(18, "bold"), fill=BG)
        draw.text((978, y), title, font=font(18, "semibold"), fill=TEXT)
        paragraph(draw, (978, y + 28), caption, font(14), MUTED, 305, 3)
        y += 90

    rounded(draw, (225, 715, 1175, 778), radius=20, fill=PANEL_ALT, outline=BORDER)
    draw.text((255, 733), "Évolution prévue : calculer un taux d’occupation utile, valider les limites du plateau et refuser une position en collision avant de la confirmer.", font=font(16, "medium"), fill=TEXT)
    save(image, "java-occupation-score.png")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--capture",
        type=Path,
        default=SOURCE_CAPTURE,
        help="Root screenshot containing the centred Swing window.",
    )
    args = parser.parse_args()
    if not args.capture.is_file():
        raise FileNotFoundError(args.capture)
    capture = Image.open(args.capture).convert("RGB")
    generate_application(capture)
    generate_overview(capture)
    generate_architecture()
    generate_states()
    generate_collisions()
    generate_score()
    print("Generated 6 Java occupation visuals in", OUT)


if __name__ == "__main__":
    main()
