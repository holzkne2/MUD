import threading
import socket
import sys
from tkinter import *

HOST = "127.0.0.1"
PORT = 65432

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((HOST, PORT))

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if not message:
                client.close()
                break

            if message == "NICK":
                client.sendall(nickname.encode('ascii'))
            else:
                # print(message, end=(''))
                Output.insert(END,message)
                Output.see(END)
        except:
            client.close()
            break


def write():
    while True:
        try:
            user_input = input()
            message = f"{nickname} {user_input}"
            client.sendall(message.encode('ascii'))
        except:
            break

window = Tk()
window.title("Space Lands")
window.geometry("1000x430")

def Take_input():
    user_input = inputtxt.get()
    message = f"{nickname} {user_input}"
    client.sendall(message.encode('ascii'))
    inputtxt.delete(0, END)

def OnEnter(arg):
    Take_input()

window.bind('<Return>', OnEnter)

inputtxt = Entry(window,
                width = 300,
                bg = "wheat1")
  
Output = Text(window, height = 25, 
              width = 300, 
              bg = "burlywood1")
  
Display = Button(window, height = 1,
                 width = 20, 
                 text ="Execute",
                 command = lambda:Take_input())
  
Output.pack()
Display.pack(side = LEFT)
inputtxt.pack(side = RIGHT)

# nickname = input("Choose a nickname: ")
nickname = sys.argv[1]

receive_thread = threading.Thread(target=receive)
receive_thread.daemon = True
receive_thread.start()

# write_thread = threading.Thread(target=write)
# write_thread.start()

window.mainloop()
print("Disconnect from server!")
sys.exit()