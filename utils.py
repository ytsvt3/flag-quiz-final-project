import os
import pygame
import requests
from PIL import Image

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets", "flags")

BG_COLOR        = (70,  23,  143)
HEADER_COLOR    = (26,  26,  46)
WHITE           = (255, 255, 255)
BLACK           = (0,   0,   0)
GRAY            = (180, 180, 180)
DARK_GRAY       = (60,  60,  60)
GREEN_FLASH     = (0,   200, 100)
RED_FLASH       = (220, 50,  50)
TIMER_GREEN     = (0,   230, 118)
TIMER_ORANGE    = (255, 165, 0)
TIMER_RED       = (220, 50,  50)

ANSWER_COLORS = [
    (226, 27,  60),
    (25,  118, 210),
    (253, 216, 53),
    (43,  163, 90),
]

ANSWER_HOVER_COLORS = [
    (200, 20,  50),
    (20,  100, 190),
    (230, 195, 40),
    (35,  140, 75),
]

ANSWER_ICONS = ["▲", "◆", "●", "■"]


def get_font(size, bold=False):
    fonts = ["Arial", "Helvetica", "DejaVu Sans", "Liberation Sans"]
    for name in fonts:
        try:
            return pygame.font.SysFont(name, size, bold=bold)
        except Exception:
            continue
    return pygame.font.Font(None, size)


def load_flag(country_code: str):
    path = os.path.join(ASSETS_DIR, f"{country_code}.png")
    if not os.path.exists(path):
        _download_flag(country_code, path)
    if os.path.exists(path):
        try:
            img = Image.open(path).convert("RGBA")
            img = img.resize((320, 200), Image.LANCZOS)
            data = img.tobytes()
            return pygame.image.fromstring(data, img.size, "RGBA")
        except Exception:
            return None
    return None


def _download_flag(code: str, dest: str):
    url = f"https://flagcdn.com/w320/{code}.png"
    try:
        r = requests.get(url, timeout=8)
        if r.status_code == 200:
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(dest, "wb") as f:
                f.write(r.content)
    except Exception:
        pass


def draw_text_centered(surface, text, font, color, center_x, center_y):
    rendered = font.render(text, True, color)
    rect = rendered.get_rect(center=(center_x, center_y))
    surface.blit(rendered, rect)
    return rect


def draw_rounded_rect(surface, color, rect, radius=12):
    pygame.draw.rect(surface, color, rect, border_radius=radius)


def timer_color(fraction: float) -> tuple:
    if fraction > 0.5:
        return TIMER_GREEN
    elif fraction > 0.25:
        return TIMER_ORANGE
    return TIMER_RED
