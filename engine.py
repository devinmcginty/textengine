import sys

class Room(object):
    def __init__(self, name, description):
        self.setName(name)
        self.setDescription(description)
        self.exits = {"NORTH": None,
                      "EAST": None,
                      "SOUTH": None,
                      "WEST": None}
        self.inventory = []
        self.commands = {}
        self.doors = []
    def __repr__(self):
        """Room name, description, inventory, and exits."""
        rstring = self.name.upper() + "\n"
        rstring += (len(self.name)) * "=" + "\n"
        rstring += self.description + "\n"
        if len(self.inventory) == 1:
            rstring += "There's a {} on the floor.\n".format(self.inventory[0])
        elif len(self.inventory) > 1:
            rstring += "On the floor there are the following:\n\t"
            rstring += "\n\t".join(self.inventory)
        rstring += self.showExits()
        return rstring
    # Name methods
    def setName(self, name):
        self.name = name
    def getName(self):
        return self.name

    # Description methods
    def setDescription(self, descr):
        self.description = descr
    def getDescription(self):
        return self.description

    # Exit direction methods
    def addExit(self, direction, room):
        if direction in self.exits:
            self.exits[direction] = room
    def getExits(self):
        return list(self.exits.keys())
    def showExits(self):
        rstring = ""
        exitDirs = [ex for ex in self.exits if self.exits[ex]]
        if len(exitDirs) == 0:
            rstring += "There are no exits."
        elif len(exitDirs) > 1:
            rstring += "There are exits to the "
            rstring += ", ".join(exitDirs[:-1])
            rstring += "and {}.".format(exitDirs[-1])
        else:
            rstring += "The only exit is to the "
            rstring += exitDirs[0]
        if len(self.doors) > 1:
            rstring += "\nThere are doors to the "
            rstring += ", ".join(self.doors[:-1])
            rstring += "and {}.".format(self.doors[-1])
        else:
            rstring += "\nThere is a door to the {}.".format(self.doors[0])
        return rstring
    def exitRoom(self, direction):
        if direction in self.exits:
            if direction in self.doors:
                print("There is a door in that direction.")
                return self.getName()
            else:
                print("You go {}.".format(direction))
                return self.exits[direction]
        else:
            return False

    # Item methods
    def getItemList(self):
        return self.inventory
    def putItem(self,item):
        self.inventory.append(item)
    def removeItem(self,item):
        self.inventory.remove(item)

    # Command methods
    def addContextualCommand(self, command, action):
        self.commands[command] = action
    def performContextualCommand(self, command, argument=None):
        if command in self.commands:
            self.commands[command](argument)
        else:
            print("I do not understand.")
    def getContextualCommands(self):
        return list(self.commands.keys())

    # Door methods
    def addDoor(self, direction):
        pass

class User(object):
    def __init__(self, roomWrapper, itemWrapper, startRoom):
        self.roomWrapper = roomWrapper
        self.itemWrapper = itemWrapper
        self.room = self.roomWrapper[startRoom]
        self.health = 100
        self.inventory = []
    def __repr__(self):
        rstring = "You are in the {}\n".format(self.room.getName())
        rstring += "Your current health is {}".format(self.health)
        return rstring
    def showRoom(self):
        print(self.room)
    def showStatus(self):
        print(self)
        self.showInventory()
    def showInventory(self):
        if self.inventory:
            pstring = "You are holding:\n\t"
            pstring += "\n\t".join(self.inventory)
        else:
            pstring = "Your are holding nothing."
        print(pstring)
    def takeItem(self, item):
        if item not in self.room.getItemList():
            print("That item is not in here.")
        else:
            self.room.removeItem(item)
            self.inventory.append(item)
            print("You take {}.".format(item))
    def dropItem(self, item):
        if item not in self.inventory:
            print("You do not have that item")
        else:
            self.inventory.remove(item)
            self.room.putItem(item)
    def useItem(self, item):
        if item not in self.inventory:
            print("You do not have that item")
        elif self.itemWrapper[item].useItem():
            self.inventory.remove(item)
    def goDirection(self, direction):
        exit = self.room.exitRoom(direction)
        if exit:
            self.room = self.roomWrapper[exit]
        else:
            print("There is no exit to the {}.".format(direction))
    def showHelp(self):
        pstring = "Standard commands:\n\t"
        commands = ["LOOK",
                    "STATUS",
                    "INVENTORY",
                    "TAKE [item]",
                    "DROP [item]",
                    "USE [item]",
                    "GO [direction]",
                    "EXIT"]
        commands.extend(self.room.getContextualCommands())
        print(pstring + "\n\t".join(commands))
    def parseInput(self, userInput):
        splitInput = userInput.upper().split()
        command = splitInput[0]
        if len(splitInput) > 1:
            argument = " ".join(splitInput[1:])
        else:
            argument = None
        stdCommands = {"LOOK": self.showRoom,
                       "TAKE": self.takeItem,
                       "DROP": self.dropItem,
                       "USE": self.useItem,
                       "STATUS": self.showStatus,
                       "HELP": self.showHelp,
                       "INVENTORY": self.showInventory,
                       "I": self.showInventory,
                       "GO": self.goDirection,
                       "EXIT": sys.exit,
                       "QUIT": sys.exit}
        if command in stdCommands:
            if argument:
                stdCommands[command](argument)
            else:
                stdCommands[command]()
        elif command in self.room.getContextualCommands():
            if argument:
                self.room.performContextualCommand(command,argument)
            else:
                self.room.performContextualCommand(command)
        else:
            print("I do not understand that command.")

class Item(object):
    """Usable item."""
    def __init__(self, name, loseWhenUsed):
        self.setName(name)
        self.loseWhenUsed = loseWhenUsed
        self.useText = ""
    def setName(self, name):
        self.name = name
    def getName(self, name):
        return self.name
    def setUseText(self, text):
        self.useText = text
    def use(self):
        if self.useText:
            print(self.useText)
        else:
            print("You use the {}.")
        return self.loseWhenUsed

class Beast(object):
    def __init__(self, name, health):
        pass
