import engine

class MainHall(engine.Room):
    def __init__(self):
        name = "Main Hall"
        description = "This is a dark humid corridor."
        super(MainHall, self).__init__(name, description)
        exits = {"NORTH": "Parlour",
                 "EAST": "Vestibule",
                 "WEST": "Library",
                 "SOUTH": "Dining Room"}
        self.addExits(exits)

class Library(engine.Room):
    def __init__(self):
        name = "Library"
        description = "This room smells like sawdust and mildew."
        description += "It looks like a flood destroyed most of the books."
        super(Library, self).__init__(name, description)
        self.addExits({"EAST": "Main Hall"})
        self.putItem("YE FLASK")
    def takeItem(self, item):
        if item == "YE FLASK":
            print("You cannot take YE FLASK")
        else:
            super(Library, self).takeItem()

class Parlour(engine.Room):
    def __init__(self):
        name = "Parlour"
        description = "This room is full of dust.\n"
        description += "It looks like nobody has been here for quite some time."
        description += "There's a big red button that says \"Do not push\"."
        super(Parlour, self).__init__(name, description)
        self.addExit({"SOUTH","Main Hall"})
        def pushButton(button = None):
            if button == "BUTTON":
                print("You die.")
                engine.exit(0)
            else:
                print("What are you trying to push?")
        self.addContextualCommand("PUSH", pushButton)

class Vestibule(engine.Room):
    def __init__(self):
        name = "Vestibule"
        description = "This is a brightly lit room filled with dirty windows."
        super(Vestibule, self).__init__(name, description)
        exits = {"WEST": "Main Hall",
                 "EAST": "Exit"}
        self.addExits(exits)

class DiningRoom(engine.Room):
    def __init__(self):
        name = "Dining Room"
        description = "There is a long table in the middle of the room."
        description += "Broken chairs lean against the walls in splinters."
        super(DiningRoom, self).__init__(name, description)
        exits = {"NORTH": "Main Hall",
                 "WEST": "Kitchen"}
        self.addExits(exits)

class Kitchen(engine.Room):
    def __init__(self):
        name = "Kitchen"
        description = "This kitchen clearly has not been used in some time."
        super(Kitchen, self).__init__(name, description)
        self.addExits({"EAST": "Dining Room"})
