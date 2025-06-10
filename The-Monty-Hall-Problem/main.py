"""
May, 2022

Title: The Monty Hall Problem
Description:
    Simulator made with Tkinter

ToDo:
    BUG: goat-car-goat -> Pick stay on first goat, only in the first round.
    Some minor tweaking:
        Code cleanup
        Cosmetics
    

"""

import tkinter as tk
import random


root = tk.Tk()
root.geometry("700x500")

door_options = ["🐐", "🐐", "🚗"]
random.shuffle(door_options)
doors_list = []
doors_map = {}
correct_guesses_stay = 0
correct_guesses_switch = 0
total_switches = 0
total_stays = 0


def door_clicked(button_index):
    doors_list[button_index].configure(bg="yellow2")
    doors_map.update({"picked": button_index})

    for x in [switch_button, stay_button]:
        x.configure(state="normal")

    for door in doors_list:
        door.configure(state="disabled")

    for door in doors_list:
        if doors_list[button_index] == door:
            continue
        elif door_options[doors_list.index(door)] == "🐐":
            door.configure(text="🐐")
            doors_map.update({"revealed": doors_list.index(door)})
            break


for button_index in range(3):
    door = tk.Button(root,
                     text="",
                     height=10,
                     width=10,
                     font=("helvetic", 20),
                     command=lambda button_index=button_index: door_clicked(
                         button_index)
                     )

    door.grid(row=0, column=button_index)
    doors_list.append(door)


def play_again():
    random.shuffle(door_options)
    doors_map.clear()
    for door in doors_list:
        door.configure(text="", state="normal", bg="SystemButtonFace")
    play_again_button.pack_forget()
    


def add_switch_door():
    for x in range(3):
        if x not in doors_map.values():
            doors_map.update({"switch": x})


def switch():
    global correct_guesses_switch, total_switches
    total_switches +=1
    add_switch_door()
    if door_options[doors_map["switch"]] == "🐐":
        doors_list[doors_map["switch"]].configure(bg="red2")
    else:
        correct_guesses_switch += 1
        doors_list[doors_map["switch"]].configure(bg="green2")

    # Reveal
    for door in doors_list:
        door.configure(text=door_options[doors_list.index(door)])
    update_score()
    stay_button.configure(state="disabled")
    switch_button.configure(state="disabled")
    play_again_button.pack()


def stay():
    global correct_guesses_stay, total_stays
    total_stays += 1
    add_switch_door()
    if door_options[doors_map["picked"]] == "🐐":
        doors_list[doors_map["picked"]].configure(bg="red2")
    else:
        correct_guesses_stay += 1
        doors_list[doors_map["picked"]].configure(bg="green2")

    # Reveal
    for door in doors_list:
        door.configure(text=door_options[doors_list.index(door)])
    update_score()
    stay_button.configure(state="disabled")
    switch_button.configure(state="disabled")
    play_again_button.pack()


def update_score():
    try:
        print(f"""
        Total stays: {total_stays}
        Stay win rate: {correct_guesses_stay/total_stays*100}%

        Total switches: {total_switches}
        Switch win rate: {correct_guesses_switch/total_switches*100}%
        
        """)
    except ZeroDivisionError:
        if correct_guesses_stay < 1:
            print(f"""
        Total stays: {total_stays}
        Stay win rate: 0.0%

        Total switches: {total_switches}
        Switch win rate: {correct_guesses_switch/total_switches*100}%

        """)
        else:
            print(f"""
        Total stays: {total_stays}
        Stay win rate: {correct_guesses_stay/total_stays*100}%

        Total switches: {total_switches}
        Switch win rate: 0.0%

        """)


# tk.Frames
button_frame = tk.Frame(root)
button_frame.grid(row=1, column=0)
###
# text_frame = tk.Frame(root)
# text_frame.grid(row=1, column=1)

# Buttons
play_again_button = tk.Button(button_frame,
                              text="Play Again",
                              command=play_again)
switch_button = tk.Button(button_frame,
                          text="switch",
                          command=switch,
                          state="disabled")

stay_button = tk.Button(button_frame,
                        text="stay",
                        command=stay,
                        state="disabled")
switch_button.pack()
stay_button.pack()

###
# label1 = tk.Label(text_frame, text="Scoreboard")
# label1.pack()


root.mainloop()
