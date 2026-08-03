import customtkinter as ctk

LIGHT = {
    "bg": "#F5F5F5",
    "panel": "#FFFFFF",
    "section_bg": "#FAFAFA",
    "text": "#1A1A1A",
    "muted": "#6B7280",
    "border": "#E0E0E0",
    "accent": "#534AB7",
    "accent_hover": "#453E9E",
    "accent_soft": "#E3E7F6",
    "canvas_bg": "#FFFFFF",
    "canvas_edge": "#3A3F55",
    "canvas_fill": "#E3E7F6",
    "entry_bg": "#FFFFFF",
    "error": "#C0392B",
    "error_soft": "#F8E1E4",
    "success": "#2E7D6B",
}

DARK = {
    "bg": "#1C1C1E",
    "panel": "#2C2C2E",
    "section_bg": "#232325",
    "text": "#F0F0F0",
    "muted": "#9A9AA0",
    "border": "#3A3A3C",
    "accent": "#534AB7",
    "accent_hover": "#6359C9",
    "accent_soft": "#3A3558",
    "canvas_bg": "#1C1C1E",
    "canvas_edge": "#C5C7D0",
    "canvas_fill": "#33344A",
    "entry_bg": "#3A3A3C",
    "error": "#E85C66",
    "error_soft": "#4A2A2E",
    "success": "#5BBFA7",
}


class ThemeManager:
    def __init__(self):
        self.mode = "light"
        self.palette = dict(LIGHT)
        self._listeners = []

    def set_mode(self, mode):
        self.mode = mode if mode in ("light", "dark") else "light"
        self.palette = dict(DARK if self.mode == "dark" else LIGHT)
        ctk.set_appearance_mode(self.mode)
        for callback in list(self._listeners):
            callback()

    def register(self, callback):
        if callback not in self._listeners:
            self._listeners.append(callback)
        return callback


theme = ThemeManager()


def t(key):
    return theme.palette[key]
