# Inventory Class
# needs more attributes/variables and functions

class Item:
    def __init__(self):
        self.name = ""
        self.description = ""
        self.tyoe = ""

    def set_name(self, new_name):
        self.name = new_name

    def set_description(self, new_des):
        self.description = new_des

    def set_type(self, new_type):
        self.type = new_type

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_type(self):
        return self.type

class Inventory:
    def __init__(self):
        self.items = {}

    def add(self, item):
        if item in self.items:
            self.items[item] += 1
        else
            self.items[item] = 1

    def remove(self, item):
        if item in self.items:
            if self.items[item] == 1
                del self.items[item]
            else
                self.items[item] -= 1
