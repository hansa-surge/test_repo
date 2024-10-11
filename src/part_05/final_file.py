import csv
import copy
from typing import List

# Abstract class for screens that display a menu and handle user choices
class Screen:
    def display_menu(self):
        # To be overridden by subclasses, defines what to show on the screen
        raise NotImplementedError("This method should be overridden by subclasses.")

    def get_choice(self):
        # Get the user's choice from input
        return input("")

    def handle_choice(self, choice):
        # To be overridden by subclasses, defines how to handle user input
        raise NotImplementedError("This method should be overridden by subclasses.")

    def run(self):
        # Run a loop where the screen is displayed and the user makes choices
        while True:
            self.display_menu()
            choice = self.get_choice()
            out = self.handle_choice(choice)
            if(out):
                break
        return out

# Class representing an item with a name and weight
class Item:
    def __init__(self, name: str, weight: int):
        self.name = name
        self.weight = weight

    def __str__(self) -> str:
        # String representation of an item
        return f"{self.name} (weight: {self.get_current_weight()})"
    
    def get_current_weight(self):
        # Return the item's current weight
        return self.weight
    
    def get_item_weight(self):
        # Return the weight of the item
        return self.weight

# Class representing a container, which can hold other items
class Container(Item):
    def __init__(self, name: str, weight: int, weight_capacity: int):
        # Initialize container with a name, weight, and capacity
        super().__init__(name, weight)
        self.weight_capacity = weight_capacity
        self.items: List[Item] = []
        self.is_multi_container = False

    def __str__(self) -> str:
        # String representation of a container
        capacity_display = f"{self.get_current_capacity()}/{self.weight_capacity}"
        if self.is_multi_container:
            capacity_display = "0/0"
        return (f"{self.name} (total weight: {self.get_current_weight()}, "
                f"empty weight: {self.weight}, capacity: {capacity_display})")

    @classmethod
    def load_items(cls, file_path: str = None, items: List[Item] = None) -> 'Container':
        # Load items from a file or a list of items into a container
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

    def add_item(self, item: Item, parent_container_name = None):
        # Add an item to the container, handling capacity constraints
        if isinstance(item, Container):
            # Add container within container (nested containers)
            self.items.append(item)
            self.is_multi_container = True
            self.weight += item.get_current_weight()
            self.weight_capacity += item.weight_capacity
        else:
            for container in self.items:
                if(isinstance(container, Container)):
                    if(item.get_current_weight() + container.get_current_capacity() <= container.weight_capacity - container.get_child_container_capacity()):
                        container.add_item(item, self.name)
                        return True
                
            if item.get_current_weight() + self.get_current_capacity() <= self.weight_capacity - self.get_child_container_capacity():
                self.items.append(item)
                if(parent_container_name):
                    print(f"Success! Item \"{item.name}\" stored in container \"{parent_container_name}\".")
                else:
                    print(f"Success! Item \"{item.name}\" stored in container \"{self.name}\".")
            else:
                print(f"Failure! Item \"{item.name}\" NOT stored in container \"{self.name}\".")
                return False
        return True

    def add_items(self, items: List[Item]):
        # Add multiple items to the container
        for item in items:
            self.add_item(item)

    def get_child_container_capacity(self):
        # Get total capacity of child containers
        return sum(item.weight_capacity for item in self.items if isinstance(item, Container))

    def get_current_weight(self):
        # Get total weight of the container including its items
        return self.weight + sum(item.get_item_weight() for item in self.items)
    
    def get_item_weight(self):
        # Get total weight of all items excluding containers
        return sum(item.get_current_weight() for item in self.items if not isinstance(item, Container))
    
    def get_current_capacity(self):
        # Get current capacity of the container based on items
        return sum(item.get_current_weight() for item in self.items if not isinstance(item, Container))

    def list_items(self, depth=1):
        # List items in the container (recursive if nested containers)
        print(self)
        for item in self.items:
            indent = "   " * depth
            if isinstance(item, Container):
                print(indent, end="")
                item.list_items(depth + 1)
            else:
                print(f"{indent}{item.name} (weight: {item.weight})")

    def get_item_by_name(self, name: str) -> Item:
        # Retrieve an item from the container by its name
        return next((item for item in self.items if item.name == name), None)

    def get_items(self) -> List[Item]:
        # Return all items in the container
        return self.items

    def get_count(self) -> int:
        # Return the number of items in the container
        return len(self.items)

# Manager for handling items
class ItemManager:
    def __init__(self):
        self.items: List[Item] = []  # Initialize as an empty list

    @classmethod
    def load_items(cls, file_path: str) -> 'ItemManager':
        # Load items from a CSV file
        instance = cls()  # Create a new instance of Items
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the first row (header)
            for row in reader:  # Process items
                name, weight = row
                instance.items.append(Item(name, int(weight)))  # Use instance's items
        return instance  # Return the created instance
    
    def add_items(self, items: List[Item]):
        # Add loaded items to the container
        self.items.extend(items)
        
    def print_items(self):
        # Print all items in the manager
        for item in self.items:
            print(item)
            
    def get_items(self) -> List[Item]:
        # Return a list of items in the manager
        return self.items
    
    def get_item_by_name(self, item_to_find) -> List[Item]:
        # Retrieve an item by name
        for item in self.items:
            if item.name.strip().lower() == item_to_find.strip().lower():
                return item
        return None
    
    def get_count(self) -> int:
        # Return the total number of items
        return len(self.items)

# A special type of container that doesn't increase in weight when items are added
class MagicContainer(Container):
    def __init__(self, name: str, weight: int, weight_capacity: int):
        super().__init__(name, weight, weight_capacity)

    def add_item(self, item: Item, parent_container_name = None):
        # Add item to the magic container
        if isinstance(item, Container):
            self.items.append(item)
            self.is_multi_container = True
            self.weight_capacity += item.weight_capacity
        else:
            for container in self.items:
                if(isinstance(container, Container)):
                    if(container.get_current_capacity() + item.get_current_weight() <= container.weight_capacity - container.get_child_container_capacity() or isinstance(item, Container)):
                        container.add_item(item, self.name)
                        return True
                
            if self.get_current_capacity() + item.get_current_weight() <= self.weight_capacity - self.get_child_container_capacity():
                self.items.append(item)
                if(parent_container_name):
                    print(f"Success! Item \"{item.name}\" stored in container \"{parent_container_name}\".")
                else:
                    print(f"Success! Item \"{item.name}\" stored in container \"{self.name}\".")
            else:
                print(f"Failure! Item \"{item.name}\" NOT stored in container \"{self.name}\".")
                return False
        return True
    
    @classmethod
    def convert_container_to_magic(cls, container: Container, magic_name):
        # Convert a regular container to a magic container
        instance = cls(magic_name, container.weight, container.weight_capacity)
        instance.is_multi_container = container.is_multi_container
        instance.items = container.items
        return instance
    
    def get_current_capacity(self):
        # Return the current capacity (ignores weight of items)
        return sum(item.get_current_weight() for item in self.items if not isinstance(item, Container))

    def get_current_weight(self):
        # Return the weight of the magic container (ignores item weight)
        return self.weight

    def __str__(self) -> str:
        # String representation of a magic container
        capacity_display = f"{self.get_current_capacity()}/{self.weight_capacity}"
        if self.is_multi_container:
            capacity_display = "0/0"
        return (f"{self.name} (total weight: {self.get_current_weight()}, "
                f"empty weight: {self.weight}, capacity: {capacity_display})")

class ContainerManager:
    def __init__(self):
        self.containers: List[Container] = []  # Initialize as an empty list of containers

    @classmethod
    def load_containers(cls, containers_file_path: str = None, multi_container_file_path: str = None, magic_container_file_path: str = None, multi_magic_container_file_path: str = None) -> 'ContainerManager':
        instance = cls()  # Create a new instance of ContainerManager

        # Load regular containers from a CSV file if the path is provided
        if containers_file_path:
            with open(containers_file_path, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header row
                instance.containers = [
                    Container(name, int(empty), int(capacity))  # Create Container objects from CSV data
                    for name, empty, capacity in reader
                ]

        # Load multi-containers (containers within containers) if the file path is provided
        if multi_container_file_path:
            with open(multi_container_file_path, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header row
                for row in reader:
                    mother_container = Container(row[0], 0, 0)  # The first entry is the name of the mother container
                    for child_name in row[1:]:  # The rest are child containers
                        child_container = instance.get_container_by_name(child_name)
                        if child_container:
                            mother_container.add_item(child_container)  # Add child containers to the mother container
                    instance.containers.append(mother_container)  # Add mother container to the list

        # Load magic containers if the file path is provided
        if magic_container_file_path:
            with open(magic_container_file_path, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header row
                for row in reader:
                    magic_container_name, container_name = row
                    normal_container = instance.get_container_by_name(container_name)  # Find the regular container
                    if normal_container:
                        magic_container = MagicContainer.convert_container_to_magic(normal_container, magic_container_name)  # Convert to magic container
                        instance.containers.append(magic_container)  # Add magic container to the list

        # Load multi-magic containers (containers containing magic containers) if the file path is provided
        if multi_magic_container_file_path:
            with open(multi_magic_container_file_path, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header row
                for row in reader:
                    magic_container_name, container_name = row
                    normal_container = instance.get_container_by_name(container_name)  # Find the regular container
                    if normal_container:
                        magic_container = MagicContainer.convert_container_to_magic(normal_container, magic_container_name)  # Convert to magic container
                        instance.containers.append(magic_container)  # Add magic container to the list

        return instance  # Return the populated ContainerManager instance

    def print_containers(self):
        # Print a list of items in each container
        for container in self.containers:
            container.list_items()  # Assuming `Container` class has `list_items()` to display contents

    def add_container(self, containers: List[Container]):
        # Add a list of containers to the manager's container list
        self.containers.extend(containers)

    def get_containers(self) -> List[Container]:
        # Return the list of all containers
        return self.containers

    def get_container_by_name(self, container_name: str) -> Container:
        # Search for a container by its name (case-insensitive)
        for container in self.containers:
            if container.name.strip().lower() == container_name.strip().lower():
                return copy.deepcopy(container)  # Return a copy of the container to avoid modifying the original
        return None  # Return None if no container is found

    def get_count(self) -> int:
        # Return the number of containers managed by the instance
        return len(self.containers)


def print_items_and_containers(items: ItemManager, containers: ContainerManager):
    # Print the total number of items and containers initialized
    print(f"Initialised {items.get_count() + containers.get_count()} items including {containers.get_count()} containers.\n")

    # Print the list of items
    print("Items:")
    items.print_items()

    # Print the list of containers
    print("\nContainers:")
    containers.print_containers()


class ContainerSelectScreen(Screen):
    def __init__(self, containers: ContainerManager) -> None:
        super().__init__()
        self.containers: ContainerManager = containers  # Store the reference to ContainerManager

    def display_menu(self):
        # Placeholder for a display menu (not implemented)
        return

    def get_choice(self):
        # Prompt the user to enter the name of the container
        return input("Enter the name of the container: ")

    def handle_choice(self, choice):
        # Handle the user's choice by finding the corresponding container
        container = self.containers.get_container_by_name(choice)
        if container:
            return container  # Return the selected container if found
        else:
            print(f"\"{choice}\" not found. Try again.")  # Inform the user if the container is not found


class MainMenu(Screen):
    def __init__(self, items: ItemManager = None, container: Container = None) -> None:
        super().__init__()
        self.items: ItemManager = items  # Store reference to the ItemManager
        self.container: Container = container  # Store reference to the selected container

    def display_menu(self):
        # Display the main menu options
        print("==================================")
        print("Enter your choice:")
        print("1. Loot item.")
        print("2. List looted items.")
        print("0. Quit.")
        print("==================================")

    def handle_choice(self, choice):
        # Handle the user's choice from the menu
        if choice == "1":
            self.handle_loot_item()  # Loot an item
        elif choice == "2":
            self.list_looted_items()  # List all looted items
        elif choice == "0":
            exit()  # Quit the program
        else:
            print("Invalid choice. Try again.")  # Handle invalid input

    def handle_loot_item(self):
        """Loot an item by asking the user for the item name."""
        while True:
            item_name = input("Enter the name of the item: ")
            item = self.items.get_item_by_name(item_name)  # Find the item by name

            if item:
                self.container.add_item(item)  # Add the item to the container
                break  # Exit the loop once the item is looted
            else:
                print(f"\"{item_name}\" not found. Try again.")  # Inform the user if the item is not found

    def list_looted_items(self):
        """List all the looted items."""
        self.container.list_items()  # List items in the selected container


def gameloop():
    # Load items and containers from CSV files
    items = ItemManager.load_items('items.csv')
    containers = ContainerManager.load_containers('containers.csv', 'multi_containers.csv', 'magic_containers.csv', 'magic_multi_containers.csv')

    # Print the initialized items and containers
    print(f"Initialised {items.get_count() + containers.get_count()} items including {containers.get_count()} containers.\n")

    # Game Loop: Select a container and display the main menu
    container = ContainerSelectScreen(containers).run()
    MainMenu(items, container).run()


if __name__ == "__main__":
    # Start the game loop
    gameloop()

    