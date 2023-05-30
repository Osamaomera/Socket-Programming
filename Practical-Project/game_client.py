#----------------------------------------------- import the libraries Start -------------------------------------------------------------------
import tkinter as tk
from tkinter import PhotoImage
from tkinter import messagebox
import socket
from tkinter import *
from time import sleep
import threading
from PIL import Image , ImageTk
#----------------------------------------------- import the libraries End -------------------------------------------------------------------

# ----------------------------------------------MAIN GAME WINDOW Start -------------------------------------------------------------------
window_main = tk.Tk()
window_main.title("Game Client")
window_main.geometry("400x600")
img3=Image.open(r"bgimg1.jpg")
#img3=img3.resize((window_main.winfo_screenwidth(),window_main.winfo_screenheight()),Image.Resampling.LANCZOS)
photoimg3=ImageTk.PhotoImage(img3)
#bg_img=Label(window_main,image=photoimg3)
#bg_img.place(x=0,y=0,width=window_main.winfo_screenwidth(),height=window_main.winfo_screenheight())
# ----------------------------------------------MAIN GAME WINDOW End ---------------------------------------------------------------------

#----------------------------------------------initialization of global variables Start  --------------------------------------------------
your_name = ""
opponent_name = ""
game_round = 0
game_timer = 5
your_choice = ""
opponent_choice = ""
TOTAL_NO_OF_ROUNDS = 5
your_score = 0
opponent_score = 0
#----------------------------------------------initialization of global variables End --------------------------------------------------


# ---------------------------------------------------------- Network Client Start ------------------------------------------------
client = None
HOST_ADDR = "127.0.0.1"
HOST_PORT = 7002
#----------------------------------------------------------- Network Client End ---------------------------------------------------


#--------------------------------------------------------- First frame (name and connect) Start -------------------------------------------
top_welcome_frame= tk.Frame(window_main)
#bg_img_welcome = Label(top_welcome_frame, image = photoimg3)
#bg_img_welcome.place(x=0,y=0,width=top_welcome_frame.winfo_screenwidth(),height=top_welcome_frame.winfo_screenheight())
lbl_main = tk.Label(top_welcome_frame, text=" BY OSAMA AYMAN EL-SAYED ", bg="blue", fg="white")
lbl_main.grid(row=0,column=1,pady=5)
lbl_name = tk.Label(top_welcome_frame, text = "Name:",font=("Arial", 10), bg="blue", fg="white")
lbl_name.grid(row=2,column=0)
ent_name = tk.Entry(top_welcome_frame,font=("Arial", 10))
ent_name.grid(row=2,column=1)
btn_connect = tk.Button(top_welcome_frame, text="Connect",font=("Arial", 10), bg="blue", fg="white", command=lambda : connect())
btn_connect.grid(row=2,column=2,pady=(0,0))
top_welcome_frame.pack(side=tk.TOP)
#---------------------------------------------First frame (name and connect) End ------------------------------------------

#------------------------------------------  Welcome Frame (from server ) Start ---------------------------------------------------------
top_message_frame = tk.Frame(window_main)
#bg_img_msg = Label(top_message_frame, image = photoimg3)
#bg_img_msg.place(x=0,y=0,width=top_message_frame.winfo_screenwidth(),height=top_message_frame.winfo_screenheight())
lbl_line_server = tk.Label(top_message_frame, text="")
lbl_line_server.pack_forget()
lbl_welcome = tk.Label(top_message_frame, text="")
lbl_welcome.pack()
top_message_frame.pack(side=tk.TOP)
#------------------------------------------------ Welcome Frame (from server ) End -------------------------------------------------

#darkseagreen = #C1FFC1


#------------------------------------------------ TOP Frame (Game information ) Start -------------------------------------------------
top_frame = tk.Frame(window_main)
#bg_img_tpframe = Label(top_frame, image = photoimg3)
#bg_img_tpframe.place(x=0,y=0,width=top_frame.winfo_screenwidth(),height=top_frame.winfo_screenheight())
lbl_line = tk.Label(top_frame, text="____________________________________________________",fg="black").pack(pady=(0,5))
lbl_line = tk.Label(top_frame, text="GAME INFORMATION",fg="#151B54").pack(pady=(0,5))
top_left_frame = tk.Frame(top_frame, highlightcolor="white",bg="#E5E4E2", highlightthickness=0)
lbl_your_name = tk.Label(top_left_frame, text="Your name: " + your_name, font = "Helvetica 10 bold",fg='#151B54',bg="#E5E4E2")
lbl_opponent_name = tk.Label(top_left_frame, text="Opponent: " + opponent_name,fg='#151B54',bg="#E5E4E2")
lbl_your_name.grid(row=0, column=0, padx=3, pady=5)
lbl_opponent_name.grid(row=1, column=0, padx=3, pady=5)
top_left_frame.pack(side=tk.LEFT, padx=(10, 10))
#------------------------------------------------ TOP Frame (Game information ) End -------------------------------------------------

#------------------------------------------------ TOP Right Frame (Game information(number of round) ) Start -------------------------------------------------
top_right_frame = tk.Frame(top_frame, highlightcolor="white",bg="#E5E4E2", highlightthickness=0)
lbl_game_round = tk.Label(top_right_frame, text="Game round (x) starts in", foreground="black",bg="#E5E4E2", font = "Helvetica 10 bold")
lbl_timer = tk.Label(top_right_frame, text=" ", font = "Helvetica 12 bold",bg="#E5E4E2", foreground="black")
lbl_game_round.grid(row=0, column=0, padx=5, pady=5)
lbl_timer.grid(row=1, column=0, padx=5, pady=5)
top_right_frame.pack(side=tk.RIGHT, padx=(10, 10))

top_frame.pack_forget()
#------------------------------------------------ TOP Right Frame (Game information(number of round) ) End -------------------------------------------------


#------------------------------------------------ Middle Frame (Results round by round) ) Start ---------------------------------------------
middle_frame = tk.Frame(window_main)
#bg_img_mframe = Label(middle_frame, image = photoimg3)
#bg_img_mframe.place(x=0,y=0,width=middle_frame.winfo_screenwidth(),height=middle_frame.winfo_screenheight())
lbl_line = tk.Label(middle_frame, text=" ______________________________________________________ ", foreground="black").pack(pady=5)
lbl_line = tk.Label(middle_frame, text=" GAME LOG ", font = "Helvetica 12 bold", foreground="black").pack(pady=5)
lbl_final_result2 = tk.Label(middle_frame, text=" ", font = "Helvetica 12 bold", foreground="blue")
lbl_final_result2.pack()
lbl_line = tk.Label(middle_frame, text=" ______________________________________________________ ", foreground="black").pack()
#------------------------------------------------ Middle Frame (Results round by round) ) End ---------------------------------------------

#------------------------------------------------ Round Frame (Choices of me and opponent ) Start -------------------------------------------------
round_frame = tk.Frame(middle_frame)
#bg_img_rouframe = Label(round_frame, image = photoimg3)
#bg_img_rouframe.place(x=0,y=0,width=round_frame.winfo_screenwidth(),height=round_frame.winfo_screenheight())
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
#------------------------------------------------ Round Frame (Choices of me and opponent ) End -------------------------------------------------

#------------------------------------------------ Final Frame (Results of rounds ) Start -------------------------------------------------

final_frame = tk.Frame(middle_frame)
#bg_img_fiframe = Label(final_frame, image = photoimg3)
#bg_img_fiframe.place(x=0,y=0,width=final_frame.winfo_screenwidth(),height=final_frame.winfo_screenheight())
lbl_line = tk.Label(final_frame, text="").pack()
lbl_final_result = tk.Label(final_frame, text=" ", font = "Helvetica 13 bold", foreground="blue")
lbl_final_result.pack()
lbl_line = tk.Label(final_frame, text="").pack()
final_frame.pack(side=tk.TOP)

middle_frame.pack_forget()
#------------------------------------------------ Final Frame (Results of rounds ) End -------------------------------------------------


#------------------------------------------------ Buttons Frame (Buttons of rock_paper_scissors ) Start --------------------------------

button_frame = tk.Frame(window_main)
bg_img_btframe = Label(button_frame, image = photoimg3)
bg_img_btframe.place(x=0,y=0,width=button_frame.winfo_screenwidth(),height=button_frame.winfo_screenheight())
photo_rock = PhotoImage(file=r"istrock.png")
photo_paper = PhotoImage(file = r"istpaper.png")
photo_scissors = PhotoImage(file = r"istscissors.png")

btn_rock = tk.Button(button_frame, text="Rock", command=lambda : choice("rock"), state=tk.DISABLED, image=photo_rock)
btn_paper = tk.Button(button_frame, text="Paper", command=lambda : choice("paper"), state=tk.DISABLED, image=photo_paper)
btn_scissors = tk.Button(button_frame, text="Scissors", command=lambda : choice("scissors"), state=tk.DISABLED, image=photo_scissors)
btn_rock.grid(row=0, column=0)
btn_paper.grid(row=0, column=1)
btn_scissors.grid(row=0, column=2)
button_frame.pack(side=tk.BOTTOM)
#------------------------------------------------ Buttons Frame (Buttons of rock_paper_scissors ) End ------------------------------------


#------------------------------------------------ Logic Function (logic of the game) Start -------------------------------------------------
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
#------------------------------------------------ Logic Function (logic of the game) End -------------------------------------------------


#------------------------------------------------ Enable Function (enable rock_paper_socissors Buttons to play) Start -------------------------------------------------
def enable_disable_buttons(todo):
    if todo == "disable":
        btn_rock.config(state=tk.DISABLED)
        btn_paper.config(state=tk.DISABLED)
        btn_scissors.config(state=tk.DISABLED)
    else:
        btn_rock.config(state=tk.NORMAL)
        btn_paper.config(state=tk.NORMAL)
        btn_scissors.config(state=tk.NORMAL)
#------------------------------------------------ Enable Function (enable rock_paper_socissors Buttons to play) End -------------------------------------------------

#------------------------------------------------ Reset Function (Reset the result and choices ) Start --------------------------------------------------------------
def reset():
    global game_round 
    game_round = 0
    global your_choice
    your_choice = ""
    global opponent_choice
    opponent_choice = ""
    global your_score
    your_score = 0
    global opponent_score
    opponent_score = 0    
#------------------------------------------------ Reset Function (Reset the result and choices ) Start --------------------------------------------------------------

#------------------------------------------------ Connect Function (the button of connect ) Start --------------------------------------------------------------
def connect():
    global your_name
    if len(ent_name.get()) < 1:
        tk.messagebox.showerror(title="ERROR!!!", message="You MUST enter your first name <e.g. John>")
    else:
        your_name = ent_name.get()
        lbl_your_name["text"] = "Your name: " + your_name
        connect_to_server(your_name)
#------------------------------------------------ Connect Function (the button of connect ) End --------------------------------------------------------------

#------------------------------------------------ Count_down Function (to count the number of round ) Start --------------------------------------------------------------
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
#------------------------------------------------ Count_down Function (to count the number of round ) End --------------------------------------------------------------


#------------------------------------------------ Choice Function (save your choice and show it in label ) Start --------------------------------------------------------------

def choice(arg):
    global your_choice, client, game_round
    your_choice = arg
    lbl_your_choice["text"] = "Your choice: " + your_choice

    if client:
        # Edit 5 ==> to send in bytes
        result = (your_choice).encode()
        client.send(result)
        enable_disable_buttons("disable")
#------------------------------------------------ Choice Function (save your choice and show it in label ) End --------------------------------------------------------------


#------------------------------------------------ Connect to server Function (establish a connection to server) Start --------------------------------------------------------------
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
#------------------------------------------------ Connect to server Function (establish a connection to server) End --------------------------------------------------------------

#------------------------------ Receive Function (receive a information of choices and results of game from server) Start --------------------------------------------------------------
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
                reset()
            # Start the timer
            threading._start_new_thread(count_down, (game_timer, ""))


    sck.close()
#------------------------------ Receive Function (receive a information of choices and results of game from server) End --------------------------------------------------------------


#------------------------------------------------------- Main loop the main Window Start --------------------------------------------------------------
window_main.mainloop()
#------------------------------------------------------- Main loop the main Window Start --------------------------------------------------------------
