import csv
import copy
from typing import List

# Screen Class is an abstraction for a menu-based user interface.
# It contains methods to display a menu, get user input, handle the input, and control the program's flow.
class Screen:
    # Displays the menu. This method should be overridden in subclasses to provide specific menu options.
    def display_menu(self):
        pass  # To be overridden by subclasses

    # Gets the user's choice as input. This method can be used as-is or overridden for custom input methods.
    def get_choice(self):
        return input()

    # Handles the user's choice. This method should be overridden in subclasses to define actions based on the user's selection.
    def handle_choice(self, choice):
        pass  # To be overridden by subclasses

    # The main loop that displays the menu, gets the user's input, and processes it.
    # The loop continues until a valid choice leads to an exit condition, defined by the handle_choice method returning a truthy value.
    def run(self):
        while True:
            # Display the menu to the user
            self.display_menu()
            
            # Get the user's choice
            choice = self.get_choice()
            
            # Handle the user's choice
            out = self.handle_choice(choice)
            
            # If a condition to break the loop is met (i.e., out is truthy), exit the loop
            if(out):
                break
        
        # Return the result of the final handled choice
        return out


# Class to represent an item with a name and weight.
class Item:
    def __init__(self, name: str, weight: int):
        # Initialize the item's name and weight.
        self.name = name
        self.weight = weight

    # String representation of the item, including its name and current weight.
    def __str__(self) -> str:
        return f"{self.name} (weight: {self.get_current_weight()})"
    
    # Returns the current weight of the item.
    def get_current_weight(self):
        return self.weight
    
    # Alias method to get the item's weight so containers can also call this later on and return the child item weights
    def get_item_weight(self):
        return self.weight

# Class to manage a collection of Item objects.
class ItemManager:
    def __init__(self):
        # Initialize an empty list to store items.
        self.items: List[Item] = []

    # Class method to load items from a CSV file.
    @classmethod
    def load_items(cls, file_path: str) -> 'ItemManager':
        # Create a new instance of ItemManager.
        instance = cls()
        # Open the file for reading.
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the first row (header).
            # Iterate through the rows in the CSV and create Item objects.
            for row in reader:
                name, weight = row
                # Append each item to the items list in the instance.
                instance.items.append(Item(name, int(weight)))
        # Return the populated instance.
        return instance
    
    # Add a list of items to the existing item collection.
    def add_items(self, items: List[Item]):
        self.items.extend(items)  # Add items to the items list.
        
    # Print all items in the collection to the console.
    def print_items(self):
        for item in self.items:
            print(item)
    
    # Return the list of items in the collection.
    def get_items(self) -> List[Item]:
        return self.items
    
    # Find an item by name in the collection (case-insensitive).
    def get_item_by_name(self, item_to_find) -> List[Item]:
        for item in self.items:
            # Compare the item's name with the provided name (case-insensitive).
            if item.name.strip().lower() == item_to_find.strip().lower():
                return item
        return None  # Return None if the item is not found.
    
    # Return the total number of items in the collection.
    def get_count(self) -> int:
        return len(self.items)

# Class to represent a container in the game
class Container(Item):
    def __init__(self, name: str, weight: int, weight_capacity: int):
        # Initialize the container's name, weight, and weight capacity.
        super().__init__(name, weight)
        self.weight_capacity = weight_capacity  # Maximum weight the container can hold.
        self.items: List[Item] = []  # List to store items within the container.
        self.is_multi_container = False  # Flag to indicate if the container can hold other containers.

    # String representation of the container
    def __str__(self) -> str:
        capacity_display = f"{self.get_current_capacity()}/{self.weight_capacity}"
        if self.is_multi_container: # did this under the assumption that later on we'd have to make containers and multi containers interchangeable
            capacity_display = "0/0"  # Indicate that multi-containers do not display capacity. 
        return (f"{self.name} (total weight: {self.get_current_weight()}, "
                f"empty weight: {self.weight}, capacity: {capacity_display})")

    # Class method to load container from a file
    @classmethod
    def load_items(cls, file_path: str = None, items: List[Item] = None) -> 'Container':
        instance = cls("", 0, 0)  # Create an empty container instance.
        if file_path:  # Load items from a file if a path is provided.
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip the first row (header).
                for name, weight in reader:
                    instance.add_item(Item(name, int(weight)))  # Add each item to the container.
        if items:  # Load items from the provided list.
            for item in items:
                instance.add_item(item)
        return instance  # Return the populated container instance.

    # Method to add an item to the container.
    def add_item(self, item: Item, parent_container_name=None, start_load=False):

        # FOR LOADING MULTI CONTAINERS
        if (isinstance(item, Container) and start_load):  # Check if item is a container and start loading.
            self.items.append(item)  # Add the container to this container.
            self.is_multi_container = True  # Mark this container as capable of holding multiple containers.
            self.weight += item.get_current_weight()  # Update the weight of this container.
            self.weight_capacity += item.weight_capacity  # Update the weight capacity.
        else:
        # NORMAL ADDING LOGIC
            # Check if the item can be added to any existing containers.
            for container in self.items:
                if isinstance(container, Container):  # Check if it's a container.
                    if (item.get_current_weight() + container.get_current_capacity() <=
                        container.weight_capacity - container.get_child_container_capacity() or isinstance(item, Container)):
                        container.add_item(item, self.name)  # Add the item to the sub-container.
                        return True  # Successfully added the item.
            # Check if the item can be added directly to this container.
            if item.get_current_weight() + self.get_current_capacity() <= self.weight_capacity - self.get_child_container_capacity():
                self.items.append(item)  # Add the item to this container.
                # Print success message with parent container name if provided.
                if parent_container_name:
                    print(f"Success! Item \"{item.name}\" stored in container \"{parent_container_name}\".")
                else:
                    print(f"Success! Item \"{item.name}\" stored in container \"{self.name}\".")
            else:
                # Print failure message if the item cannot be stored.
                print(f"Failure! Item \"{item.name}\" NOT stored in container \"{self.name}\".")
                return False  # Return false if the item couldn't be added.
        return True  # Return true if the item was added successfully.

    # Method to add multiple items to the container.
    def add_items(self, items: List[Item]):
        for item in items:
            self.add_item(item)  # Add each item individually.

    # Calculate the total weight capacity of all child containers.
    def get_child_container_capacity(self):
        return sum(item.weight_capacity for item in self.items if isinstance(item, Container))

    # Calculate the current total weight of the container, including its items.
    def get_current_weight(self):
        return self.weight + sum(item.get_item_weight() for item in self.items)

    # Calculate the total weight of items that are not containers.
    def get_item_weight(self):
        return sum(item.get_current_weight() for item in self.items if not isinstance(item, Container))

    # Calculate the current total weight of items that are not containers.
    def get_current_capacity(self):
        return sum(item.get_current_weight() for item in self.items if not isinstance(item, Container))

    # List all items in the container, including items in nested containers.
    def list_items(self, depth=1):
        print(self)  # Print the container itself.
        for item in self.items:
            indent = "   " * depth  # Create indentation for nested items.
            if isinstance(item, Container):  # If the item is a container, list its items recursively.
                print(indent, end="")
                item.list_items(depth + 1)
            else:
                # Print the item name and weight.
                print(f"{indent}{item.name} (weight: {item.weight})")

    # Find and return an item by its name, or None if not found.
    def get_item_by_name(self, name: str) -> Item:
        return next((item for item in self.items if item.name == name), None)

    # Return the list of items in the container.
    def get_items(self) -> List[Item]:
        return self.items

    # Return the count of items in the container.
    def get_count(self) -> int:
        return len(self.items)

# Class representing a special type of container with additional properties or behaviors.
class MagicContainer(Container):
    def __init__(self, name: str, weight: int, weight_capacity: int):
        # Initialize the magic container with name, weight, and weight capacity.
        super().__init__(name, weight, weight_capacity)

    # Override the add_item method to include any special behavior for magic containers.
    def add_item(self, item: Item, parent_container_name=None, start_load=False):
        if (isinstance(item, Container) and start_load):  # Check if the item is a container and if loading starts.
            self.items.append(item)  # Add the magic container.
            self.is_multi_container = True  # Indicate that this is a multi-container.
            self.weight_capacity += item.weight_capacity  # Update the weight capacity.
        else:
            # Check if the item can be added to any existing containers.
            for container in self.items:
                if isinstance(container, Container):  # Check if it's a container.
                    if (container.get_current_capacity() + item.get_current_weight() <=
                        container.weight_capacity - container.get_child_container_capacity() or isinstance(item, Container)):
                        container.add_item(item, self.name)  # Add the item to the sub-container.
                        return True  # Successfully added the item.

            # Check if the item can be added directly to this magic container.
            if self.get_current_capacity() + item.get_current_weight() <= self.weight_capacity - self.get_child_container_capacity():
                self.items.append(item)  # Add the item to the magic container.
                # Print success message with parent container name if provided.
                if parent_container_name:
                    print(f"Success! Item \"{item.name}\" stored in container \"{parent_container_name}\".")
                else:
                    print(f"Success! Item \"{item.name}\" stored in container \"{self.name}\".")
            else:
                # Print failure message if the item cannot be stored.
                print(f"Failure! Item \"{item.name}\" NOT stored in container \"{self.name}\".")
                return False  # Return false if the item couldn't be added.
        return True  # Return true if the item was added successfully.

    # Class method to convert a regular container to a magic container.
    @classmethod
    def convert_container_to_magic(cls, container: Container, magic_name):
        instance = cls(magic_name, container.weight, container.weight_capacity)  # Create a new magic container instance.
        instance.is_multi_container = container.is_multi_container  # Copy the multi-container flag.
        instance.items = container.items  # Copy the items from the original container.
        return instance  # Return the new magic container instance.

    # Override the get_current_capacity method for specific behavior if needed.
    def get_current_capacity(self):
        return sum(item.get_current_weight() for item in self.items if not isinstance(item, Container))

    # Override the get_current_weight method for specific behavior if needed.
    def get_current_weight(self):
        return self.weight

    # Override the get_item_weight method for specific behavior if needed.
    def get_item_weight(self):
        return sum(item.get_current_weight() for item in self.items if not isinstance(item, Container))

    # String representation of the magic container, similar to the base Container class.
    def __str__(self) -> str:
        capacity_display = f"{self.get_current_capacity()}/{self.weight_capacity}"
        if self.is_multi_container:
            capacity_display = "0/0"  # Indicate that multi-containers do not display capacity.
        return (f"{self.name} (total weight: {self.get_current_weight()}, "
                f"empty weight: {self.weight}, capacity: {capacity_display})")
    
class ContainerManager:
    def __init__(self):
        # Initialize an empty list to hold containers
        self.containers: List[Container] = []

    @classmethod
    def load_containers(cls, containers_file_path: str = None, 
                        multi_container_file_path: str = None, 
                        magic_container_file_path: str = None, 
                        multi_magic_container_file_path: str = None) -> 'ContainerManager':
        # Create an instance of ContainerManager
        instance = cls()

        # Load regular containers if the file path is provided
        if containers_file_path:
            with open(containers_file_path, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                # Create Container instances for each entry in the file
                instance.containers = [
                    Container(name, int(empty), int(capacity))
                    for name, empty, capacity in reader
                ]

        # Load multi containers if the file path is provided
        if multi_container_file_path:
            with open(multi_container_file_path, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                # Create a mother container and add child containers from the file
                for row in reader:
                    mother_container = Container(row[0], 0, 0)  # First entry is the mother container name
                    for child_name in row[1:]:
                        # Get the child container by name
                        child_container = instance.get_container_by_name(child_name)
                        if child_container:
                            # Add child container to the mother container
                            mother_container.add_item(child_container, start_load=True)
                    # Append the mother container to the list of containers
                    instance.containers.append(mother_container)

        # Load magic containers if the file path is provided
        if magic_container_file_path:
            with open(magic_container_file_path, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                # Create magic containers from normal containers
                for row in reader:
                    magic_container_name, container_name = row
                    normal_container = instance.get_container_by_name(container_name)
                    if normal_container:
                        # Convert normal container to a magic container
                        magic_container = MagicContainer.convert_container_to_magic(normal_container, magic_container_name)
                        instance.containers.append(magic_container)

        # Load multi-magic containers if the file path is provided
        if multi_magic_container_file_path:
            with open(multi_magic_container_file_path, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                # Create magic containers from normal containers
                for row in reader:
                    magic_container_name, container_name = row
                    normal_container = instance.get_container_by_name(container_name)
                    if normal_container:
                        # Convert normal container to a magic container
                        magic_container = MagicContainer.convert_container_to_magic(normal_container, magic_container_name)
                        instance.containers.append(magic_container)

        return instance  # Return the populated ContainerManager instance

    def print_containers(self):
        # Print details of all containers
        for container in self.containers:
            container.list_items()  # Assuming `Container` class has a method to list items

    def add_container(self, containers: List[Container]):
        # Add a list of containers to the manager
        self.containers.extend(containers)

    def get_containers(self) -> List[Container]:
        # Return the list of all containers
        return self.containers

    def get_container_by_name(self, container_name: str) -> Container:
        # Find and return a container by its name (case-insensitive)
        for container in self.containers:
            if container.name.strip().lower() == container_name.strip().lower():
                return copy.deepcopy(container)  # Return a deep copy of the container
        return None  # Return None if not found

    def get_count(self) -> int:
        # Return the total count of containers
        return len(self.containers)

class ContainerSelectScreen(Screen):
    def __init__(self, containers:ContainerManager) -> None:
        super().__init__()  # Initialize the parent Screen class
        self.containers: ContainerManager = containers  # Store the ContainerManager instance
    
    def display_menu(self):
        # Placeholder for displaying the menu; implementation can be added later
        return

    def get_choice(self):
        # Prompt user to enter the name of the container
        return input("Enter the name of the container: ")

    def handle_choice(self, choice):
        # Handle the user's choice of container
        container = self.containers.get_container_by_name(choice)
        if container:
            return container  # Return the found container
        else:
            print(f"\"{choice}\" not found. Try again.")  # Inform the user if the container is not found

class MainMenu(Screen):
    def __init__(self, items: ItemManager = None, containers: ContainerManager = None, container: Container = None) -> None:
        super().__init__()  # Initialize the parent Screen class
        self.items: ItemManager = items  # Store the ItemManager instance
        self.containers: ContainerManager = containers  # Store the ContainerManager instance
        self.container: Container = container  # Store the current Container instance

    def display_menu(self):
        """Display the main menu options to the user."""
        print("==================================")
        print("Enter your choice:")
        print("1. Loot item.")
        print("2. List looted items.")
        print("0. Quit.")
        print("==================================")

    def handle_choice(self, choice):
        """Handle the choice made by the user."""
        if choice == "1":
            self.handle_loot_item()  # Call method to loot an item
        elif choice == "2":
            self.list_looted_items()  # Call method to list looted items
        elif choice == "0":
            exit()  # Exit the program
        else:
            print("Invalid choice. Try again.")  # Inform user of invalid choice
    
    def handle_loot_item(self):
        """Loot an item by asking the user for the item name."""
        while True:
            item_name = input("Enter the name of the item: ")  # Prompt user for item name
            item = self.items.get_item_by_name(item_name)  # Attempt to find the item in ItemManager
            if not item:
                item = self.containers.get_container_by_name(item_name)  # If not found, check in ContainerManager

            if item:  # If the item was found
                self.container.add_item(item)  # Add the item to the current container
                break  # Exit the loop after successful addition
            else:
                print(f"\"{item_name}\" not found. Try again.")  # Prompt to try again if item is not found

    def list_looted_items(self):
        """List all the looted items."""
        self.container.list_items()  # Call the list_items method of the current container


def gameloop():
    """Main game loop to initialize managers and start the game."""
    # Load items from the specified CSV file into ItemManager
    items = ItemManager.load_items('items.csv')
    # Load containers from the specified CSV files into ContainerManager
    containers = ContainerManager.load_containers('containers.csv', 
                                                  'multi_containers.csv', 
                                                  'magic_containers.csv', 
                                                  'magic_multi_containers.csv')

    # Print the count of initialized items and containers
    print(f"Initialised {items.get_count()+containers.get_count()} items including {containers.get_count()} containers.\n")

    # Start the game loop by selecting a container and running the main menu
    container = ContainerSelectScreen(containers).run()  # Get selected container from the user
    MainMenu(items, containers, container).run()  # Run the main menu with the loaded items and containers


if __name__ == "__main__":
    gameloop()  # Start the game loop when the script is executed
