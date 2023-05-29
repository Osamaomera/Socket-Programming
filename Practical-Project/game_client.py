
import tkinter as tk
from tkinter import PhotoImage
from tkinter import messagebox
import socket
from time import sleep
import threading

# MAIN GAME WINDOW
window_main = tk.Tk()
window_main.title("Game Client")
window_main.geometry("400x600")
your_name = ""
opponent_name = ""
game_round = 0
game_timer = 5
your_choice = ""
opponent_choice = ""
TOTAL_NO_OF_ROUNDS = 5
your_score = 0
opponent_score = 0

# network client
client = None
HOST_ADDR = "127.0.0.1"
HOST_PORT = 7002


top_welcome_frame= tk.Frame(window_main)
lbl_main = tk.Label(top_welcome_frame, text=" BY OSAMA AYMAN EL-SAYED ", bg="blue", fg="white")
lbl_main.grid(row=0,column=1,pady=5)
lbl_name = tk.Label(top_welcome_frame, text = "Name:",font=("Arial", 10), bg="blue", fg="white")
lbl_name.grid(row=2,column=0,pady=5)
ent_name = tk.Entry(top_welcome_frame,font=("Arial", 10))
ent_name.grid(row=2,column=1,pady=5)
btn_connect = tk.Button(top_welcome_frame, text="Connect",font=("Arial", 10), bg="blue", fg="white", command=lambda : connect())
btn_connect.grid(row=2,column=2,pady=(0,5))
top_welcome_frame.pack(side=tk.TOP)

top_message_frame = tk.Frame(window_main)
lbl_line_server = tk.Label(top_message_frame, text="")
lbl_line_server.pack_forget()
lbl_welcome = tk.Label(top_message_frame, text="")
lbl_welcome.pack()
top_message_frame.pack(side=tk.TOP)

#darkseagreen = #C1FFC1

top_frame = tk.Frame(window_main)
lbl_line = tk.Label(top_frame, text="____________________________________________________",fg="black").pack(pady=(0,5))
lbl_line = tk.Label(top_frame, text="GAME INFORMATION",fg="green").pack(pady=(0,5))
top_left_frame = tk.Frame(top_frame, highlightbackground="green", highlightcolor="white",bg="#FFF8D6", highlightthickness=1)
lbl_your_name = tk.Label(top_left_frame, text="Your name: " + your_name, font = "Helvetica 10 bold",fg='black',bg="#FFF8D6")
lbl_opponent_name = tk.Label(top_left_frame, text="Opponent: " + opponent_name,fg='black',bg="#FFF8D6")
lbl_your_name.grid(row=0, column=0, padx=3, pady=5)
lbl_opponent_name.grid(row=1, column=0, padx=3, pady=5)
top_left_frame.pack(side=tk.LEFT, padx=(10, 10))


top_right_frame = tk.Frame(top_frame, highlightbackground="green", highlightcolor="white",bg="#FFF8D6", highlightthickness=1)
lbl_game_round = tk.Label(top_right_frame, text="Game round (x) starts in", foreground="black",bg="#FFF8D6", font = "Helvetica 10 bold")
lbl_timer = tk.Label(top_right_frame, text=" ", font = "Helvetica 12 bold",bg="#FFF8D6", foreground="black")
lbl_game_round.grid(row=0, column=0, padx=5, pady=5)
lbl_timer.grid(row=1, column=0, padx=5, pady=5)
top_right_frame.pack(side=tk.RIGHT, padx=(10, 10))

top_frame.pack_forget()

middle_frame = tk.Frame(window_main)
lbl_line = tk.Label(middle_frame, text=" ______________________________________________________ ", foreground="black").pack(pady=5)
lbl_line = tk.Label(middle_frame, text=" GAME LOG ", font = "Helvetica 12 bold", foreground="black").pack(pady=5)
lbl_final_result2 = tk.Label(middle_frame, text=" ", font = "Helvetica 12 bold", foreground="blue")
lbl_final_result2.pack()
lbl_line = tk.Label(middle_frame, text=" ______________________________________________________ ", foreground="black").pack()
round_frame = tk.Frame(middle_frame)
lbl_round = tk.Label(round_frame, text="Round")
lbl_round.pack(pady=5)
lbl_your_choice = tk.Label(round_frame, text="Your choice: " + "None", font = "Helvetica 14 bold")
lbl_your_choice.pack()
lbl_opponent_choice = tk.Label(round_frame, text="Opponent choice: " + "None",font = "Helvetica 10")
lbl_opponent_choice.pack()
lbl_line = tk.Label(round_frame, text=" ______________________________________________________ ", foreground="black").pack(pady=5)
lbl_result = tk.Label(round_frame, text=" ", foreground="red", font = "Helvetica 12 bold")
lbl_result.pack()
round_frame.pack(side=tk.TOP)

final_frame = tk.Frame(middle_frame)
lbl_line = tk.Label(final_frame, text="").pack()
lbl_final_result = tk.Label(final_frame, text=" ", font = "Helvetica 13 bold", foreground="blue")
lbl_final_result.pack()
lbl_line = tk.Label(final_frame, text="").pack()
final_frame.pack(side=tk.TOP)

middle_frame.pack_forget()

button_frame = tk.Frame(window_main)
photo_rock = PhotoImage(file=r"rock.gif")
photo_paper = PhotoImage(file = r"paper.gif")
photo_scissors = PhotoImage(file = r"scissors.gif")

btn_rock = tk.Button(button_frame, text="Rock", command=lambda : choice("rock"), state=tk.DISABLED, image=photo_rock)
btn_paper = tk.Button(button_frame, text="Paper", command=lambda : choice("paper"), state=tk.DISABLED, image=photo_paper)
btn_scissors = tk.Button(button_frame, text="Scissors", command=lambda : choice("scissors"), state=tk.DISABLED, image=photo_scissors)
btn_rock.grid(row=0, column=0)
btn_paper.grid(row=0, column=1)
btn_scissors.grid(row=0, column=2)
button_frame.pack(side=tk.BOTTOM)


def game_logic(you, opponent):
    winner = ""
    rock = "rock"
    paper = "paper"
    scissors = "scissors"
    player0 = "you"
    player1 = "opponent"
    
    if you == opponent:
        winner = "Draw"

    elif you == rock:
        if opponent == scissors:
            winner = player0

        elif opponent == paper:
            winner = player1
        
    elif you == scissors:
        if opponent == paper:
            winner = player0
            
        elif opponent == rock:
            winner = player1

    elif you == paper:
        if opponent == rock:
            winner = player0

        elif opponent == scissors:
            winner = player1

            
    return winner


def enable_disable_buttons(todo):
    if todo == "disable":
        btn_rock.config(state=tk.DISABLED)
        btn_paper.config(state=tk.DISABLED)
        btn_scissors.config(state=tk.DISABLED)
    else:
        btn_rock.config(state=tk.NORMAL)
        btn_paper.config(state=tk.NORMAL)
        btn_scissors.config(state=tk.NORMAL)


def reset():
    game_round = 0
    game_timer = 5
    your_choice = ""
    opponent_choice = ""
    TOTAL_NO_OF_ROUNDS = 5
    your_score = 0
    opponent_score = 0
    
    
def connect():
    global your_name
    if len(ent_name.get()) < 1:
        tk.messagebox.showerror(title="ERROR!!!", message="You MUST enter your first name <e.g. John>")
    else:
        your_name = ent_name.get()
        lbl_your_name["text"] = "Your name: " + your_name
        connect_to_server(your_name)


def count_down(my_timer, nothing):
    global game_round
    if game_round <= TOTAL_NO_OF_ROUNDS:
        game_round = game_round + 1
    elif game_round>TOTAL_NO_OF_ROUNDS:
        reset()

    lbl_game_round["text"] = "Game round " + str(game_round) + " starts in"

    while my_timer > 0:
        my_timer = my_timer - 1
        #print("game timer is: " + str(my_timer))
        lbl_timer["text"] = my_timer
        sleep(1)

    enable_disable_buttons("enable")
    lbl_round["text"] = "Round - " + str(game_round)
    lbl_final_result["text"] = ""


def choice(arg):
    global your_choice, client, game_round
    your_choice = arg
    lbl_your_choice["text"] = "Your choice: " + your_choice

    if client:
        # Edit 5 ==> to send in bytes
        result = (your_choice).encode()
        client.send(result)
        enable_disable_buttons("disable")
        


def connect_to_server(name):
    global client, HOST_PORT, HOST_ADDR, your_name
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((socket.gethostname(), HOST_PORT))
        # client.send(name) # Send name to server after connecting
        #Edit 1 ==> which solve the problem of connection
        client.send(name.encode('utf-8'))  # Send name to server after connecting
        print("Connected to the server")
        # disable widgets
        btn_connect.config(state=tk.DISABLED)
        ent_name.config(state=tk.DISABLED)
        lbl_name.config(state=tk.DISABLED)
        enable_disable_buttons("disable")

        # start a thread to keep receiving message from server
        # do not block the main thread :)
        threading._start_new_thread(receive_message_from_server, (client, "m"))
        # receive_message_thread = threading.Thread(target= receive_message_from_server, args =(client,))
        # receive_message_thread.start()
    except Exception as e:
        tk.messagebox.showerror(title="ERROR!!!", message="Cannot connect to host: " + HOST_ADDR + " on port: " + str(HOST_PORT) + " Server may be Unavailable. Try again later")


def receive_message_from_server(sck,m):
    global your_name, opponent_name, game_round
    global your_choice, opponent_choice, your_score, opponent_score

    while True:
        # Edit 4 ==> must decode the message
        from_server = sck.recv(4096).decode('utf-8')

        if not from_server: break

        if from_server.startswith("welcome"):
            if from_server == "welcome1":
                lbl_welcome["text"] = "Server says: Welcome " + your_name + "! Waiting for player 2"
            elif from_server == "welcome2":
                lbl_welcome["text"] = "Server says: Welcome " + your_name + "! Game will start soon"
            lbl_line_server.pack()
            #lbl_line_server.destroy()

        elif from_server.startswith("opponent_name$"):
            opponent_name = from_server.replace("opponent_name$", "")
            lbl_opponent_name["text"] = "Opponent: " + opponent_name
            top_frame.pack()
            middle_frame.pack()

            # we know two users are connected so game is ready to start
            threading._start_new_thread(count_down, (game_timer, ""))
            lbl_welcome.config(state=tk.DISABLED)
            lbl_line_server.config(state=tk.DISABLED)

        elif from_server.startswith("$opponent_choice"):
            # get the opponent choice from the server
            opponent_choice = from_server.replace("$opponent_choice", "")
            your_choice1=from_server.startswith("$your_choice")
            
            #print the choices of you and apponenet in powershell 
            print(f"your choice is {your_choice}")
            print(f"opponent choice is {opponent_choice}")
            
            # figure out who wins in this round
            who_wins = game_logic(your_choice, opponent_choice)
            round_result = " "
            
            #print the winner in powershell
            print("the winner is "+ who_wins)
            
            if who_wins == "you":
                your_score = your_score + 1
                round_result = "WIN"
                lbl_final_result2["text"] = "RESULT = " + str(your_score) + " - " + str(opponent_score)
                lbl_final_result2.config(foreground='green')
                print("RESULT = " + str(your_score) + " - " + str(opponent_score))
            elif who_wins == "opponent":
                opponent_score = opponent_score + 1
                round_result = "LOSS"
                lbl_final_result2["text"] = "RESULT = " + str(your_score) + " - " + str(opponent_score)
                lbl_final_result2.config(foreground='green')
                print("RESULT = " + str(your_score) + " - " + str(opponent_score))
            else:
                round_result = "DRAW"
                lbl_final_result2["text"] = "RESULT = " + str(your_score) + " - " + str(opponent_score)
                lbl_final_result2.config(foreground='green')
                print("RESULT = " + str(your_score) + " - " + str(opponent_score))
    
            # Update GUI
            lbl_opponent_choice["text"] = "Opponent choice: " + opponent_choice
            lbl_result["text"] = "Result: " + round_result

            # is this the last round e.g. Round 5?
            if game_round == TOTAL_NO_OF_ROUNDS:
                # compute final result
                final_result = ""
                color = ""

                if your_score > opponent_score:
                    final_result = "(You Won!!!)"
                    color = "green"
                elif your_score < opponent_score:
                    final_result = "(You Lost!!!)"
                    color = "red"
                else:
                    final_result = "(Draw!!!)"
                    color = "black"

                lbl_final_result["text"] = "FINAL RESULT: " + str(your_score) + " - " + str(opponent_score) + " " + final_result
                lbl_final_result.config(foreground=color)

                enable_disable_buttons("disable")
                game_round = 0
                your_score=0
                opponent_score=0
            # Start the timer
            threading._start_new_thread(count_down, (game_timer, ""))


    sck.close()


window_main.mainloop()