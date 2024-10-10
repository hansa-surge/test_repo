import csv
from typing import List

class Container:
    def __init__(self, name: str, empty: int, capacity: int):
        self.initial = 0
        self.name = name
        self.empty = empty
        self.capacity = capacity

    def __str__(self) -> str:
        return (f"{self.name} (total weight: {self.empty + self.initial}, "
                f"empty weight: {self.empty}, capacity: {self.initial}/{self.capacity})")

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
    
    def get_count(self) -> int:
        return len(self.containers)
