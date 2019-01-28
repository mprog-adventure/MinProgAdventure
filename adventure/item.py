class Item(object):
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __str__(self):
        return f"{self.name.upper()}: {self.description}"
