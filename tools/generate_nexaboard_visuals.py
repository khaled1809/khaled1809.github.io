#!/usr/bin/env python3
"""Generate self-contained NexaBoard documentation visuals for the portfolio."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "images" / "projects"
W, H = 1400, 850

BG = (7, 22, 38)
PANEL = (11, 33, 55)
PANEL_ALT = (13, 43, 70)
PANEL_LIGHT = (20, 52, 82)
BORDER = (48, 116, 166)
TEXT = (240, 246, 255)
MUTED = (164, 184, 210)
CYAN = (67, 226, 202)
BLUE = (89, 159, 255)
PURPLE = (157, 112, 255)
YELLOW = (255, 198, 71)
RED = (255, 91, 96)
GREEN = (87, 214, 137)
ORANGE = (255, 148, 82)
WHITE = (255, 255, 255)
INK = (31, 41, 55)
SOFT = (244, 247, 251)
GRAY = (107, 114, 128)

FONT_DIR = Path("/usr/share/fonts/opentype/inter")
FONTS = {
    "regular": FONT_DIR / "Inter-Regular.otf",
    "medium": FONT_DIR / "Inter-Medium.otf",
    "semibold": FONT_DIR / "Inter-SemiBold.otf",
    "bold": FONT_DIR / "Inter-Bold.otf",
}


def font(size: int, weight: str = "regular") -> ImageFont.FreeTypeFont:
    path = FONTS.get(weight, FONTS["regular"])
    if not path.is_file():
        fallback = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
        bold = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
        path = bold if weight in {"semibold", "bold"} and bold.is_file() else fallback
    return ImageFont.truetype(str(path), size)


def text_width(draw: ImageDraw.ImageDraw, value: str, fnt: ImageFont.FreeTypeFont) -> int:
    box = draw.textbbox((0, 0), value, font=fnt)
    return box[2] - box[0]


def wrap(draw: ImageDraw.ImageDraw, value: str, fnt: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    lines: list[str] = []
    for paragraph_text in value.split("\n"):
        words = paragraph_text.split()
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


def paragraph(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    value: str,
    fnt: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int],
    max_width: int,
    line_gap: int = 7,
    max_lines: int | None = None,
) -> int:
    x, y = xy
    lines = wrap(draw, value, fnt, max_width)
    if max_lines is not None:
        lines = lines[:max_lines]
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + line_gap
    return y


def rounded(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    radius: int = 22,
    fill: tuple[int, int, int] = PANEL,
    outline: tuple[int, int, int] = BORDER,
    width: int = 1,
) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def arrow(
    draw: ImageDraw.ImageDraw,
    start: tuple[int, int],
    end: tuple[int, int],
    color: tuple[int, int, int] = CYAN,
    width: int = 4,
) -> None:
    draw.line([start, end], fill=color, width=width)
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    length = 13
    for delta in (2.55, -2.55):
        tip = (end[0] + length * math.cos(angle + delta), end[1] + length * math.sin(angle + delta))
        draw.line([end, tip], fill=color, width=width)


def decorative(draw: ImageDraw.ImageDraw) -> None:
    for radius in (150, 230, 320):
        draw.arc((1120 - radius, -105 - radius, 1120 + radius, -105 + radius), 0, 360, fill=(19, 118, 143), width=1)
    draw.ellipse((1285, 780, 1303, 798), fill=CYAN)
    draw.text((1315, 778), "KD", font=font(22, "semibold"), fill=TEXT)


def header(draw: ImageDraw.ImageDraw, title: str, subtitle: str, badge: str, title_size: int = 43) -> None:
    draw.text((70, 52), title, font=font(title_size, "bold"), fill=TEXT)
    draw.text((70, 113), subtitle, font=font(22), fill=MUTED)
    badge_font = font(14, "medium")
    badge_width = text_width(draw, badge, badge_font) + 30
    draw.rounded_rectangle((1310 - badge_width, 62, 1310, 94), radius=16, fill=PANEL_ALT, outline=BORDER)
    draw.text((1325 - badge_width, 70), badge, font=badge_font, fill=CYAN)


def base(title: str, subtitle: str, badge: str, title_size: int = 43) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(image)
    decorative(draw)
    header(draw, title, subtitle, badge, title_size)
    return image, draw


def save(image: Image.Image, filename: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    image.save(OUT / filename, optimize=True)


def tag(draw: ImageDraw.ImageDraw, x: int, y: int, label: str, color: tuple[int, int, int] = CYAN) -> int:
    fnt = font(14, "medium")
    width = text_width(draw, label, fnt) + 28
    draw.rounded_rectangle((x, y, x + width, y + 32), radius=16, fill=PANEL_ALT, outline=BORDER)
    draw.text((x + 14, y + 7), label, font=fnt, fill=color)
    return x + width + 12


def footer_tags(draw: ImageDraw.ImageDraw, items: Iterable[tuple[str, tuple[int, int, int]]]) -> None:
    x = 70
    for label, color in items:
        x = tag(draw, x, 770, label, color)


def small_icon(draw: ImageDraw.ImageDraw, center: tuple[int, int], label: str, color: tuple[int, int, int]) -> None:
    x, y = center
    draw.ellipse((x - 25, y - 25, x + 25, y + 25), fill=color)
    fnt = font(13, "bold")
    tw = text_width(draw, label, fnt)
    draw.text((x - tw / 2, y - 8), label, font=fnt, fill=BG)


def metric(draw: ImageDraw.ImageDraw, x: int, y: int, number: str, title: str, detail: str, color: tuple[int, int, int]) -> None:
    draw.rounded_rectangle((x, y, x + 58, y + 58), radius=15, fill=color)
    fnt = font(17, "bold")
    tw = text_width(draw, number, fnt)
    draw.text((x + 29 - tw / 2, y + 16), number, font=fnt, fill=BG)
    draw.text((x + 78, y + 1), title, font=font(18, "semibold"), fill=TEXT)
    paragraph(draw, (x + 78, y + 29), detail, font(14), MUTED, 175, 3, 2)


def dark_node(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    title: str,
    body: str,
    color: tuple[int, int, int],
    label: str,
    body_size: int = 15,
) -> None:
    x0, y0, x1, y1 = box
    rounded(draw, box, radius=22, fill=PANEL_ALT, outline=color, width=2)
    small_icon(draw, (x0 + 48, y0 + 48), label, color)
    draw.text((x0 + 86, y0 + 24), title, font=font(20, "semibold"), fill=TEXT)
    paragraph(draw, (x0 + 24, y0 + 80), body, font(body_size), MUTED, x1 - x0 - 48, 5)


def ui_card(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], title: str, value: str, accent: tuple[int, int, int], detail: str) -> None:
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=14, fill=WHITE, outline=(226, 232, 240), width=1)
    draw.ellipse((x0 + 14, y0 + 16, x0 + 38, y0 + 40), fill=accent)
    draw.text((x0 + 48, y0 + 13), title, font=font(11, "semibold"), fill=GRAY)
    draw.text((x0 + 18, y0 + 48), value, font=font(24, "bold"), fill=INK)
    draw.text((x0 + 18, y0 + 80), detail, font=font(9), fill=GRAY)


def generate_overview() -> None:
    image, draw = base(
        "NexaBoard — projets, tâches et collaboration",
        "Une application d’équipe complète, du tableau de bord au Kanban transactionnel",
        "FULL-STACK",
        40,
    )

    # Reconstitution de l'interface d'après les composants Vue fournis.
    app = (70, 176, 1000, 725)
    rounded(draw, app, radius=28, fill=SOFT, outline=BLUE, width=2)
    x0, y0, x1, y1 = app
    draw.rounded_rectangle((x0, y0, x0 + 155, y1), radius=28, fill=(19, 24, 38))
    draw.rectangle((x0 + 126, y0, x0 + 155, y1), fill=(19, 24, 38))
    draw.rounded_rectangle((x0 + 25, y0 + 28, x0 + 67, y0 + 70), radius=12, fill=PURPLE)
    draw.text((x0 + 39, y0 + 39), "N", font=font(17, "bold"), fill=WHITE)
    draw.text((x0 + 78, y0 + 31), "NexaBoard", font=font(15, "bold"), fill=WHITE)
    nav_items = [("Dashboard", CYAN), ("Projets", BLUE), ("Équipe", PURPLE), ("Profil", MUTED)]
    ny = y0 + 116
    for i, (label, color) in enumerate(nav_items):
        if i == 0:
            draw.rounded_rectangle((x0 + 18, ny - 8, x0 + 137, ny + 28), radius=10, fill=(34, 47, 68))
        draw.ellipse((x0 + 30, ny + 2, x0 + 40, ny + 12), fill=color)
        draw.text((x0 + 50, ny - 2), label, font=font(11, "medium"), fill=WHITE if i == 0 else (178, 188, 205))
        ny += 48
    draw.text((x0 + 25, y1 - 66), "Mohamed B.", font=font(11, "semibold"), fill=WHITE)
    draw.text((x0 + 25, y1 - 45), "Manager", font=font(9), fill=(148, 163, 184))

    mx = x0 + 185
    draw.text((mx, y0 + 30), "Bonjour, Mohamed.", font=font(13, "semibold"), fill=PURPLE)
    draw.text((mx, y0 + 58), "Voici l’essentiel de votre activité.", font=font(24, "bold"), fill=INK)
    draw.text((mx, y0 + 94), "Surveillez les échéances et gardez les projets en mouvement.", font=font(11), fill=GRAY)
    draw.rounded_rectangle((x1 - 150, y0 + 36, x1 - 28, y0 + 76), radius=12, fill=PURPLE)
    draw.text((x1 - 132, y0 + 49), "+ Nouveau projet", font=font(10, "semibold"), fill=WHITE)

    card_y = y0 + 132
    widths = [170, 170, 170, 170]
    labels = [
        ("Projets", "06", BLUE, "Projets accessibles"),
        ("Terminées", "42", GREEN, "72% de réalisation"),
        ("En cours", "11", YELLOW, "Travail actif"),
        ("En retard", "03", RED, "À traiter"),
    ]
    cx = mx
    for width, item in zip(widths, labels):
        ui_card(draw, (cx, card_y, cx + width, card_y + 110), *item)
        cx += width + 14

    # Chart card.
    draw.rounded_rectangle((mx, card_y + 132, mx + 295, y1 - 28), radius=16, fill=WHITE, outline=(226, 232, 240))
    draw.text((mx + 18, card_y + 150), "État des tâches", font=font(13, "bold"), fill=INK)
    center = (mx + 145, card_y + 245)
    draw.ellipse((center[0] - 60, center[1] - 60, center[0] + 60, center[1] + 60), outline=(226, 232, 240), width=22)
    draw.arc((center[0] - 60, center[1] - 60, center[0] + 60, center[1] + 60), -90, 60, fill=PURPLE, width=22)
    draw.arc((center[0] - 60, center[1] - 60, center[0] + 60, center[1] + 60), 64, 190, fill=GREEN, width=22)
    draw.text((center[0] - 20, center[1] - 12), "56", font=font(22, "bold"), fill=INK)
    draw.text((center[0] - 25, center[1] + 18), "tâches", font=font(9), fill=GRAY)
    legend_y = y1 - 85
    for lx, color, label in ((mx + 25, (203, 213, 225), "À faire"), (mx + 110, PURPLE, "En cours"), (mx + 205, GREEN, "Terminées")):
        draw.ellipse((lx, legend_y, lx + 8, legend_y + 8), fill=color)
        draw.text((lx + 13, legend_y - 3), label, font=font(8), fill=GRAY)

    # Project progress + mini kanban.
    right_x = mx + 315
    draw.rounded_rectangle((right_x, card_y + 132, x1 - 28, y1 - 28), radius=16, fill=WHITE, outline=(226, 232, 240))
    draw.text((right_x + 18, card_y + 150), "Progression des projets", font=font(13, "bold"), fill=INK)
    projects = [("Site e-commerce", 70, PURPLE), ("Application mobile", 45, BLUE), ("Migration API", 88, GREEN)]
    py = card_y + 185
    for name, progress, color in projects:
        draw.text((right_x + 18, py), name, font=font(10, "semibold"), fill=INK)
        draw.text((x1 - 67, py), f"{progress}%", font=font(9, "semibold"), fill=GRAY)
        draw.rounded_rectangle((right_x + 18, py + 21, x1 - 50, py + 29), radius=4, fill=(229, 233, 240))
        bar_end = right_x + 18 + int((x1 - 68 - right_x) * progress / 100)
        draw.rounded_rectangle((right_x + 18, py + 21, bar_end, py + 29), radius=4, fill=color)
        py += 57
    draw.text((right_x + 18, py + 4), "Kanban", font=font(10, "bold"), fill=INK)
    cols = [("À faire", 2, (203, 213, 225)), ("En cours", 1, PURPLE), ("Terminées", 3, GREEN)]
    kx = right_x + 18
    for title, count, color in cols:
        draw.rounded_rectangle((kx, py + 28, kx + 118, py + 105), radius=10, fill=(248, 250, 252), outline=(226, 232, 240))
        draw.ellipse((kx + 10, py + 40, kx + 18, py + 48), fill=color)
        draw.text((kx + 24, py + 35), title, font=font(8, "semibold"), fill=INK)
        draw.rounded_rectangle((kx + 10, py + 58, kx + 108, py + 89), radius=7, fill=WHITE, outline=(226, 232, 240))
        draw.text((kx + 17, py + 65), f"{count} tâche{'s' if count > 1 else ''}", font=font(8), fill=GRAY)
        kx += 130

    # Recruiter-facing panel.
    rounded(draw, (1030, 176, 1330, 725), radius=28, fill=PANEL, outline=CYAN, width=2)
    draw.text((1062, 211), "Ce que le projet prouve", font=font(18, "semibold"), fill=MUTED)
    draw.text((1062, 247), "Une vraie application", font=font(28, "bold"), fill=CYAN)
    paragraph(draw, (1062, 292), "Frontend typé, API sécurisée, modèle métier, transactions, documentation et livraison automatisée.", font(16), MUTED, 232, 6, 5)
    metric(draw, 1062, 408, "03", "rôles métier", "Admin · Manager · Membre", PURPLE)
    metric(draw, 1062, 492, "05", "entités cœur", "Projet · membre · tâche · commentaire · activité", BLUE)
    metric(draw, 1062, 576, "11", "tests fournis", "8 Django + 3 Vitest à rejouer", GREEN)

    footer_tags(draw, [("Vue.js 3", GREEN), ("TypeScript", BLUE), ("Django REST", CYAN), ("PostgreSQL", PURPLE), ("Docker", ORANGE)])
    save(image, "nexaboard-overview.png")


def generate_architecture() -> None:
    image, draw = base(
        "Architecture — une séparation nette des responsabilités",
        "La SPA ne décide jamais seule des autorisations : l’API reste la source de vérité",
        "ARCHITECTURE",
        39,
    )

    dark_node(draw, (70, 230, 330, 460), "Vue.js 3", "TypeScript · Vue Router\nPinia · Tailwind CSS 4\nChart.js · vuedraggable", GREEN, "UI")
    dark_node(draw, (395, 230, 655, 460), "Nginx", "Bundle Vite statique\nFallback de la SPA\nReverse proxy /api", ORANGE, "NX")
    dark_node(draw, (720, 205, 1020, 485), "Django REST", "ViewSets · serializers\nPermissions · filtres\nSimpleJWT · OpenAPI", CYAN, "API")
    arrow(draw, (330, 345), (395, 345), GREEN)
    arrow(draw, (655, 345), (720, 345), CYAN)

    dark_node(draw, (1085, 230, 1330, 460), "PostgreSQL 17", "Django ORM\nContraintes et index\nTransactions et verrous", PURPLE, "PG")
    arrow(draw, (1020, 345), (1085, 345), PURPLE)

    # Internal architecture layers.
    boxes = [
        ((70, 545, 315, 705), "Stores Pinia", "auth · projets · tâches\ndashboard · notifications", BLUE, "ST"),
        ((345, 545, 590, 705), "Client Axios", "Bearer en mémoire\nrefresh unique · retry 401", GREEN, "HTTP"),
        ((620, 545, 865, 705), "Domaines Django", "accounts · workspace\ndashboard · core", CYAN, "PY"),
        ((895, 545, 1140, 705), "Contrats", "Swagger / OpenAPI\nPostman · types TS", YELLOW, "DOC"),
        ((1170, 545, 1330, 705), "Runtime", "Gunicorn\nhealthchecks\nGitHub Actions", ORANGE, "CI"),
    ]
    for box, title, body, color, label in boxes:
        dark_node(draw, box, title, body, color, label, 14)

    draw.line((850, 485, 850, 515), fill=BORDER, width=3)
    draw.line((190, 515, 1250, 515), fill=BORDER, width=2)
    for x, color in ((190, BLUE), (468, GREEN), (742, CYAN), (1017, YELLOW), (1250, ORANGE)):
        arrow(draw, (x, 515), (x, 545), color, 3)

    footer_tags(draw, [("SPA typée", GREEN), ("API REST", CYAN), ("Permissions objet", PURPLE), ("OpenAPI", YELLOW), ("PostgreSQL", BLUE)])
    save(image, "nexaboard-architecture.png")


def task_card(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], title: str, priority: str, color: tuple[int, int, int], person: str) -> None:
    x0, y0, x1, y1 = box
    rounded(draw, box, radius=14, fill=PANEL, outline=BORDER)
    draw.rounded_rectangle((x0 + 14, y0 + 14, x0 + 14 + text_width(draw, priority, font(10, "semibold")) + 18, y0 + 37), radius=10, fill=color)
    draw.text((x0 + 23, y0 + 20), priority, font=font(10, "semibold"), fill=BG)
    paragraph(draw, (x0 + 14, y0 + 51), title, font(14, "semibold"), TEXT, x1 - x0 - 28, 4, 2)
    draw.ellipse((x0 + 14, y1 - 34, x0 + 36, y1 - 12), fill=PURPLE)
    draw.text((x0 + 44, y1 - 31), person, font=font(10), fill=MUTED)


def generate_kanban_transaction() -> None:
    image, draw = base(
        "Kanban — fluidité côté Vue, cohérence côté PostgreSQL",
        "Le drag & drop optimiste reste réversible et l’ordre serveur est normalisé dans une transaction",
        "TRANSACTION",
        38,
    )

    # Kanban columns.
    columns = [
        ((70, 190, 350, 570), "À faire", (203, 213, 225), [("Créer la maquette", "HAUTE", RED, "Sarah"), ("Préparer le schéma", "MOYENNE", YELLOW, "Karim")]),
        ((380, 190, 660, 570), "En cours", PURPLE, [("Développer l’API", "URGENTE", ORANGE, "Khaled")]),
        ((690, 190, 970, 570), "Terminées", GREEN, [("Configurer le projet", "BASSE", GREEN, "Thomas")]),
    ]
    for box, title, color, cards in columns:
        x0, y0, x1, y1 = box
        rounded(draw, box, radius=24, fill=PANEL_ALT, outline=color, width=2)
        draw.ellipse((x0 + 20, y0 + 24, x0 + 32, y0 + 36), fill=color)
        draw.text((x0 + 45, y0 + 18), title, font=font(18, "semibold"), fill=TEXT)
        draw.rounded_rectangle((x1 - 48, y0 + 18, x1 - 20, y0 + 42), radius=12, fill=PANEL)
        draw.text((x1 - 38, y0 + 23), str(len(cards)), font=font(11, "bold"), fill=MUTED)
        cy = y0 + 70
        for card in cards:
            task_card(draw, (x0 + 18, cy, x1 - 18, cy + 132), *card)
            cy += 148
    arrow(draw, (303, 334), (426, 334), CYAN, 5)
    draw.text((315, 295), "drag", font=font(12, "bold"), fill=CYAN)

    # Server transaction pipeline.
    rounded(draw, (1010, 190, 1330, 570), radius=24, fill=PANEL, outline=CYAN, width=2)
    draw.text((1040, 222), "POST /tasks/{id}/move/", font=font(18, "semibold"), fill=CYAN)
    steps = [
        ("1", "transaction.atomic", "une unité de travail", BLUE),
        ("2", "select_for_update", "verrouillage des lignes", PURPLE),
        ("3", "Insertion", "position demandée bornée", YELLOW),
        ("4", "Normalisation", "colonnes source et cible", GREEN),
        ("5", "bulk_update", "positions + statut", CYAN),
        ("6", "Activity", "journal du déplacement", ORANGE),
    ]
    sy = 270
    for num, title, detail, color in steps:
        draw.ellipse((1040, sy, 1068, sy + 28), fill=color)
        draw.text((1050, sy + 7), num, font=font(10, "bold"), fill=BG)
        draw.text((1082, sy - 1), title, font=font(14, "semibold"), fill=TEXT)
        draw.text((1082, sy + 20), detail, font=font(11), fill=MUTED)
        sy += 48

    rounded(draw, (70, 615, 660, 710), radius=20, fill=PANEL, outline=GREEN, width=2)
    draw.text((100, 642), "Mise à jour optimiste", font=font(18, "semibold"), fill=GREEN)
    paragraph(draw, (100, 672), "Le store Pinia déplace immédiatement la carte pour garder l’interface réactive.", font(14), MUTED, 520, 4, 2)
    rounded(draw, (690, 615, 1330, 710), radius=20, fill=PANEL, outline=RED, width=2)
    draw.text((720, 642), "Rollback en cas d’échec", font=font(18, "semibold"), fill=RED)
    paragraph(draw, (720, 672), "Une copie de l’état précédent restaure toutes les tâches si l’API rejette le déplacement.", font(14), MUTED, 570, 4, 2)

    footer_tags(draw, [("vuedraggable", GREEN), ("Pinia", BLUE), ("transaction.atomic", CYAN), ("select_for_update", PURPLE), ("bulk_update", YELLOW)])
    save(image, "nexaboard-kanban-transaction.png")


def flow_step(draw: ImageDraw.ImageDraw, x: int, y: int, number: str, title: str, body: str, color: tuple[int, int, int], width: int = 230) -> None:
    rounded(draw, (x, y, x + width, y + 170), radius=22, fill=PANEL_ALT, outline=color, width=2)
    draw.rounded_rectangle((x + 18, y + 18, x + 58, y + 58), radius=10, fill=color)
    draw.text((x + 29, y + 30), number, font=font(12, "bold"), fill=BG)
    draw.text((x + 22, y + 76), title, font=font(18, "semibold"), fill=TEXT)
    paragraph(draw, (x + 22, y + 108), body, font(13), MUTED, width - 44, 4, 3)


def generate_auth_security() -> None:
    image, draw = base(
        "Authentification — session courte, refresh protégé",
        "Le navigateur ne persiste pas l’access token et le serveur révoque les refresh tokens utilisés",
        "SÉCURITÉ",
        39,
    )

    flow_step(draw, 70, 220, "01", "Connexion", "E-mail + mot de passe\nvalidateurs Django", BLUE)
    flow_step(draw, 335, 220, "02", "Paire JWT", "Access 15 min\nRefresh 7 jours", PURPLE)
    flow_step(draw, 600, 220, "03", "Stockage séparé", "Access en mémoire\nRefresh cookie HttpOnly", CYAN)
    flow_step(draw, 865, 220, "04", "Requête API", "Authorization: Bearer\npermissions DRF", GREEN)
    flow_step(draw, 1130, 220, "05", "Rotation", "401 → refresh unique\nancien token blacklisté", YELLOW, 200)
    for start, end, color in [((300, 305), (335, 305), BLUE), ((565, 305), (600, 305), PURPLE), ((830, 305), (865, 305), CYAN), ((1095, 305), (1130, 305), GREEN)]:
        arrow(draw, start, end, color, 3)

    rounded(draw, (70, 445, 650, 700), radius=24, fill=PANEL, outline=CYAN, width=2)
    draw.text((102, 480), "Intercepteur Axios", font=font(22, "semibold"), fill=CYAN)
    items = [
        "Ajoute le Bearer token à chaque requête authentifiée",
        "Ignore les routes login, register et reset lors du refresh",
        "Partage une refreshPromise entre plusieurs réponses 401",
        "Rejoue la requête d’origine avec le nouvel access token",
        "Déclenche auth:expired si la session ne peut plus être restaurée",
    ]
    iy = 528
    for item in items:
        draw.ellipse((104, iy + 6, 112, iy + 14), fill=CYAN)
        draw.text((126, iy), item, font=font(14), fill=MUTED)
        iy += 34

    rounded(draw, (690, 445, 1330, 700), radius=24, fill=PANEL, outline=PURPLE, width=2)
    draw.text((722, 480), "Défense en profondeur", font=font(22, "semibold"), fill=PURPLE)
    protections = [
        ("HttpOnly", "le refresh n’est pas lisible par JavaScript", CYAN),
        ("SameSite=Lax", "réduction du risque CSRF", BLUE),
        ("Rotation + blacklist", "réutilisation d’un ancien refresh bloquée", YELLOW),
        ("Permissions objet", "rôle et appartenance contrôlés côté API", GREEN),
        ("Reset Django", "token lié au mot de passe et réponse non énumérable", ORANGE),
    ]
    py = 526
    for title, body, color in protections:
        draw.rounded_rectangle((724, py, 860, py + 28), radius=14, fill=color)
        draw.text((738, py + 7), title, font=font(11, "bold"), fill=BG)
        draw.text((878, py + 5), body, font=font(13), fill=MUTED)
        py += 37

    footer_tags(draw, [("SimpleJWT", PURPLE), ("HttpOnly", CYAN), ("Rotation", YELLOW), ("Blacklist", RED), ("RBAC", GREEN)])
    save(image, "nexaboard-auth-security.png")


def entity(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], title: str, fields: list[str], color: tuple[int, int, int]) -> None:
    x0, y0, x1, y1 = box
    rounded(draw, box, radius=18, fill=PANEL_ALT, outline=color, width=2)
    draw.rounded_rectangle((x0, y0, x1, y0 + 42), radius=18, fill=color)
    draw.rectangle((x0, y0 + 24, x1, y0 + 42), fill=color)
    draw.text((x0 + 16, y0 + 11), title, font=font(16, "bold"), fill=BG)
    y = y0 + 56
    for field in fields:
        draw.text((x0 + 16, y), field, font=font(11), fill=MUTED)
        y += 23


def generate_data_model() -> None:
    image, draw = base(
        "Modèle métier — équipe, travail et traçabilité",
        "Les relations et permissions sont explicites au lieu d’être cachées dans l’interface",
        "DOMAINE",
        40,
    )

    entity(draw, (70, 205, 280, 395), "User", ["email unique", "role global", "profil", "mot de passe Django"], BLUE)
    entity(draw, (365, 185, 620, 405), "Project", ["manager / created_by", "dates + statut", "progress calculé", "couleur + description"], PURPLE)
    entity(draw, (365, 470, 620, 675), "ProjectMembership", ["project + user", "role projet", "contrainte unique", "joined_at"], CYAN)
    entity(draw, (720, 185, 960, 425), "Task", ["statut + priorité", "position Kanban", "due_date", "assigned_to / created_by", "index projet-statut-position"], GREEN)
    entity(draw, (1050, 205, 1280, 395), "Comment", ["task", "author", "body", "timestamps"], YELLOW)
    entity(draw, (1050, 485, 1280, 690), "Activity", ["project + actor", "action", "entity_type / id", "metadata JSON", "index activité récente"], ORANGE)

    arrow(draw, (280, 300), (365, 300), BLUE, 3)
    arrow(draw, (492, 405), (492, 470), CYAN, 3)
    arrow(draw, (620, 300), (720, 300), PURPLE, 3)
    arrow(draw, (960, 300), (1050, 300), GREEN, 3)
    arrow(draw, (960, 365), (1050, 555), ORANGE, 3)
    draw.text((290, 270), "crée / gère", font=font(11, "medium"), fill=MUTED)
    draw.text((505, 432), "appartenance", font=font(11, "medium"), fill=MUTED)
    draw.text((632, 270), "contient", font=font(11, "medium"), fill=MUTED)
    draw.text((972, 270), "discute", font=font(11, "medium"), fill=MUTED)

    rounded(draw, (70, 465, 280, 690), radius=18, fill=PANEL, outline=BORDER)
    draw.text((94, 490), "Matrice de droits", font=font(18, "semibold"), fill=TEXT)
    rows = [
        ("Admin", "tous les projets", PURPLE),
        ("Manager", "configuration + équipe", BLUE),
        ("Membre", "tâches + commentaires", GREEN),
        ("Auteur", "son commentaire", YELLOW),
    ]
    ry = 535
    for role, right, color in rows:
        draw.rounded_rectangle((94, ry, 165, ry + 27), radius=13, fill=color)
        draw.text((106, ry + 7), role, font=font(10, "bold"), fill=BG)
        paragraph(draw, (176, ry + 3), right, font(11), MUTED, 80, 2, 2)
        ry += 38

    footer_tags(draw, [("Django ORM", CYAN), ("Contraintes", PURPLE), ("Index", GREEN), ("Permissions objet", BLUE), ("Journal d’activité", ORANGE)])
    save(image, "nexaboard-data-model.png")


def ci_job(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], title: str, steps: list[str], color: tuple[int, int, int]) -> None:
    x0, y0, x1, y1 = box
    rounded(draw, box, radius=22, fill=PANEL_ALT, outline=color, width=2)
    draw.text((x0 + 24, y0 + 22), title, font=font(21, "semibold"), fill=color)
    y = y0 + 66
    for index, step in enumerate(steps, 1):
        draw.ellipse((x0 + 26, y + 2, x0 + 50, y + 26), fill=color)
        draw.text((x0 + 35, y + 7), str(index), font=font(9, "bold"), fill=BG)
        draw.text((x0 + 64, y), step, font=font(14), fill=MUTED)
        y += 34


def generate_ci_deployment() -> None:
    image, draw = base(
        "Livraison — documentation, CI et conteneurs",
        "Le dépôt décrit les contrôles automatiques et une pile de production reproductible",
        "DELIVERY",
        40,
    )

    rounded(draw, (70, 190, 255, 315), radius=22, fill=PANEL_ALT, outline=PURPLE, width=2)
    small_icon(draw, (120, 252), "GH", PURPLE)
    draw.text((155, 220), "Push / PR", font=font(18, "semibold"), fill=TEXT)
    draw.text((155, 252), "GitHub Actions", font=font(13), fill=MUTED)
    arrow(draw, (255, 252), (320, 252), CYAN)

    ci_job(draw, (320, 175, 655, 415), "Job backend", ["Python 3.13", "pip install", "manage.py check", "migrations --check", "8 tests Django"], CYAN)
    ci_job(draw, (695, 175, 1030, 415), "Job frontend", ["Node.js 22", "npm install", "3 tests Vitest", "vue-tsc", "build Vite"], GREEN)
    arrow(draw, (1030, 285), (1095, 285), GREEN)
    rounded(draw, (1095, 205, 1330, 365), radius=22, fill=PANEL, outline=YELLOW, width=2)
    draw.text((1125, 232), "Contrats", font=font(19, "semibold"), fill=YELLOW)
    paragraph(draw, (1125, 270), "Swagger / OpenAPI\nCollection Postman\nDocumentation sécurité", font(14), MUTED, 180, 5)

    draw.text((70, 448), "Déploiement Docker Compose", font=font(22, "semibold"), fill=TEXT)
    services = [
        ((70, 495, 330, 690), "Frontend", "Nginx 1.27\nSPA Vite\nreverse proxy /api", ORANGE, "WEB"),
        ((395, 495, 675, 690), "Backend", "Django REST\nGunicorn · 3 workers\nmigrations + seed", CYAN, "API"),
        ((740, 495, 1000, 690), "PostgreSQL", "Version 17 Alpine\nvolume persistant\npg_isready", PURPLE, "DB"),
        ((1065, 495, 1330, 690), "Healthchecks", "ordre de démarrage\nAPI /health/\nfrontend HTTP", GREEN, "OK"),
    ]
    for box, title, body, color, label in services:
        dark_node(draw, box, title, body, color, label, 14)
    for start, end, color in [((330, 592), (395, 592), ORANGE), ((675, 592), (740, 592), CYAN), ((1000, 592), (1065, 592), PURPLE)]:
        arrow(draw, start, end, color, 3)

    draw.rounded_rectangle((70, 720, 1030, 756), radius=18, fill=(31, 49, 69), outline=BORDER)
    draw.text((88, 730), "Validation locale de cette livraison : contrôles statiques réussis ; tests et Docker à rejouer avec les dépendances.", font=font(13, "medium"), fill=MUTED)

    footer_tags(draw, [("GitHub Actions", PURPLE), ("Vitest", GREEN), ("Django tests", CYAN), ("Gunicorn", BLUE), ("Nginx", ORANGE)])
    save(image, "nexaboard-ci-deployment.png")


def main() -> None:
    generate_overview()
    generate_architecture()
    generate_kanban_transaction()
    generate_auth_security()
    generate_data_model()
    generate_ci_deployment()
    print("Generated 6 NexaBoard visuals in", OUT)


if __name__ == "__main__":
    main()
