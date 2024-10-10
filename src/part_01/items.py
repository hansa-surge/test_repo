import csv
from typing import List

class Item:
    def __init__(self, name: str, weight: int):
        self.name = name
        self.weight = weight

    def __str__(self) -> str:
        return f"{self.name} (weight: {self.weight})"

class ItemManager:
    def __init__(self):
        self.items: List[Item] = []  # Initialize as an empty list

    @classmethod
    def load_items(cls, file_path: str) -> 'ItemManager':
        instance = cls()  # Create a new instance of Items
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the first row (header)
            for row in reader:  # Process items
                name, weight = row
                instance.items.append(Item(name, int(weight)))  # Use instance's items
        return instance  # Return the created instance
    
    def add_items(self, items: List[Item]):
        self.items.extend(items)  # Add loaded items to container
        
    def print_items(self):
        for item in sorted(self.items, key=lambda x: x.name):
            print(item)
            
    def get_items(self) -> List[Item]:
        return self.items
    
    def get_count(self) -> int:
        return len(self.items)
