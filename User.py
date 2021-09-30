from Health import Health
from AttackComp import AttackComp

import uuid

users = []

class User:
    def __init__(self, client, name):
        self.client = client
        self.name = name
        self.id = uuid.uuid4()
        self.room = None
        self.health = Health(self, 100, 100)
        self.attack = AttackComp(self, 6, 1, 12)

    def Destroy(self):
        self.client.close()
        print (f"{self.name} {self.id} disconnected.")
        if self.room != None:
            self.room.Leave(self)

    def SetTarget(self, target):
        self.attack.SetTarget(target)

    def Attack(self):
        self.attack.Attack()

    # Static Functions
    def UserAdd(client, name):
        user = User(client, name)
        users.append(user)
        return user

    def UserRemove(user):
        users.remove(user)

    def UserGetList():
        return users