from ElapsedTimer import ElapsedTimer

import random

class AttackComp:
    def __init__(self, object, damage, rate, dc):
        self.object = object
        self.damage = damage
        self.rate = rate
        self.ready = ElapsedTimer(0)
        self.target = None
        self.in_combat = False
        self.dc = dc

    def SetTarget(self, target):
        self.target = target

    def Attack(self):
        self.in_combat = True

        if self.ready.Elapsed() == False:
            return
        self.ready = ElapsedTimer(self.rate)

        hit = random.randint(1, 20)
        if hit > self.target.attack.dc:
            damage_amount = random.randint(1, self.damage)
            if hit == 20:
                damage_amount += self.damage
            self.target.health.Damage(damage_amount)
            self.object.room.Chat(f"{self.object.name} did {damage_amount} damage to {self.target.name} [{self.target.health.curr_hp}/{self.target.health.max_hp}]\n")
            if self.target.health.IsDead():
                self.object.room.Chat(f"{self.object.name} killed {self.target.name}\n")
                self.in_combat = False
                self.target = None
        else:
            self.object.room.Chat(f"{self.object.name} missed {self.target.name}\n")

