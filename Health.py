class Health:
    def __init__(self, object, curr_hp, max_hp):
        self.object = object
        self.curr_hp = curr_hp
        self.max_hp = max_hp

    def Damage(self, amount):
        self.curr_hp = max(self.curr_hp - amount, 0)
        if (self.curr_hp == 0):
            self.Die()

    def Heal(self, amount):
        self.curr_hp = min(self.curr_hp + amount, self.max_hp)

    def IsDead(self):
        return self.curr_hp == 0

    def Die(self):
        if self.object.Die != None:
            self.object.Die()