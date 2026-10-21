#!/usr/bin/env python3
"""
Live mouse coordinate display in a small always-on-top window.

Part of the mouse_coordinates/ example. See README.txt for details.

Usage:
    python mouse.py

Requires:
    pip install pyautogui

Runs until the window is closed (click on it, or right-click the
left-side drag handle).
"""
import sys

try:
    import pyautogui
except ImportError as e:
    print("[FAIL] Missing dependency: " + str(e))
    print("       Run: pip install pyautogui")
    sys.exit(1)

import tkinter as tk
import threading
import time

class MouseCoordinates:
    def __init__(self):
        self.running = True
        self.dragging = False
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.window_x = 0
        self.window_y = 0

        self.root = tk.Tk()
        self.root.title("Mouse Coordinates")
        self.root.geometry("220x30")
        self.root.attributes('-topmost', True)
        self.root.overrideredirect(True)
        self.root.configure(bg='black')

        screen_width = self.root.winfo_screenwidth()
        self.root.geometry("220x30+" + str(screen_width - 230) + "+5")

        main_frame = tk.Frame(self.root, bg='black')
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.handle = tk.Label(
            main_frame,
            text="::",
            font=("Arial", 10, "bold"),
            fg="lime",
            bg="#333333",
            padx=4,
            pady=2,
            cursor="fleur"
        )
        self.handle.pack(side=tk.LEFT, fill=tk.Y)
        self.handle.bind('<Button-1>', self.start_drag)
        self.handle.bind('<B1-Motion>', self.on_drag)
        self.handle.bind('<Double-Button-1>', self.reset_position)
        self.handle.bind('<Button-3>', self.toggle_close)

        self.label = tk.Label(
            main_frame,
            text="X: 0, Y: 0",
            font=("Consolas", 12, "bold"),
            fg="lime",
            bg="black",
            padx=10,
            pady=2
        )
        self.label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.label.bind('<Button-1>', self.toggle_close)
        self.label.bind('<Button-3>', self.toggle_close)

        self.update_coords()
        self.root.mainloop()

    def start_drag(self, event):
        self.dragging = True
        self.drag_start_x = event.x_root
        self.drag_start_y = event.y_root
        self.window_x = self.root.winfo_x()
        self.window_y = self.root.winfo_y()
        self.handle.config(bg="#444444")

    def on_drag(self, event):
        if self.dragging:
            dx = event.x_root - self.drag_start_x
            dy = event.y_root - self.drag_start_y
            new_x = self.window_x + dx
            new_y = self.window_y + dy
            self.root.geometry("+" + str(new_x) + "+" + str(new_y))

    def reset_position(self, event):
        screen_width = self.root.winfo_screenwidth()
        self.root.geometry("220x30+" + str(screen_width - 230) + "+5")
        self.handle.config(bg="#333333")

    def update_coords(self):
        if self.running:
            try:
                x, y = pyautogui.position()
                self.label.config(text="X: " + str(x).rjust(4) + "  Y: " + str(y).rjust(4))
            except Exception:
                pass
            self.root.after(50, self.update_coords)

    def toggle_close(self, event):
        self.running = False
        self.root.destroy()

if __name__ == '__main__':
    print("")
    print("=" * 50)
    print("MOUSE COORDINATES")
    print("=" * 50)
    print("A small window will appear in the top-right corner")
    print("showing the current mouse position.")
    print("")
    print("Drag the left handle to move the window.")
    print("Double-click the handle to reset to top-right.")
    print("Click anywhere on the window to close it.")
    print("=" * 50)
    print("")
    MouseCoordinates()
