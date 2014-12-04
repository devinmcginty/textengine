import engine

class Key(engine.Item):
    """Usable item."""
    def __init__(self):
        super(Key, self).__init__("Gold Key",True)
        useText = "You insert the key into the keyhole and turn it."
        self.setUseText(useText)
