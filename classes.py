# -*- coding: utf-8 -*-
class Smurf:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return self.name + ": " + str(self.age)

def main():
    boris = Smurf("Boris", 28)
    print boris

    smurfs = [Smurf("Gok", 30), Smurf("Akka", 19), Smurf(u"Вася", 13)]
    print smurfs
    print [unicode(s) for s in smurfs]

if __name__ == "__main__":
    main()
