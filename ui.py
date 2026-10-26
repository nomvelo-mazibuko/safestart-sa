"""Colours and small building blocks shared by every screen."""
import flet as ft

# ---------- Colours ----------
TEAL = "#0F4C5C"
INK = "#1B2A30"
MUTED = "#5B6B71"
BACKGROUND = "#F2F6F7"
WHITE = "#FFFFFF"
RED = "#B3261E"
AMBER = "#8A5200"   # darker than before so it is easier to read on white
GREEN = "#2E7D32"


def make_card(content, border_color="#D9E2E5"):
    """A white box with a thin border."""
    return ft.Container(
        content=content,
        bgcolor=WHITE,
        padding=16,
        border_radius=10,
        border=ft.Border.all(1, border_color),
    )


def make_heading(text):
    return ft.Text(text, size=24, weight=ft.FontWeight.BOLD, color=INK)


def make_section_title(text):
    return ft.Text(text, size=18, weight=ft.FontWeight.W_600, color=TEAL)


def make_text(text, color=INK, size=15):
    return ft.Text(text, size=size, color=color)


def make_help_row(name, description, web_address):
    """A tappable row that opens a website."""
    async def open_website(e):
        await ft.UrlLauncher().launch_url(web_address)

    return ft.ListTile(
        title=ft.Text(name, weight=ft.FontWeight.W_600, color=INK),
        subtitle=ft.Text(description, color=MUTED),
        trailing=ft.Icon(ft.Icons.OPEN_IN_NEW, color=TEAL),
        on_click=open_website,
    )
