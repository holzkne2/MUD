import uuid

rooms = []

class Room:
    def __init__(self, name):
        self.name = name
        self.id = uuid.uuid4()
        self.active_users = []
        self.enemies = []

    def Join(self, user):
        self.active_users.append(user)
        user.room = self
        user.client.sendall(f"Welcome to {self.name}!\n".encode('ascii'))
        self.Chat(f"{user.name} joined the room.\n")

    def Leave(self, user):
        self.active_users.remove(user)
        user.room = None
        self.Chat(f"{user.name} left the room.\n")

    def EnemySpawned(self, enemy):
        self.enemies.append(enemy)
        enemy.room = self

    def GetEnemy(self, target=None):
        if len(self.enemies) > 0:
            return self.enemies[0]
        else:
            return None

    def Search(self, searcher):
        out_message = "Users:\n"
        for user in self.active_users:
            out_message += "\t" + user.GetName() + "\n"
        out_message += "Enemies:\n"
        for enemy in self.enemies:
            out_message += "\t" + enemy.GetName() + "\n"
        searcher.client.sendall(out_message.encode('ascii'))

    def Chat(self, message):
        for user in self.active_users:
            user.client.sendall(message.encode('ascii'))

    def Update(self):
        for user in self.active_users:
            if user.attack.in_combat:
                user.Attack()
        for enemy in self.enemies:
            enemy.Update()

    def GetRoom(id=None, name=None):
        for room in rooms:
            if id != None and room.id == id:
                return room
            if name != None and room.name == name:
                return room

    def GetRoomList():
        return rooms

    def AddRoom(room):
        rooms.append(room)
        return room
