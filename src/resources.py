"""
Miscellaneous functions for displaying things

Textboxes required:
- Velocity direction display (with magnitude)
- Mesh dimensions clearly labeled
- FPS and performance details
- "ESC to exit" text
- Title

Should work on the principle of dependency injection, where it is
agnostic to the particular pygame "surface" object it is sent.
"""

from typing import Tuple, List
import os
import pygame

FG = (0, 0, 0)
BG = (255, 255, 255)

pygame.font.init()
font = pygame.font.Font(os.path.join("res", "fonts", "JetBrainsMono-Regular.ttf"), 20)
font_para = pygame.font.Font(os.path.join("res", "fonts", "JetBrainsMono-Regular.ttf"), 16)


def paragraph(
    color: Tuple[int, int, int],
    paragraph: str,
) -> pygame.Surface:
    lines: List[str] = paragraph.split("\n")
    margin: int = 5
    line_surfaces: List[pygame.Surface] = []
    max_width: int = 0

    for i in range(len(lines)):
        line_surface: pygame.Surface = font_para.render(lines[i], True, color)
        line_surfaces.append(line_surface)
        if line_surface.get_width() > max_width:
            max_width = line_surface.get_width()

    paragraph_surface = pygame.Surface(
        (
            max_width,
            len(line_surfaces) * line_surfaces[0].get_height()
            + margin * (len(line_surfaces) - 1),
        )
    )
    paragraph_surface.fill(BG)

    for i in range(len(lines)):
        y = 0 + i * line_surfaces[i].get_height()
        if y != 0:
            y += i * margin

        paragraph_surface.blit(line_surfaces[i], (2, y))

    return paragraph_surface


def border(
    surface: pygame.Surface,
    pos: Tuple[int, int],
    rect: Tuple[int, int],
    title: str = "",
) -> None:
    thickness = 2
    pygame.draw.lines(
        surface,
        FG,
        True,
        [
            (pos[0], pos[1]),
            (pos[0] + rect[0], pos[1]),
            (pos[0] + rect[0], pos[1] + rect[1]),
            (pos[0], pos[1] + rect[1]),
        ],
        thickness,
    )

    # put title on top of border
    title_surface = font.render(title, True, FG, BG)
    surface.blit(
        title_surface,
        (pos[0] + 20, pos[1] + thickness - title_surface.get_height()),
    )


def textbox_width(
    surface: pygame.Surface,
    pos: Tuple[int, int],
    width: int,
    text: str,
    title: str = "",
) -> None:
    paragraph_surface = paragraph(FG, text)

    height = paragraph_surface.get_height()
    textbox_surface = pygame.Surface((width, height))
    textbox_surface.fill(BG)
    textbox_surface.blit(paragraph_surface, (0, 0))

    surface.blit(textbox_surface, pos)

    mw = 2  # markerwidth
    pygame.draw.lines(
        surface,
        FG,
        True,
        [
            (pos[0] - mw / 2, pos[1] - mw / 2),
            (pos[0] + width + mw / 2, pos[1] - mw / 2),
            (pos[0] + width + mw / 2, pos[1] + height + mw / 2),
            (pos[0] - mw / 2, pos[1] + height + mw / 2),
        ],
        mw,
    )

    # put title on top of border
    title_surface = font.render(title, True, FG, BG)
    surface.blit(
        title_surface,
        (pos[0] + 20, pos[1] + mw - title_surface.get_height()),
    )
