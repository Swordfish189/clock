import tkinter as tk
import time


class TransparentClock(tk.Tk):
    def __init__(self):
        super().__init__()

        # Remove window border and title bar
        self.overrideredirect(True)

        # Keep the window always on top
        self.wm_attributes("-topmost", True)

        # Set the window background color (the same color used for transparency)
        self.config(bg="black")

        # Make the chosen background color transparent
        self.wm_attributes("-transparentcolor", "black")

        # Create a label to display the clock
        self.label = tk.Label(
            self,
            text="",
            font=("Consolas", 20),  # "Courier New", "Lucida Console", etc.
            fg="lime",  # Hacker green color
            bg="black",  # Must match the window's background for transparency
        )
        self.label.pack()

        # Enable dragging the window by clicking on the label
        self.label.bind("<Button-1>", self.start_move)
        self.label.bind("<B1-Motion>", self.do_move)

        # Start updating the clock
        self.update_clock()

    def update_clock(self):
        """Update the clock label every second."""
        current_time = time.strftime("%H:%M:%S")
        self.label.config(text=current_time)
        self.after(1000, self.update_clock)

    def start_move(self, event):
        """Remember the offset when a left-click starts."""
        self.click_x = event.x
        self.click_y = event.y

    def do_move(self, event):
        """Move the window based on mouse drag."""
        x = self.winfo_pointerx() - self.click_x
        y = self.winfo_pointery() - self.click_y
        self.geometry(f"+{x}+{y}")


if __name__ == "__main__":
    TransparentClock().mainloop()
