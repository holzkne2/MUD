from User import User
from Room import Room
from Enemy import Enemy
from ElapsedTimer import ElapsedTimer

import threading
import socket


HOST = "127.0.0.1"
PORT = 65432

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

def broadcast(message):
    for user in User.UserGetList():
        user.client.sendall(message)

def message_breakdown(user, message):
    tokens = message.split()
    if len(tokens) < 2:
        return
    if tokens[1].lower() in ["help"]:
        say_message = """say text\n\tSay something
goto room\n\tGoto another room
attack\n\tAttack enemy in room
search\n\tSearch room
"""
        user.client.sendall(say_message.encode('ascii'))

    elif tokens[1].lower() in ["say"]:
        say_message = f"{user.name}:"
        for i in range(2, len(tokens)-1):
            say_message += tokens[i] + " "
        say_message += tokens[len(tokens)-1] + '\n'
        user.room.Chat(say_message)

    elif tokens[1].lower() in ["goto"]:
        desired_room = Room.GetRoom(name=tokens[2])
        if desired_room == None:
            user.client.sendall("Unknown Room\n".encode('ascii'))
        elif desired_room == user.room:
            user.client.sendall("You are already in that room.\n".encode('ascii'))
        else:
            user.room.Leave(user)
            desired_room.Join(user)

    elif tokens[1].lower() in ["attack"]:
        enemy = user.room.GetEnemy()
        if enemy == None:
            user.client.sendall("Enemy not found.\n".encode('ascii'))
        else:
            user.SetTarget(enemy)
            user.room.Chat(f"{user.name} started attacking {enemy.name}\n")
            user.Attack()
            enemy.SetTarget(user)
            enemy.attack.Attack()

    elif tokens[1].lower() in ["search"]:
        user.room.Search(user)

    else:
        user.client.sendall("Unknown Command\n".encode('ascii'))

def handle(user):
    while True:
        try:
            message = user.client.recv(1024).decode('ascii')
            if not message:
                user.Destroy()
                User.UserRemove(user)
                break
            message_breakdown(user, message)
        except socket.error:
            user.Destroy()
            User.UserRemove(user)
            break

def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.sendall("NICK".encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        user = User.UserAdd(client, nickname)
        client.sendall("Connected to the server!\n".encode('ascii'))

        room = Room.GetRoom(name="Lobby")
        room.Join(user)

        thread = threading.Thread(target=handle, args=(user,))
        thread.start()

receive_thread = threading.Thread(target=receive)
receive_thread.start()

lobby = Room.AddRoom(Room("Lobby"))
room_01 = Room.AddRoom(Room("Room01"))

slime = Enemy("Slime", 14, 8, 5)
lobby.EnemySpawned(slime)

while True:
    desired_framerate = ElapsedTimer(0.1)
    for room in Room.GetRoomList():
        room.Update()
    desired_framerate.Sleep()

server.close()
