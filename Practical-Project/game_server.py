import tkinter as tk
from tkinter import *
import socket
import threading
from time import sleep


window = tk.Tk()
window.title("Server Of The Game")
window.geometry("450x200")
border_color = Frame(window, background="red")
#window.config(bg="#FFF8D6")

# Top frame consisting of two buttons widgets (i.e. btnStart, btnStop)
topFrame = tk.Frame(window)
lblmain = tk.Label(topFrame,text=" OSAMA AYMAN EL-SAYED ",fg='white',bg='blue' )
lblmain.grid(row=0,column=1,padx=3,pady=3)
lblmain2 = tk.Label(topFrame,text=" SEC 1 ",fg='white',bg='blue')
lblmain2.grid(row=1,column=1,padx=3,pady=3)
btnStart = tk.Button(topFrame, text="Start",foreground='white',background='green', command=lambda : start_server())
btnStart.grid(row=5,column=3,padx=3,pady=3)
btnStop = tk.Button(topFrame, text="Stop",foreground='white',background='red', command=lambda : stop_server(), state=tk.DISABLED)
btnStop.grid(row=6,column=3,padx=3,pady=3)
topFrame.pack(side=tk.LEFT, pady=(5, 5))

# Middle frame consisting of two labels for displaying the host and port info
middleFrame = tk.Frame(window)
lblHost = tk.Label(middleFrame, text = "Address: X.X.X.X",foreground='white',bg='red')
lblHost.grid(row=1, column=3, padx= 3, pady=3)
lblPort = tk.Label(middleFrame, text = "Port:XXXX",foreground='white',bg='blue')
lblPort.grid(row=1, column=6, padx= 3, pady=3)
middleFrame.pack(side=tk.TOP,pady=(3, 0),padx=(0,3))

# The client frame shows the client area
clientFrame = tk.Frame(window)
lblLine = tk.Label(clientFrame, text="Client List",foreground='white',bg='green').pack()
scrollBar = tk.Scrollbar(clientFrame)
scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
tkDisplay = tk.Text(clientFrame, height=10, width=30)
tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
scrollBar.config(command=tkDisplay.yview)
tkDisplay.config(yscrollcommand=scrollBar.set, background='#FFF8D6', highlightbackground="green", state="disabled")
clientFrame.pack(side=tk.BOTTOM, pady=(5, 10))


server = None
HOST_ADDR = "127.0.0.1"
HOST_PORT = 7002
client_name = " "
clients = []
clients_names = []
player_data = []


# Start server function
def start_server():
    global server, HOST_ADDR, HOST_PORT # code is fine without this
    btnStart.config(state=tk.DISABLED)
    btnStop.config(state=tk.NORMAL)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("socket created successfully...")
    #print(socket.AF_INET)
    #print(socket.SOCK_STREAM)

    server.bind((socket.gethostname(), HOST_PORT))
    print("server binded to ",HOST_PORT)
    server.listen(5)  # server is listening for client connection

    threading._start_new_thread(accept_clients, (server, " "))

    lblHost["text"] = "Address: " + HOST_ADDR
    lblPort["text"] = "Port: " + str(HOST_PORT)


# Stop server function
def stop_server():
    global server
    server.close()
    btnStart.config(state=tk.NORMAL)
    btnStop.config(state=tk.DISABLED)


def accept_clients(the_server, y):
    while True:
        if len(clients) < 2:
            client, addr = the_server.accept()
            print(f"Connection from {addr} has been established!")
            clients.append(client)

            # use a thread so as not to clog the gui thread
            threading._start_new_thread(send_receive_client_message, (client, addr))

# Function to receive message from current client AND
# Send that message to other clients
#Edit 2 ====> change alot of things in that function to slove the problem of bytes and str


# Function to receive message from current client AND
# Send that message to other clients
def send_receive_client_message(client_connection, client_ip_addr):
    global server, clients, clients_names, player_data

    client_msg = " "

    # send welcome message to client
    client_name = client_connection.recv(4096)
    if len(clients) < 2:
        client_connection.send(b"welcome1")
    else:
        client_connection.send(b"welcome2")

    clients_names.append(client_name)
    update_client_names_display(clients_names)  # update client names display

    if len(clients) > 1:
        # send opponent name to client
        clients[0].send(("opponent_name$" + clients_names[1].decode()).encode())
        clients[1].send(("opponent_name$" + clients_names[0].decode()).encode())

        sleep(1)

        # send signal to both clients to start game
        clients[0].send(b"start")
        clients[1].send(b"start")

    while True:
        data = client_connection.recv(4096)
        if not data:
            break
        #print(data)
        if len(clients) > 1 and client_connection == clients[0]:
            player_data.append({"socket": clients[0], "choice": data})
        elif len(clients) > 1 and client_connection == clients[1]:
            player_data.append({"socket": clients[1], "choice": data})
        print(player_data)
        if len(player_data) == 2:
            # send opponent choice to each client
            player_data[0].get("socket").send(("$opponent_choice" + player_data[1].get("choice").decode()).encode())
            player_data[1].get("socket").send(("$opponent_choice" + player_data[0].get("choice").decode()).encode())

            player_data = []
        #print(player_data)

    client_connection.close()


#Return the index of the current client in the list of clients
def get_client_index(client_list, curr_client):
    idx = 0
    for conn in client_list:
        if conn == curr_client:
            break
        idx = idx + 1

    return idx


# Update client name display when a new client connects OR
# When a connected client disconnects
def update_client_names_display(name_list):
    tkDisplay.config(state=tk.NORMAL)
    tkDisplay.delete('1.0', tk.END)

    for c in name_list:
        #Edit 3 ===> solve: display the name of players in server gui
        tkDisplay.insert(tk.END, c.decode()+"\n")
    tkDisplay.config(state=tk.DISABLED)


window.mainloop()
