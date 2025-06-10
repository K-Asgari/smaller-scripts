"""
19.04.2022

TicTacToe tkinter - 2nd attempt. 
Game logic is complete.
ToDo:
    Add play again option. - Done
    Add win counter. - Done
    Add quit button. - Done
    


"""


import tkinter as tk


window = tk.Tk()
window.title('Tic-Tac-Toe')
window.geometry('450x550')
window.config(bg='#222222')
window.resizable(False, False)


# Game variables
p1_win_counter = 0
p2_win_counter = 0
draw_counter = 0
p1_piece = 'X'
p2_piece = 'O'
played_pieces_on_board = []
p1_pieces_on_board = set()
p2_pieces_on_board = set()


win_conditions = [{0, 1, 2}, {3, 4, 5},
                  {6, 7, 8}, {0, 3, 6},
                  {1, 4, 7}, {2, 5, 8},
                  {0, 4, 8}, {2, 4, 6}]
# Button indexes:
# 0, 1, 2,
# 3, 4, 5,
# 6, 7, 8


# Create and place tk.Widget frames
button_frame = tk.Frame(bg='#222222')
button_frame.pack(side=tk.TOP)
text_frame = tk.Frame(window, bg='gray')
text_frame.pack(side=tk.TOP)

# Game text labels
scoreboard_text = (f"""
    Player X wins: {p1_win_counter}
    Player O wins: {p2_win_counter}
    Draws: {draw_counter}
    """)

score_text_label = tk.Label(text_frame, bg='red', width=30,height=6, font='calibri, 10', text=scoreboard_text)
score_text_label.pack(side=tk.LEFT)
game_text_label = tk.Label(text_frame, bg='yellow',width=10, height=6, font='calibri, 15')
game_text_label.pack(side=tk.LEFT)


# Create tk.Widget buttons
buttons_list = []
for button_index in range(9):
    btn = tk.Button(master=button_frame,
                    text='',
                    height=2,
                    width=6,
                    bg='#777777',
                    font=('calibri', 30),
                    borderwidth=8,
                    activebackground='orange4',
                    disabledforeground='black' ,
                    command=lambda button_index=button_index: button_clicked(button_index))
    buttons_list.append(btn)

# Place buttons by grid in button frame
counter = 0
for x in range(3):
    for y in range(3):
        buttons_list[counter].grid(row=x, column=y)
        counter += 1


def move_validator(button_pressed):
    for i, button in enumerate(buttons_list):
        if button == button_pressed:
            if i not in played_pieces_on_board:
                played_pieces_on_board.append(i)
                button.configure(state='disabled')
                return True
            else:
                game_text_label.configure(text='Invalid move,\n try again!')
                return False


def button_clicked(button_index):
    global p1_win_counter, p2_win_counter
    current_player = get_player_turn(len(played_pieces_on_board))
    if move_validator(buttons_list[button_index]):
        buttons_list[button_index].config(text=current_player)
        if current_player == p1_piece:
            p1_pieces_on_board.add(button_index)
        else:
            p2_pieces_on_board.add(button_index)

    if win_check():
        if current_player == p1_piece:
            p1_win_counter += 1
        else:
            p2_win_counter += 1
    draw_check()
    update_game_text()

def get_player_turn(played_pieces: int):
    if played_pieces % 2 == 0:
        return p1_piece
    else:
        return p2_piece


def win_check():
    for combination in win_conditions:
        if combination.issubset(p1_pieces_on_board) or combination.issubset(p2_pieces_on_board):
            win_detected(combination)
            return True


def win_detected(win_combination):
    play_again_button.configure(state='normal')
    for button in buttons_list:
        button.configure(state="disabled")
    for i in win_combination:
        buttons_list[i].configure(bg='green')


def update_game_text():
    game_text_label.configure(text="")
    if win_check():
        game_text_label.configure(
            text=f"{get_player_turn((len(played_pieces_on_board)-1))} wins!")
    if draw_check():
        game_text_label.configure(text='Draw!')
    score_text_label.configure(text=(f"""
    Player X wins: {p1_win_counter}
    Player O wins: {p2_win_counter}
    Draws: {draw_counter}
    """))


def draw_check():
    global draw_counter
    if len(played_pieces_on_board) == 9 and not win_check():
        draw_counter += 1
        for button in buttons_list:
            button.configure(state="disabled", bg='gold4')
        play_again_button.configure(state='normal')
        return True


def play_again():
    global played_pieces_on_board, p1_pieces_on_board, p2_pieces_on_board
    played_pieces_on_board = []
    p1_pieces_on_board = set()
    p2_pieces_on_board = set()
    for button in buttons_list:
        button.configure(state='normal', text='', bg='#777777')
    game_text_label.configure(text='')
    play_again_button.configure(state='disabled')


play_again_button = tk.Button(text_frame, text='Play Again', state='disabled', command=play_again)
play_again_button.pack(side=tk.TOP)
quit_button = tk.Button(text_frame, text='Quit', command=window.destroy)
quit_button.pack(side=tk.BOTTOM, fill='x')


window.mainloop()
