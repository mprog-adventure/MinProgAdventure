# Import own modules.
from .room import Room
from .item import Item
from .inventory import Inventory

# Import external libraries.
from collections import defaultdict


class Adventure():
    """
    This is your Adventure game class. It should contains
    necessary attributes and methods to setup and play
    Crowther's text based RPG Adventure.
    """
    def __init__(self, game):
        """
        Create rooms and items for the appropriate 'game' version.
        """
        self.rooms = self.load_rooms(f"/app/data/{game}Rooms.txt")
        self.items = self.load_items(f"/app/data/{game}Items.txt")
        self.current_room = self.rooms[1]
        self.items = Inventory()
        self.synonyms = self.load_synonyms("/app/data/SmallSynonyms.txt")

    def load_synonyms(self, filename):
        with open(filename, "r") as f:
            synonyms = {}
            for line in f:
                key, value = line.strip().lower().split('=')
                synonyms[key] = value

        return synonyms

    def load_rooms(self, filename):
        """
        Load rooms from filename.
        Returns a collection of Room objects.
        """
        rooms = [Room(0, "Game over", "Game over", {})]
        rooms += self.construct_rooms(filename)
        self.update_rooms(rooms)

        return rooms

    def load_items(self, filename):
        """
        Load rooms from filename.
        Returns a collection of Room objects.
        """
        items = self.construct_items(filename)

        return items

    def read_file(self, filename):
        with open(filename, "r") as f:
            lines = []
            for line in f:
                if not line == "\n":
                    lines.append(line.strip())
                else:
                    yield lines
                    lines = []

            # Add final item due to bad code.
            yield lines

    def construct_items(self, filename):
        items = []
        for lines in self.read_file(filename):
            name = lines[0].lower()
            description = lines[1]
            location = int(lines[2])

            item = Item(name, description)
            self.rooms[location].add(item)
            items.append(item)

        return items

    def construct_rooms(self, filename):
        rooms = []
        for lines in self.read_file(filename):
            id = lines[0]
            name = lines[1]
            description = lines[2]
            routes = lines[3:]
            connections = defaultdict(list)

            # Setup routes from room and split for conditional moves.
            for route in routes:
                if route == "-----":
                    continue
                key, value = route.lower().split()
                connections[key.lower()].append(tuple(value.split("/")))

            rooms.append(Room(id, name, description, connections))

        return rooms

    def update_rooms(self, rooms):
        """
        Replaces room_ids in room connection dicts for actual room objects.
        """
        for room in rooms:
            for direction, connections in room.connections.items():
                values = []
                for connection in connections:
                    if len(connection) == 2:
                        values.append((rooms[int(connection[0])],
                                      connection[1]))
                    else:
                        values.append((rooms[int(connection[0])], None))
                room.connections[direction] = values

    def game_over(self):
        """
        Check if the game is over.
        Returns a boolean.
        """
        return self.current_room.id == 0

    def move(self, direction):
        """
        Moves to a different room in the specified direction.
        """
        for connection, item in self.current_room.connected(direction):
            if not item or self.items.has(item):
                self.current_room = connection
                return

    def help(self):
        print("You can move by typing directions such as EAST/WEST/IN/OUT\n"
              "QUIT quits the game.\n"
              "HELP prints instructions for the game.\n"
              "INVENTORY lists the item in your inventory.\n"
              "LOOK lists the complete description of the "
              "room and its contents.\n"
              "TAKE <item> take item from the room.\n"
              "DROP <item> drop item from your inventory.")

    def quit(self):
        print("Thanks for playing!")
        exit(0)

    def look(self):
        print(self.current_room.display())

    def inventory(self):
        print(self.items)

    def move_item(self, item_name, giver, taker):
        if giver.has(item_name):
            item = giver.give(item_name)
            taker.add(item)
            return True
        else:
            print("No such item.")
            return False

    def take(self, item_name):
        if self.move_item(item_name, self.current_room, self.items):
            print(f"{item_name.upper()} taken.")

    def drop(self, item_name):
        if self.move_item(item_name, self.items, self.current_room):
            print(f"{item_name.upper()} dropped.")

    def display_current_room(self):
        if self.current_room.is_forced():
            print(self.current_room.display())
        else:
            print(self.current_room)

    def get_command(self):
        command = input("> ").lower()
        commands = command.split()
        item_name = ""

        if len(commands) == 2:
            item_name = commands[1]
            command = commands[0]

        if command in self.synonyms:
            command = self.synonyms[command]

        return command, item_name

    def play(self):
        """
        Play an Adventure game
        """
        print(f"Welcome, to the Adventure games.\n"
              "May the randomly generated numbers be ever in your favour.\n")

        self.display_current_room()

        # Prompt the user for commands until the game is over.
        while not self.game_over():
            command, item_name = self.get_command()

            # Check if the command is a movement or not.
            if self.current_room.valid_move(command):
                self.move(command)
                self.display_current_room()

            elif command in ["help", "look", "quit", "inventory"]:
                getattr(self, command)()

            elif command in ["take", "drop"]:
                getattr(self, command)(item_name)

            else:
                print("Invalid command.")

            while self.current_room.is_forced():
                self.move('forced')
                self.display_current_room()
