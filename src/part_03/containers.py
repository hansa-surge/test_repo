import csv
import copy
from typing import List
from items import Item

class Container(Item):
    def __init__(self, name: str, weight: int, weight_capacity: int):
        super().__init__(name, weight)
        self.weight_capacity = weight_capacity
        self.items: List[Item] = []
        self.is_multi_container = False

    def __str__(self) -> str:
        capacity_display = f"{self.get_current_weight()}/{self.weight_capacity}"
        if self.is_multi_container:
            capacity_display = "0/0"
        return (f"{self.name} (total weight: {self.get_current_weight()}, "
                f"empty weight: {self.weight}, capacity: {capacity_display})")

    @classmethod
    def load_items(cls, file_path: str = None, items: List[Item] = None) -> 'Container':
        instance = cls("", 0, 0)
        if file_path:
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                next(reader)
                for name, weight in reader:
                    instance.add_item(Item(name, int(weight)))
        if items:
            for item in items:
                instance.add_item(item)
        return instance

    def add_item(self, item: Item):
        if isinstance(item, Container):
            self.items.append(item)
            self.is_multi_container = True
            self.weight += item.get_current_weight()
            self.weight_capacity += item.weight_capacity
        else:
            for container in self.items:
                if(isinstance(container, Container)):
                    if(container.add_item(item)):
                        return True
                
            if item.get_current_weight() + self.get_current_weight() <= self.weight_capacity - self.get_child_container_capacity():
                self.items.append(item)
                print(f"Success! Item \"{item.name}\" stored in container \"{self.name}\".")
            else:
                print(f"Failure! Item \"{item.name}\" NOT stored in container \"{self.name}\".")
                return False
        return True

    def add_items(self, items: List[Item]):
        for item in items:
            self.add_item(item)

    def get_child_container_capacity(self):
        return sum(item.weight_capacity for item in self.items if isinstance(item, Container))

    def get_current_weight(self):
        print()
        weight = 0
        for item in self.items:
            print("item: ", item)
            weight += item.get_current_weight()
            print("new_weight: ", weight)
        self.weight + weight

    def list_items(self, depth=1):
        print(self)
        for item in sorted(self.items, key=lambda x: x.name):
            indent = "   " * depth
            if isinstance(item, Container):
                print(indent, end="")
                item.list_items(depth + 1)
            else:
                print(f"{indent}{item.name} (weight: {item.weight})")

    def get_item_by_name(self, name: str) -> Item:
        return next((item for item in self.items if item.name == name), None)

    def get_items(self) -> List[Item]:
        return self.items

    def get_count(self) -> int:
        return len(self.items)

class ContainerManager:
    def __init__(self):
        self.containers: List[Container] = []  # Initialize as an empty list

    @classmethod
    def load_containers(cls, file_path: str) -> 'ContainerManager':
        instance = cls()  # Create a new instance of ContainerManager
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            instance.containers = [
                Container(name, int(empty), int(capacity))
                for name, empty, capacity in reader  # Use list comprehension
            ]
        return instance

    @classmethod
    def load_multi_containers(cls, containers_file_path: str, multi_container_file_path: str) -> 'ContainerManager':
        instance = cls.load_containers(containers_file_path)  # Load containers
        with open(multi_container_file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                mother_container = Container(row[0], 0, 0)  # First entry is mother container name
                for child_name in row[1:]:
                    child_container = instance.get_container_by_name(child_name)
                    if child_container:
                        mother_container.add_item(child_container)
                instance.containers.append(mother_container)
        return instance

    def print_containers(self):
        for container in sorted(self.containers, key=lambda x: x.name):
            container.list_items()  # Assuming `Container` class has print_items()

    def add_container(self, containers: List[Container]):
        self.containers.extend(containers)

    def get_containers(self) -> List[Container]:
        return self.containers

    def get_container_by_name(self, container_name: str) -> Container:
        for container in self.containers:
            if container.name.strip().lower() == container_name.strip().lower():
                return copy.deepcopy(container)
        return None

    def get_count(self) -> int:
        return len(self.containers)
