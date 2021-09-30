from Health import Health
from AttackComp import AttackComp
from ElapsedTimer import ElapsedTimer

class Enemy:
    def __init__(self, name, max_hp, dc, respawn_rate):
        self.name = name
        self.health = Health(self, max_hp, max_hp)
        self.attack = AttackComp(self, 4, 1, dc)
        self.respawn_rate = respawn_rate
        self.respawn = ElapsedTimer(0)
        self.room = None

    def GetName(self):
        return self.name

    def Die(self):
        self.respawn = ElapsedTimer(self.respawn_rate)
        self.attack.target = None
        self.attack.in_combat = False

    def SetTarget(self, target):
        self.attack.SetTarget(target)

    def Update(self):
        if self.health.IsDead():
            if self.respawn.Elapsed():
                self.health.Heal(self.health.max_hp)
                self.room.Chat(f"{self.name} respawned.\n")
        elif self.attack.in_combat:
            self.attack.Attack()
            