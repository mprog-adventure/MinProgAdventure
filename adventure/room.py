from .inventory import Inventory


class Room(object):
    """
    Representation of a room in Adventure
    """

    def __init__(self, id, name, description, connections):
        """
        Initialize a Room
        give it an id, name and description
        """
        self.id = id
        self.name = name
        self.description = description
        self.connections = connections
        self.visited = False
        self.inventory = Inventory()

    def __str__(self):
        if self.visited:
            return f"{self.name}"
        else:
            self.visited = True
            return self.display()

    def display(self):
        if self.inventory.count() > 0:
            return f"{self.description}\n{self.inventory}"
        else:
            return f"{self.description}"

    def valid_move(self, direction):
        return direction in self.connections

    def connected(self, direction):
        return self.connections[direction]

    def is_forced(self):
        return self.connections.get("forced")

    def has(self, item_name):
        return self.inventory.has(item_name)

    def add(self, item):
        self.inventory.add(item)

    def give(self, item_name):
        return self.inventory.remove(item_name)
