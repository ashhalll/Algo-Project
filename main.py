import customtkinter as ctk
import math
import time
from tkinter import filedialog, messagebox


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Algo Project Part 2")
        self.geometry("1200x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=7)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#2B2B2B")
        self.sidebar_frame.grid(row=0, column=0, sticky="nswe")

        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="Algorithms Project Part 2",
            font=ctk.CTkFont(family="Helvetica", size=25, weight="bold"),
            text_color="white",
        )
        self.logo_label.pack(pady=(150, 10), padx=10)

        self.group_labels = [
            "22k-4419",
            "22k-4306",
            "22k-4481",
        ]
        for member in self.group_labels:
            label = ctk.CTkLabel(
                self.sidebar_frame,
                text=member,
                font=ctk.CTkFont(family="Helvetica", size=16),
                text_color="white",
            )
            label.pack(pady=5)

        # Main Content Area (70%)
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#1A1A1A")
        self.main_frame.grid(row=0, column=1, sticky="nswe")

        # Main buttons in implementation area
        self.main_button_5 = ctk.CTkButton(
            self.main_frame,
            text="Closest Pair Algorithm",
            command=self.run_closest_pair,
            height=40,
            width=200,
            fg_color="purple",
            hover_color="maroon"
        )
        self.main_button_5.pack(pady=14)

        # Canvas for visualization
        self.canvas = ctk.CTkCanvas(self.main_frame, width=1000, height=600, bg="white")
        self.canvas.pack(pady=10)

        self.main_button_6 = ctk.CTkButton(
            self.main_frame,
            text="Integer Multiplication",
            command=self.run_karatsuba,
            height=40,
            width=200,
            fg_color="purple",
            hover_color="maroon"
        )
        self.main_button_6.pack(pady=25)

        # Output label
        self.output_text = ctk.StringVar()
        self.output_label = ctk.CTkLabel(
            self.main_frame,
            textvariable=self.output_text,
            wraplength=600,
            text_color="white",
            font=ctk.CTkFont(size=14),
        )
        self.output_label.pack(pady=10)

        self.points = []

    # Closest Pair Algorithm
    def load_points(self, filename):
        with open(filename, "r") as f:
            self.points = [tuple(map(int, line.strip().split())) for line in f]
            self.canvas.delete("all")  # Clear canvas before plotting new points
            for (x, y) in self.points:
                self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="blue")
            return self.points

    def distance(self, p1, p2):
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    def brute_force(self, points):
        min_dist = float("inf")
        closest_pair = None
        n = len(points)
        for i in range(n):
            for j in range(i + 1, n):
                d = self.distance(points[i], points[j])
                if d < min_dist:
                    min_dist = d
                    closest_pair = (points[i], points[j])
        if closest_pair is not None:
            return closest_pair[0], closest_pair[1], min_dist
        else:
            raise ValueError(
                "No closest pair found. Check input data for correctness."
            )

    def closest_pair_recursive(self, points_sorted_x, points_sorted_y):
        n = len(points_sorted_x)
        if n <= 3:
            return self.brute_force(points_sorted_x)

        mid = n // 2
        midpoint = points_sorted_x[mid][0]

        self.canvas.delete("midline")
        self.canvas.create_line(midpoint, 0, midpoint, 500, fill="gray", dash=(4, 2), tags="midline")
        self.update()
        time.sleep(0.1)

        left_x, right_x = points_sorted_x[:mid], points_sorted_x[mid:]
        left_y = list(filter(lambda p: p[0] <= midpoint, points_sorted_y))
        right_y = list(filter(lambda p: p[0] > midpoint, points_sorted_y))

        (p1, q1, d1) = self.closest_pair_recursive(left_x, left_y)
        (p2, q2, d2) = self.closest_pair_recursive(right_x, right_y)

        min_dist, closest_pair = (d1, (p1, q1)) if d1 < d2 else (d2, (p2, q2))

        in_strip = [p for p in points_sorted_y if abs(p[0] - midpoint) < min_dist]

        for i in range(len(in_strip)):
            for j in range(i + 1, min(i + 7, len(in_strip))):
                p, q = in_strip[i], in_strip[j]
                d = self.distance(p, q)
                if d < min_dist:
                    min_dist, closest_pair = d, (p, q)
                    self.canvas.delete("pair")
                    self.canvas.create_line(
                        p[0], p[1], q[0], q[1], fill="red", width=2, tags="pair"
                    )
                    self.update()
                    time.sleep(0.5)

        return closest_pair[0], closest_pair[1], min_dist

    def closest_pair_of_points(self):
        points_sorted_x = sorted(self.points, key=lambda p: p[0])
        points_sorted_y = sorted(self.points, key=lambda p: p[1])
        return self.closest_pair_recursive(points_sorted_x, points_sorted_y)

    def run_closest_pair(self):
        try:
            file_path = filedialog.askopenfilename()
            if file_path:
                self.points = self.load_points(file_path)
                result = self.closest_pair_of_points()
                self.canvas.delete("pair")
                self.canvas.delete("midline")
                self.output_text.set(
                    f"Closest Pair: ({result[0][0]}, {result[0][1]}) and ({result[1][0]}, {result[1][1]})\nDistance: {result[2]:.4f}"
                )
        except Exception as e:
            self.output_text.set(f"Error: {str(e)}")

    def karatsuba(self, x, y):
        if x < 10 or y < 10:
            return x * y
        n = max(len(str(x)), len(str(y)))
        m = n // 2

        high1, low1 = divmod(x, 10**m)
        high2, low2 = divmod(y, 10**m)

        z0 = self.karatsuba(low1, low2)
        z1 = self.karatsuba((low1 + high1), (low2 + high2))
        z2 = self.karatsuba(high1, high2)

        return (z2 * 10**(2 * m)) + ((z1 - z2 - z0) * 10**m) + z0

    def run_karatsuba(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                with open(file_path, "r") as f:
                    x, y = map(int, f.readline().strip().split())
                result = self.karatsuba(x, y)
                self.output_text.set(f"Product: {result}")
            except Exception as e:
                self.output_text.set(f"Error: {str(e)}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
