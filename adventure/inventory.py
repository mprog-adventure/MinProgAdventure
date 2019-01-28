class Inventory():
    def __init__(self):
        self.items = {}

    def add(self, item):
        self.items[item.name] = item

    def remove(self, item_name):
        return self.items.pop(item_name)

    def count(self):
        return len(self.items.keys())

    def has(self, item_name):
        return item_name in self.items

    def give(self, item_name):
        return self.remove(item_name)

    def __str__(self):
        items = ""
        for key, value in self.items.items():
            items += f"{key.upper()}: {value.description}\n"
        if items == "":
            return "Your inventory is empty."
        return items.strip()
