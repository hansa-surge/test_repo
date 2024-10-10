import csv
from typing import List
from items import Item

class Container:
    def __init__(self, name: str, container_weight: int, weight_capacity: int):
        self.name:str = name
        self.container_weight:int = container_weight
        self.weight_capacity:int = weight_capacity

        self.items:List[Item] = [] 

    def __str__(self) -> str:
        return (f"{self.name} (total weight: {self.get_current_weight()}, "
                f"empty weight: {self.container_weight}, capacity: {self.get_current_weight()}/{self.weight_capacity})")
    
    @classmethod
    def load_items(cls, file_path: str) -> 'Container':
        instance = cls()  # Create a new instance of Items
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the first row (header)
            for row in reader:  # Process items
                name, weight = row
                instance.add_item(Item(name, int(weight)))  # Use instance's items
        return instance  # Return the created instance
    
    def add_item(self, item: Item):
        if item.weight + self.get_current_weight() <= self.weight_capacity:
            self.items.add_item(item)
            self.current_weight += item.weight
            print(f"Success! Item \"{item.name}\" stored in \"{self.name}\".")
        else:
            print(f"Failure! Item \"{item.name}\" NOT stored in container \"{self.name}\".")

    def add_items(self, items: List[Item]):
        for item in items:
            self.add_item(item)
    
    def get_current_weight(self):
        current_weight = self.container_weight
        for item in self.items:
            print(item)
            current_weight += item.weight
        return current_weight

    def list_items(self):
            print(f"{self.name} (total weight: {self.get_current_weight()}, empty weight: {self.container_weight}, capacity: {self.get_current_weight()}/{self.weight_capacity})")
            for item in self.items:
                print(f"   {item}")

    def print_items(self):
        for item in sorted(self.items, key=lambda x: x.name):
            print(item)

    def get_item_by_name(self, item_name):
        for item in self.items:
            if item.name == item_name:
                return item
            
    def get_items(self) -> List[Item]:
        return self.items
    
    def get_count(self) -> int:
        return len(self.items)

class ContainerManager:
    def __init__(self):
        self.containers: List[Container] = []  # Initialize as an empty list

    @classmethod
    def load_containers(cls, file_path: str) -> 'ContainerManager':
        instance = cls()  # Create a new instance of Containers
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the first row (header)
            for row in reader:  # Process containers
                name, empty, capacity = row
                instance.containers.append(Container(name, int(empty), int(capacity)))  # Use instance's containers
        return instance  # Return the created instance

    def print_containers(self):
        for container in sorted(self.containers, key=lambda x: x.name):
            print(container)
    
    def add_container(self, containers: List[Container]):
        self.containers.extend(containers)  # Add loaded containers to the list
            
    def get_containers(self) -> List[Container]:
        return self.containers
    
    def get_container_by_name(self, container_to_find:str) -> List[Container]:
        for container in self.containers:
            if container.name.strip().lower() == container_to_find.strip().lower():
                return container
        return None
    
    def get_count(self) -> int:
        return len(self.containers)
