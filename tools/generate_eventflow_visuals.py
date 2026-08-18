#!/usr/bin/env python3
"""Generate self-contained EventFlow documentation visuals for the portfolio."""

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

FONT_DIR = Path("/usr/share/fonts/opentype/inter")
FONTS = {
    "regular": FONT_DIR / "Inter-Regular.otf",
    "medium": FONT_DIR / "Inter-Medium.otf",
    "semibold": FONT_DIR / "Inter-SemiBold.otf",
    "bold": FONT_DIR / "Inter-Bold.otf",
}


def font(size: int, weight: str = "regular") -> ImageFont.FreeTypeFont:
    path = FONTS[weight]
    if not path.is_file():
        fallback = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
        path = fallback
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


def small_icon(draw: ImageDraw.ImageDraw, center: tuple[int, int], label: str, color: tuple[int, int, int]) -> None:
    x, y = center
    draw.ellipse((x - 25, y - 25, x + 25, y + 25), fill=color)
    fnt = font(14, "bold")
    tw = text_width(draw, label, fnt)
    draw.text((x - tw / 2, y - 8), label, font=fnt, fill=BG)


def tech_node(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    title: str,
    body: str,
    color: tuple[int, int, int],
    label: str = "",
    body_size: int = 15,
) -> None:
    x0, y0, x1, y1 = box
    rounded(draw, box, radius=22, fill=PANEL_ALT, outline=color, width=2)
    if label:
        small_icon(draw, (x0 + 48, y0 + 48), label, color)
        tx = x0 + 86
    else:
        tx = x0 + 24
    draw.text((tx, y0 + 24), title, font=font(20, "semibold"), fill=TEXT)
    paragraph(draw, (x0 + 24, y0 + 78), body, font(body_size), MUTED, x1 - x0 - 48, 5)


def metric(draw: ImageDraw.ImageDraw, x: int, y: int, number: str, title: str, detail: str, color: tuple[int, int, int]) -> None:
    draw.rounded_rectangle((x, y, x + 58, y + 58), radius=15, fill=color)
    fnt = font(17, "bold")
    tw = text_width(draw, number, fnt)
    draw.text((x + 29 - tw / 2, y + 16), number, font=fnt, fill=BG)
    draw.text((x + 78, y + 1), title, font=font(18, "semibold"), fill=TEXT)
    paragraph(draw, (x + 78, y + 29), detail, font(14), MUTED, 285, 3, 2)


def footer_tags(draw: ImageDraw.ImageDraw, items: Iterable[tuple[str, tuple[int, int, int]]]) -> None:
    x = 70
    for label, color in items:
        x = tag(draw, x, 770, label, color)


def generate_overview() -> None:
    image, draw = base(
        "EventFlow — plateforme événementielle full-stack",
        "Réservation atomique, paiement idempotent et billetterie QR sécurisée",
        "FULL-STACK",
        42,
    )

    rounded(draw, (70, 176, 875, 725), radius=28, fill=PANEL_ALT, outline=BORDER, width=2)
    draw.text((108, 208), "Un parcours transactionnel complet", font=font(24, "semibold"), fill=TEXT)
    draw.text((108, 248), "du catalogue au contrôle d’entrée", font=font(34, "bold"), fill=CYAN)

    # Product-style flow.
    flow = [
        ((112, 345, 292, 510), "01", "Catalogue", "React 19\nRecherche et fiches", BLUE),
        ((330, 345, 510, 510), "02", "Réservation", "MongoDB atomique\nCapacité protégée", PURPLE),
        ((548, 345, 728, 510), "03", "Paiement", "Stripe Checkout\nWebhook idempotent", YELLOW),
    ]
    for box, number, title, body, color in flow:
        x0, y0, x1, y1 = box
        rounded(draw, box, radius=20, fill=PANEL, outline=color, width=2)
        draw.rounded_rectangle((x0 + 18, y0 + 18, x0 + 58, y0 + 58), radius=10, fill=color)
        draw.text((x0 + 29, y0 + 30), number, font=font(12, "bold"), fill=BG)
        draw.text((x0 + 22, y0 + 78), title, font=font(19, "semibold"), fill=TEXT)
        paragraph(draw, (x0 + 22, y0 + 112), body, font(14), MUTED, x1 - x0 - 44, 4)
    arrow(draw, (292, 427), (330, 427), CYAN, 3)
    arrow(draw, (510, 427), (548, 427), CYAN, 3)

    rounded(draw, (108, 560, 836, 680), radius=22, fill=PANEL, outline=CYAN, width=2)
    small_icon(draw, (158, 620), "QR", CYAN)
    draw.text((200, 580), "Billet signé et consommable une seule fois", font=font(21, "semibold"), fill=TEXT)
    paragraph(draw, (200, 618), "UUID + payload versionné + HMAC SHA-256 + comparaison constante + transition atomique valid → used.", font(16), MUTED, 595, 5, 2)

    rounded(draw, (910, 176, 1330, 725), radius=28, fill=PANEL, outline=CYAN, width=2)
    draw.text((944, 210), "Architecture", font=font(18, "semibold"), fill=MUTED)
    draw.text((944, 246), "Production-ready", font=font(33, "bold"), fill=CYAN)
    paragraph(draw, (944, 292), "Une SPA, une API REST en couches, deux moteurs de données et un fournisseur de paiement isolé.", font(17), MUTED, 345, 6, 4)
    metric(draw, 944, 408, "04", "services Docker", "client · API · MySQL · MongoDB", BLUE)
    metric(draw, 944, 492, "02", "bases spécialisées", "SQL relationnel + documents métier", PURPLE)
    metric(draw, 944, 576, "08", "tests Node", "sécurité, permissions, slugs et QR", GREEN)

    footer_tags(draw, [
        ("React 19", BLUE), ("Express 5", CYAN), ("MongoDB + MySQL", PURPLE),
        ("Stripe", YELLOW), ("Docker / Nginx", ORANGE),
    ])
    save(image, "eventflow-overview.png")


def generate_architecture() -> None:
    image, draw = base(
        "Architecture — du navigateur aux services métier",
        "Nginx expose une origine unique et l’API Express orchestre persistance, paiement et billets",
        "ARCHITECTURE",
        40,
    )

    tech_node(draw, (70, 250, 330, 455), "React 19 / Vite", "SPA responsive\nReact Router\nAuthContext + ProtectedRoute", BLUE, "UI")
    tech_node(draw, (405, 250, 665, 455), "Nginx", "Bundle statique\nFallback SPA\nReverse proxy /api", ORANGE, "NX")
    tech_node(draw, (740, 220, 1035, 485), "Express 5", "Routes → contrôleurs → services\nRepositories · modèles · Zod\nJWT · RBAC · Helmet · rate limit", CYAN, "API")
    arrow(draw, (330, 352), (405, 352), BLUE)
    arrow(draw, (665, 352), (740, 352), CYAN)

    services = [
        ((70, 565, 350, 705), "MySQL 8.4", "Sites relationnels\nRequêtes paramétrées", YELLOW, "SQL"),
        ((405, 565, 685, 705), "MongoDB 8", "Users · events\nOrders · tickets", GREEN, "MDB"),
        ((740, 565, 1020, 705), "Stripe", "Checkout Sessions\nWebhook signé", PURPLE, "PAY"),
        ((1075, 565, 1330, 705), "QR sécurisé", "UUID + HMAC\nUsage unique", RED, "QR"),
    ]
    for box, title, body, color, label in services:
        tech_node(draw, box, title, body, color, label, 14)

    # API to services bus.
    draw.line((887, 485, 887, 525), fill=CYAN, width=4)
    draw.line((210, 525, 1202, 525), fill=BORDER, width=3)
    for x, color in ((210, YELLOW), (545, GREEN), (880, PURPLE), (1202, RED)):
        arrow(draw, (x, 525), (x, 565), color, 3)

    rounded(draw, (1080, 210, 1330, 470), radius=24, fill=PANEL, outline=BORDER)
    draw.text((1107, 240), "Principes", font=font(20, "semibold"), fill=TEXT)
    principles = [
        ("1", "Responsabilités séparées", CYAN),
        ("2", "Stockage encapsulé", GREEN),
        ("3", "Sécurité par middleware", PURPLE),
        ("4", "Services remplaçables", YELLOW),
        ("5", "Démarrage vérifiable", BLUE),
    ]
    y = 286
    for number, label, color in principles:
        draw.ellipse((1110, y + 3, 1132, y + 25), fill=color)
        draw.text((1117, y + 7), number, font=font(10, "bold"), fill=BG)
        draw.text((1145, y), label, font=font(15, "medium"), fill=MUTED)
        y += 37

    footer_tags(draw, [("SPA", BLUE), ("Reverse proxy", ORANGE), ("API REST", CYAN), ("Persistance polyglotte", GREEN), ("Paiement", PURPLE)])
    save(image, "eventflow-architecture.png")


def journey_column(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], number: str, title: str, subtitle: str, steps: list[str], color: tuple[int, int, int]) -> None:
    x0, y0, x1, y1 = box
    rounded(draw, box, radius=26, fill=PANEL_ALT, outline=color, width=2)
    draw.rounded_rectangle((x0 + 24, y0 + 24, x0 + 70, y0 + 70), radius=12, fill=color)
    draw.text((x0 + 37, y0 + 38), number, font=font(13, "bold"), fill=BG)
    draw.text((x0 + 88, y0 + 21), title, font=font(24, "bold"), fill=TEXT)
    draw.text((x0 + 88, y0 + 52), subtitle, font=font(14), fill=MUTED)
    y = y0 + 120
    for index, step in enumerate(steps, 1):
        draw.ellipse((x0 + 28, y + 2, x0 + 52, y + 26), fill=PANEL, outline=color, width=2)
        draw.text((x0 + 36, y + 7), str(index), font=font(10, "bold"), fill=color)
        paragraph(draw, (x0 + 70, y), step, font(16), TEXT, x1 - x0 - 100, 4, 2)
        if index < len(steps):
            draw.line((x0 + 40, y + 29, x0 + 40, y + 67), fill=BORDER, width=2)
        y += 74


def generate_user_journeys() -> None:
    image, draw = base(
        "Trois parcours — une même plateforme",
        "L’interface et l’API adaptent leurs données et leurs autorisations au contexte utilisateur",
        "EXPÉRIENCE",
        42,
    )
    journey_column(draw, (70, 180, 470, 720), "01", "Visiteur", "Découverte publique", [
        "Parcourir et rechercher les événements publiés.",
        "Ouvrir une fiche détaillée et consulter les disponibilités.",
        "Être redirigé vers la connexion au moment d’acheter.",
        "Conserver une expérience responsive et accessible."
    ], BLUE)
    journey_column(draw, (500, 180, 900, 720), "02", "Utilisateur", "Réservation et billets", [
        "Créer un compte et restaurer la session avec /auth/me.",
        "Réserver jusqu’à dix places sans dépasser la capacité.",
        "Payer via Stripe ou utiliser le mode mock local.",
        "Retrouver chaque billet et afficher son QR signé."
    ], CYAN)
    journey_column(draw, (930, 180, 1330, 720), "03", "Administrateur", "Pilotage et contrôle", [
        "Gérer sites MySQL et événements MongoDB.",
        "Modifier les rôles sans supprimer le dernier administrateur.",
        "Vérifier un QR, puis consommer le billet si autorisé.",
        "Consulter les indicateurs et le chiffre d’affaires."
    ], PURPLE)
    footer_tags(draw, [("Catalogue", BLUE), ("Authentification", CYAN), ("Paiement", YELLOW), ("Billetterie", RED), ("Administration", PURPLE)])
    save(image, "eventflow-user-journeys.png")


def step_box(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], number: str, title: str, body: str, color: tuple[int, int, int]) -> None:
    x0, y0, x1, y1 = box
    rounded(draw, box, radius=22, fill=PANEL_ALT, outline=color, width=2)
    draw.rounded_rectangle((x0 + 18, y0 + 18, x0 + 60, y0 + 60), radius=11, fill=color)
    draw.text((x0 + 30, y0 + 31), number, font=font(12, "bold"), fill=BG)
    draw.text((x0 + 77, y0 + 20), title, font=font(18, "semibold"), fill=TEXT)
    paragraph(draw, (x0 + 22, y0 + 80), body, font(14), MUTED, x1 - x0 - 44, 5, 4)


def generate_payment_flow() -> None:
    image, draw = base(
        "Paiement — réservation atomique et finalisation idempotente",
        "Le stock est réservé avant le checkout puis engagé une seule fois après confirmation",
        "TRANSACTION",
        39,
    )

    boxes = [
        ((70, 245, 302, 465), "01", "Demande", "Event + quantité\nUtilisateur authentifié", BLUE),
        ((330, 245, 562, 465), "02", "Réservation", "findOneAndUpdate\n$expr + $inc\nticketsReserved", CYAN),
        ((590, 245, 822, 465), "03", "Checkout", "Stripe Session\nou mode mock", PURPLE),
        ((850, 245, 1082, 465), "04", "Finalisation", "paymentFinalizing\nétats idempotents", YELLOW),
        ((1110, 245, 1330, 465), "05", "Billets", "upsert + index unique\n(order, sequence)", GREEN),
    ]
    for box, number, title, body, color in boxes:
        step_box(draw, box, number, title, body, color)
    for left, right in zip(boxes, boxes[1:]):
        arrow(draw, (left[0][2], 355), (right[0][0], 355), CYAN, 3)

    rounded(draw, (70, 530, 665, 708), radius=24, fill=PANEL, outline=RED, width=2)
    draw.text((102, 562), "Échec, expiration ou abandon", font=font(21, "semibold"), fill=RED)
    paragraph(draw, (102, 604), "La commande conserve son état ; reservationReleased empêche une double restitution et $inc remet les places réservées dans l’inventaire disponible.", font(16), MUTED, 525, 6, 3)

    rounded(draw, (700, 530, 1330, 708), radius=24, fill=PANEL, outline=CYAN, width=2)
    draw.text((732, 562), "Garanties contre les doublons", font=font(21, "semibold"), fill=CYAN)
    guarantees = [
        "paymentFinalizing verrouille la transition métier",
        "inventoryCommitted protège l’engagement du stock",
        "ticketsIssued documente l’émission",
        "index (order, sequence) bloque les billets dupliqués",
    ]
    y = 608
    for item in guarantees:
        draw.ellipse((734, y + 7, 742, y + 15), fill=CYAN)
        draw.text((754, y), item, font=font(15), fill=MUTED)
        y += 28

    footer_tags(draw, [("Concurrence", CYAN), ("Idempotence", YELLOW), ("Stripe Webhooks", PURPLE), ("Inventaire", BLUE), ("Index unique", GREEN)])
    save(image, "eventflow-payment-flow.png")


def generate_ticket_security() -> None:
    image, draw = base(
        "Billetterie QR — authentique, vérifiable et à usage unique",
        "Une signature HMAC protège le payload ; une écriture conditionnelle empêche la double consommation",
        "SÉCURITÉ",
        39,
    )

    # QR-like decorative matrix.
    rounded(draw, (70, 190, 470, 690), radius=28, fill=PANEL_ALT, outline=CYAN, width=2)
    draw.text((108, 222), "Payload versionné", font=font(22, "semibold"), fill=TEXT)
    draw.text((108, 258), '{ "v": 1, "code": "UUID", ... }', font=font(17, "medium"), fill=CYAN)
    cell = 14
    origin_x, origin_y = 140, 330
    matrix = [
        "111111101011111111",
        "100000101010000001",
        "101110101110111101",
        "101110100010111101",
        "101110101010111101",
        "100000100010000001",
        "111111101011111111",
        "000000001000000000",
        "101101111011011010",
        "010011001100110101",
        "111010111011101110",
        "001100010110001001",
        "111111101011101110",
        "100000101100111001",
        "101110101011010110",
        "101110100110101001",
        "100000101011011110",
        "111111101100100101",
    ]
    for row, bits in enumerate(matrix):
        for col, bit in enumerate(bits):
            if bit == "1":
                draw.rectangle((origin_x + col * cell, origin_y + row * cell, origin_x + (col + 1) * cell - 2, origin_y + (row + 1) * cell - 2), fill=TEXT)
    draw.text((108, 625), "QR = données + signature", font=font(18, "semibold"), fill=TEXT)
    draw.text((108, 654), "Aucun secret n’est embarqué.", font=font(14), fill=MUTED)

    stages = [
        ((525, 190, 885, 315), "01", "UUID imprévisible", "Identifie le billet sans exposer un numéro séquentiel.", BLUE),
        ((925, 190, 1330, 315), "02", "HMAC SHA-256", "Signe exactement le payload avec un secret serveur.", PURPLE),
        ((525, 365, 885, 490), "03", "timingSafeEqual", "Compare les signatures à temps constant après validation du format.", YELLOW),
        ((925, 365, 1330, 490), "04", "Recherche du billet", "Contrôle propriétaire, événement, statut et cohérence du code.", CYAN),
        ((525, 540, 885, 690), "05", "Transition atomique", "findOneAndUpdate exige status = valid avant de passer à used.", GREEN),
        ((925, 540, 1330, 690), "06", "Audit du contrôle", "Le serveur conserve usedAt et l’administrateur qui a consommé le billet.", RED),
    ]
    for box, number, title, body, color in stages:
        step_box(draw, box, number, title, body, color)
    arrow(draw, (885, 252), (925, 252), CYAN, 3)
    arrow(draw, (1127, 315), (1127, 365), CYAN, 3)
    arrow(draw, (925, 427), (885, 427), CYAN, 3)
    arrow(draw, (705, 490), (705, 540), CYAN, 3)
    arrow(draw, (885, 615), (925, 615), CYAN, 3)

    footer_tags(draw, [("UUID", BLUE), ("HMAC SHA-256", PURPLE), ("Comparaison constante", YELLOW), ("Usage unique", GREEN), ("Traçabilité", RED)])
    save(image, "eventflow-ticket-security.png")


def storage_card(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], title: str, subtitle: str, items: list[str], color: tuple[int, int, int], icon_label: str) -> None:
    x0, y0, x1, y1 = box
    rounded(draw, box, radius=28, fill=PANEL_ALT, outline=color, width=2)
    small_icon(draw, (x0 + 58, y0 + 60), icon_label, color)
    draw.text((x0 + 100, y0 + 28), title, font=font(27, "bold"), fill=TEXT)
    draw.text((x0 + 100, y0 + 63), subtitle, font=font(14), fill=MUTED)
    y = y0 + 135
    for item in items:
        draw.rounded_rectangle((x0 + 32, y, x1 - 32, y + 54), radius=14, fill=PANEL, outline=BORDER)
        draw.ellipse((x0 + 52, y + 22, x0 + 62, y + 32), fill=color)
        draw.text((x0 + 78, y + 15), item, font=font(16, "medium"), fill=TEXT)
        y += 68


def generate_polyglot_storage() -> None:
    image, draw = base(
        "Persistance polyglotte et orchestration Docker",
        "Chaque moteur sert un besoin précis, derrière une couche d’accès dédiée et vérifiable",
        "DATA + OPS",
        41,
    )

    storage_card(draw, (70, 185, 525, 670), "MySQL 8.4", "Données relationnelles et CRUD paramétré", [
        "sites — identifiants et contenu structuré",
        "siteRepository.js — isolation du SQL",
        "placeholders — protection contre l’injection",
        "init.sql — création reproductible du schéma",
    ], YELLOW, "SQL")

    storage_card(draw, (560, 185, 1015, 670), "MongoDB 8", "Domaine événementiel et documents métier", [
        "users — comptes, mots de passe et rôles",
        "events — capacité, réservations et ventes",
        "orders — états de paiement et inventaire",
        "tickets — UUID, signature, statut et index",
    ], GREEN, "MDB")

    rounded(draw, (1050, 185, 1330, 670), radius=28, fill=PANEL, outline=CYAN, width=2)
    draw.text((1080, 218), "Docker Compose", font=font(23, "bold"), fill=TEXT)
    services = [
        ("client", "React + Nginx", BLUE),
        ("server", "Express 5", CYAN),
        ("mysql", "volume persistant", YELLOW),
        ("mongo", "volume persistant", GREEN),
    ]
    y = 276
    for title, detail, color in services:
        draw.rounded_rectangle((1080, y, 1300, y + 68), radius=16, fill=PANEL_ALT, outline=color)
        draw.ellipse((1098, y + 25, 1116, y + 43), fill=color)
        draw.text((1130, y + 10), title, font=font(17, "semibold"), fill=TEXT)
        draw.text((1130, y + 36), detail, font=font(13), fill=MUTED)
        y += 82
    draw.text((1080, 615), "healthchecks + service_healthy", font=font(14, "medium"), fill=CYAN)

    rounded(draw, (310, 700, 1090, 756), radius=18, fill=PANEL, outline=BORDER)
    draw.text((338, 717), "Validation fournie : 8 tests Node et contrôle syntaxique de 39 fichiers serveur. Intégration Docker à rejouer sur une machine équipée.", font=font(15, "medium"), fill=TEXT)
    save(image, "eventflow-polyglot-storage.png")


def main() -> None:
    generate_overview()
    generate_architecture()
    generate_user_journeys()
    generate_payment_flow()
    generate_ticket_security()
    generate_polyglot_storage()
    print(f"Generated 6 EventFlow visuals in {OUT}")


if __name__ == "__main__":
    main()
