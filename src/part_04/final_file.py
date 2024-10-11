import csv
import copy
from typing import List

class Screen:
    # Base class for the different screen interfaces in the game.
    def display_menu(self):
        raise NotImplementedError("This method should be overridden by subclasses.")

    def get_choice(self):
        # Collect user input for menu selection.
        return input("")

    def handle_choice(self, choice):
        raise NotImplementedError("This method should be overridden by subclasses.")

    def run(self):
        # Main loop to run the screen and process user choices.
        while True:
            self.display_menu()  # Show the menu options
            choice = self.get_choice()  # Get user input
            out = self.handle_choice(choice)  # Handle user input
            if out:
                break  # Exit loop if necessary
        return out  # Return the final choice

class Item:
    # Represents an item with a name and weight.
    def __init__(self, name: str, weight: int):
        self.name = name
        self.weight = weight

    def __str__(self) -> str:
        # Display the item details.
        return f"{self.name} (weight: {self.get_current_weight()})"
    
    def get_current_weight(self):
        # Return the current weight of the item.
        return self.weight
    
    def get_item_weight(self):
        # Same as current weight for basic items.
        return self.weight

class Container(Item):
    # Represents a container that can hold multiple items and has a weight capacity.
    def __init__(self, name: str, weight: int, weight_capacity: int):
        super().__init__(name, weight)
        self.weight_capacity = weight_capacity
        self.items: List[Item] = []  # Initialize with an empty list of items
        self.is_multi_container = False  # Track if this container can hold other containers

    def __str__(self) -> str:
        # Display container details including current capacity and weight.
        capacity_display = f"{self.get_current_capacity()}/{self.weight_capacity}"
        if self.is_multi_container:
            capacity_display = "0/0"  # Special handling for multi containers
        return (f"{self.name} (total weight: {self.get_current_weight()}, "
                f"empty weight: {self.weight}, capacity: {capacity_display})")

    @classmethod
    def load_items(cls, file_path: str = None, items: List[Item] = None) -> 'Container':
        # Load items into a container either from a CSV file or from a given list.
        instance = cls("", 0, 0)
        if file_path:
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                for name, weight in reader:
                    instance.add_item(Item(name, int(weight)))
        if items:
            for item in items:
                instance.add_item(item)
        return instance

    def add_item(self, item: Item, parent_container_name=None):
        # Add an item to the container, checking weight capacity.
        if isinstance(item, Container):
            self.items.append(item)
            self.is_multi_container = True  # Mark as multi container
            self.weight += item.get_current_weight()
            self.weight_capacity += item.weight_capacity
        else:
            # Check if the item can fit into a nested container.
            for container in self.items:
                if isinstance(container, Container):
                    if (item.get_current_weight() + container.get_current_capacity() 
                            <= container.weight_capacity - container.get_child_container_capacity()):
                        container.add_item(item, self.name)
                        return True

            # Check if the item can fit into this container.
            if item.get_current_weight() + self.get_current_capacity() <= self.weight_capacity - self.get_child_container_capacity():
                self.items.append(item)
                if parent_container_name:
                    print(f"Success! Item \"{item.name}\" stored in container \"{parent_container_name}\".")
                else:
                    print(f"Success! Item \"{item.name}\" stored in container \"{self.name}\".")
            else:
                print(f"Failure! Item \"{item.name}\" NOT stored in container \"{self.name}\".")
                return False
        return True

    def add_items(self, items: List[Item]):
        # Add a list of items to the container.
        for item in items:
            self.add_item(item)

    def get_child_container_capacity(self):
        # Calculate the capacity taken by child containers.
        return sum(item.weight_capacity for item in self.items if isinstance(item, Container))

    def get_current_weight(self):
        # Calculate the current weight of the container including its contents.
        return self.weight + sum(item.get_item_weight() for item in self.items)
    
    def get_item_weight(self):
        # Calculate the total weight of items in the container (excluding child containers).
        return sum(item.get_current_weight() for item in self.items if not isinstance(item, Container))
    
    def get_current_capacity(self):
        # Calculate the current used capacity of the container.
        return sum(item.get_current_weight() for item in self.items if not isinstance(item, Container))

    def list_items(self, depth=1):
        # Recursively list all items in the container.
        print(self)
        for item in self.items:
            indent = "   " * depth  # Indentation for nested items
            if isinstance(item, Container):
                print(indent, end="")
                item.list_items(depth + 1)  # Recursively list items in child containers
            else:
                print(f"{indent}{item.name} (weight: {item.weight})")

    def get_item_by_name(self, name: str) -> Item:
        # Find an item by its name.
        return next((item for item in self.items if item.name == name), None)

    def get_items(self) -> List[Item]:
        # Return a list of all items in the container.
        return self.items

    def get_count(self) -> int:
        # Return the total number of items in the container.
        return len(self.items)
class ItemManager:
    def __init__(self):
        self.items: List[Item] = []  # Initialize an empty list to store Item objects

    @classmethod
    def load_items(cls, file_path: str) -> 'ItemManager':
        """Loads items from a CSV file and returns an instance of ItemManager."""
        instance = cls()  # Create a new instance of ItemManager
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            for row in reader:  # Iterate over rows and create items
                name, weight = row
                instance.items.append(Item(name, int(weight)))  # Append Item to the list
        return instance  # Return the populated instance

    def add_items(self, items: List[Item]):
        """Add multiple items to the ItemManager."""
        self.items.extend(items)  # Extend the list with new items

    def print_items(self):
        """Print all items in the ItemManager."""
        for item in self.items:
            print(item)

    def get_items(self) -> List[Item]:
        """Return a list of all items."""
        return self.items

    def get_item_by_name(self, item_to_find) -> List[Item]:
        """Find and return an item by its name."""
        for item in self.items:
            if item.name.strip().lower() == item_to_find.strip().lower():
                return item  # Return the matching item
        return None  # Return None if no match is found

    def get_count(self) -> int:
        """Return the total number of items."""
        return len(self.items)

class MagicContainer(Container):
    def __init__(self, name: str, weight: int, weight_capacity: int):
        super().__init__(name, weight, weight_capacity)
        self.magic_capacity_filled = 0  # Track the current filled capacity of the magic container

    def add_item(self, item: Item):
        """Add an item to the container, or delegate to child containers if needed."""
        if isinstance(item, Container):
            # Add a container inside this container and adjust the weight capacity
            self.items.append(item)
            self.is_multi_container = True
            self.weight_capacity += item.weight_capacity
        else:
            # Try adding to child containers first
            for container in self.items:
                if isinstance(container, Container):
                    return container.add_item(item)
            # Add item if it fits in this container
            if self.get_magic_capacity_filled() + item.get_current_weight() <= self.weight_capacity - self.get_child_container_capacity():
                self.items.append(item)
                print(f"Success! Item \"{item.name}\" stored in container \"{self.name}\".")
            else:
                print(f"Failure! Item \"{item.name}\" NOT stored in container \"{self.name}\".")
                return False
        return True

    @classmethod
    def convert_container_to_magic(cls, container: Container, magic_name):
        """Convert a regular container into a magic container."""
        return cls(magic_name, container.weight, container.weight_capacity)

    def get_magic_capacity_filled(self):
        """Calculate the filled capacity based on the weight of stored items."""
        return sum(item.get_current_weight() for item in self.items if not isinstance(item, Container))

    def get_current_weight(self):
        """Return the container's current weight."""
        return self.weight

    def __str__(self) -> str:
        """Return a string representation of the container."""
        capacity_display = f"{self.get_magic_capacity_filled()}/{self.weight_capacity}"
        return (f"{self.name} (total weight: {self.get_current_weight()}, "
                f"empty weight: {self.weight}, capacity: {capacity_display})")

class ContainerManager:
    def __init__(self):
        self.containers: List[Container] = []  # Initialize an empty list to store Container objects

    @classmethod
    def load_containers(cls, containers_file_path: str = None, multi_container_file_path: str = None, magic_container_file_path: str = None, multi_magic_container_file_path: str = None) -> 'ContainerManager':
        """Load containers from different files (regular, multi-container, magic)."""
        instance = cls()

        # Load regular containers from CSV
        if containers_file_path:
            with open(containers_file_path, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header
                instance.containers = [
                    Container(name, int(empty), int(capacity))
                    for name, empty, capacity in reader
                ]

        # Load multi-containers where one container holds others
        if multi_container_file_path:
            with open(multi_container_file_path, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    mother_container = Container(row[0], 0, 0)  # First entry is the parent container
                    for child_name in row[1:]:
                        child_container = instance.get_container_by_name(child_name)
                        if child_container:
                            mother_container.add_item(child_container)
                    instance.containers.append(mother_container)

        # Load magic containers
        if magic_container_file_path:
            with open(magic_container_file_path, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    magic_container_name, container_name = row
                    normal_container = instance.get_container_by_name(container_name)
                    if normal_container:
                        magic_container = MagicContainer.convert_container_to_magic(normal_container, magic_container_name)
                        instance.containers.append(magic_container)

        # Load multi-magic containers
        if multi_magic_container_file_path:
            with open(multi_magic_container_file_path, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    magic_container_name, container_name = row
                    normal_container = instance.get_container_by_name(container_name)
                    if normal_container:
                        magic_container = MagicContainer.convert_container_to_magic(normal_container, magic_container_name)
                        instance.containers.append(magic_container)

        return instance

    def print_containers(self):
        """Print all containers."""
        for container in self.containers:
            container.list_items()  # Assuming Container class has a list_items method

    def add_container(self, containers: List[Container]):
        """Add multiple containers to the ContainerManager."""
        self.containers.extend(containers)

    def get_containers(self) -> List[Container]:
        """Return a list of all containers."""
        return self.containers

    def get_container_by_name(self, container_name: str) -> Container:
        """Find and return a container by its name."""
        for container in self.containers:
            if container.name.strip().lower() == container_name.strip().lower():
                return copy.deepcopy(container)  # Return a copy to prevent modification
        return None  # Return None if no match is found

    def get_count(self) -> int:
        """Return the total number of containers."""
        return len(self.containers)

def print_items_and_containers(items: ItemManager, containers: ContainerManager):
    """Print the count of items and containers, and their details."""
    print(f"Initialized {items.get_count() + containers.get_count()} items including {containers.get_count()} containers.\n")
    
    print("Items:")
    items.print_items()

    print("\nContainers:")
    containers.print_containers()

class ContainerSelectScreen(Screen):
    def __init__(self, containers: ContainerManager) -> None:
        super().__init__()
        self.containers: ContainerManager = containers  # Store the container manager
    
    def display_menu(self):
        """Display menu (implementation needed)."""
        return

    def get_choice(self):
        """Get the name of the container from the user."""
        return input("Enter the name of the container: ")

    def handle_choice(self, choice):
        """Handle the user's choice of container."""
        container = self.containers.get_container_by_name(choice)
        if container:
            return container  # Return selected container
        else:
            print(f"\"{choice}\" not found. Try again.")  # Prompt for valid input

class MainMenu(Screen):
    def __init__(self, items: ItemManager = None, container: Container = None) -> None:
        super().__init__()
        self.items: ItemManager = items  # Store the item manager
        self.container: Container = container  # Store the current container

    def display_menu(self):
        """Display the main menu options."""
        print("==================================")
        print("Enter your choice:")
        print("1. Loot item.")
        print("2. List looted items.")
        print("0. Quit.")
        print("==================================")

    def handle_choice(self, choice):
        """Handle the user's choice of action."""
        if choice == "1":
            self.handle_loot_item()  # Loot an item
        elif choice == "2":
            self.list_looted_items()  # List looted items
        elif choice == "0":
            exit()  # Exit the program
        else:
            print("Invalid choice. Try again.")  # Handle invalid choice
    
    def handle_loot_item(self):
        """Loot an item by asking the user for the item name."""
        while True:
            item_name = input("Enter the name of the item: ")
            item = self.items.get_item_by_name(item_name)  # Look for the item

            if item:
                self.container.add_item(item)  # Add the item to the container
                
                break
            else:
                print(f"\"{item_name}\" not found. Try again.")

    def list_looted_items(self):
        """List all the looted items."""
        self.container.list_items()
        
def gameloop():
    items = ItemManager.load_items('items.csv')
    containers = ContainerManager.load_containers('containers.csv', 'multi_containers.csv', 'magic_containers.csv')

    print(f"Initialised {items.get_count()+containers.get_count()} items including {containers.get_count()} containers.\n")
    # print_items_and_containers(items, containers)
    # print("")

    # Game Loop
    container = ContainerSelectScreen(containers).run()
    MainMenu(items, container).run()

if __name__ == "__main__":
    gameloop()
    