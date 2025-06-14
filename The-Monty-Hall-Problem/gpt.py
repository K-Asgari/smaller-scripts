import tkinter as tk
import ttkbootstrap as ttk
import random
import threading
import pygame
import time

class MontyHallSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Monty Hall Problem Simulator")

        # Init sound system
        pygame.mixer.init()
        self.sounds = {
            "reveal": pygame.mixer.Sound("reveal.wav"),
            "win": pygame.mixer.Sound("win.wav"),
            "lose": pygame.mixer.Sound("lose.wav"),
        }

        self.door_options = ["🐐", "🐐", "🚗"]
        self.doors_list = []
        self.doors_map = {}

        self.correct_guesses_stay = 0
        self.correct_guesses_switch = 0
        self.total_switches = 0
        self.total_stays = 0

        self.create_widgets()
        self.new_game()

    def create_widgets(self):
        self.main_frame = ttk.Frame(self.root, padding=20)
        self.main_frame.pack(fill="both", expand=True)

        self.doors_frame = ttk.Frame(self.main_frame)
        self.doors_frame.pack(pady=20)

        for button_index in range(3):
            door = ttk.Button(
                self.doors_frame,
                text="❓",
                bootstyle="secondary outline",
                width=10,
                command=lambda i=button_index: self.door_clicked(i),
            )
            door.grid(row=0, column=button_index, padx=20)
            self.doors_list.append(door)

        self.controls_frame = ttk.Frame(self.main_frame)
        self.controls_frame.pack(pady=10)

        self.switch_button = ttk.Button(self.controls_frame, text="Switch", command=self.switch, state="disabled")
        self.stay_button = ttk.Button(self.controls_frame, text="Stay", command=self.stay, state="disabled")
        self.play_again_button = ttk.Button(self.controls_frame, text="Play Again", command=self.new_game)
        self.simulate_button = ttk.Button(self.controls_frame, text="Simulate 1000", command=self.simulate)

        self.switch_button.grid(row=0, column=0, padx=10)
        self.stay_button.grid(row=0, column=1, padx=10)
        self.play_again_button.grid(row=0, column=2, padx=10)
        self.simulate_button.grid(row=0, column=3, padx=10)

        self.score_label = ttk.Label(self.main_frame, text="", font=("Helvetica", 14))
        self.score_label.pack(pady=10)

    def door_clicked(self, index):
        self.highlight_door(index, "warning outline")
        self.doors_map["picked"] = index

        for btn in self.doors_list:
            btn.config(state="disabled")

        self.root.after(500, self.reveal_goat)

    def reveal_goat(self):
        for i in range(3):
            if i != self.doors_map["picked"] and self.door_options[i] == "🐐":
                self.animate_reveal(i)
                self.doors_map["revealed"] = i
                break

        self.switch_button.config(state="normal")
        self.stay_button.config(state="normal")

    def animate_reveal(self, index):
        def reveal_sequence():
            for frame in ["", ".", "..", "..."]:
                self.doors_list[index].config(text=frame)
                time.sleep(0.1)
            self.doors_list[index].config(text="🐐")
            self.sounds["reveal"].play()

        threading.Thread(target=reveal_sequence).start()

    def add_switch_door(self):
        for i in range(3):
            if i not in self.doors_map.values():
                self.doors_map["switch"] = i

    def switch(self):
        self.total_switches += 1
        self.add_switch_door()

        switch_index = self.doors_map["switch"]
        if self.door_options[switch_index] == "🚗":
            self.correct_guesses_switch += 1
            self.highlight_door(switch_index, "success")
            self.sounds["win"].play()
        else:
            self.highlight_door(switch_index, "danger")
            self.sounds["lose"].play()

        self.reveal_all()

    def stay(self):
        self.total_stays += 1
        self.add_switch_door()

        picked_index = self.doors_map["picked"]
        if self.door_options[picked_index] == "🚗":
            self.correct_guesses_stay += 1
            self.highlight_door(picked_index, "success")
            self.sounds["win"].play()
        else:
            self.highlight_door(picked_index, "danger")
            self.sounds["lose"].play()

        self.reveal_all()

    def reveal_all(self):
        for i, door in enumerate(self.doors_list):
            door.config(text=self.door_options[i])
        self.update_score()
        self.switch_button.config(state="disabled")
        self.stay_button.config(state="disabled")

    def update_score(self):
        stay_rate = (self.correct_guesses_stay / self.total_stays * 100) if self.total_stays else 0
        switch_rate = (self.correct_guesses_switch / self.total_switches * 100) if self.total_switches else 0

        self.score_label.config(
            text=f"Stays: {self.total_stays} | Stay win rate: {stay_rate:.1f}%\n"
                 f"Switches: {self.total_switches} | Switch win rate: {switch_rate:.1f}%"
        )

    def new_game(self):
        random.shuffle(self.door_options)
        self.doors_map.clear()
        for door in self.doors_list:
            door.config(text="❓", bootstyle="secondary outline", state="normal")
        self.switch_button.config(state="disabled")
        self.stay_button.config(state="disabled")

    def highlight_door(self, index, color):
        self.doors_list[index].config(bootstyle=color)

    def simulate(self):
        threading.Thread(target=self._simulate, daemon=True).start()

    def _simulate(self):
        for _ in range(1000):
            random.shuffle(self.door_options)
            picked = random.randint(0, 2)
            revealed = next(i for i in range(3) if i != picked and self.door_options[i] == "🐐")
            switch = next(i for i in range(3) if i != picked and i != revealed)

            if self.door_options[switch] == "🚗":
                self.correct_guesses_switch += 1
            self.total_switches += 1

            if self.door_options[picked] == "🚗":
                self.correct_guesses_stay += 1
            self.total_stays += 1

            if _ % 100 == 0:
                self.root.after(0, self.update_score)

        self.root.after(0, self.update_score)


if __name__ == "__main__":
    app = ttk.Window(themename="flatly", title="Monty Hall Simulator", size=(800, 500))
    MontyHallSimulator(app)
    app.mainloop()
