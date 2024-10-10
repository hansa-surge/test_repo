from screens import Screen
from containers import Container, ContainerManager
from items import ItemManager

def print_items_and_containers(items:ItemManager , containers:ContainerManager):
    print(f"Initialised {items.get_count()+containers.get_count()} items including {containers.get_count()} containers.\n")
    
    print("Items:")
    items.print_items()

    print("\nContainers:")
    containers.print_containers()

class ContainerSelectScreen(Screen):
    def __init__(self, containers:ContainerManager) -> None:
        super().__init__()
        self.containers: ContainerManager = containers
    
    def display_menu(self):
        print("")

    def get_choice(self):
        return input("Enter the name of the container: ")

    def handle_choice(self, choice):
        container = self.containers.get_container_by_name(choice)
        if(container):
            return container
        else:
            print(f"\"{choice}\" not found. Try again.")

class MainMenu(Screen):
    def __init__(self, items:ItemManager = None, container:Container = None) -> None:
        super().__init__()
        self.items: ItemManager = items
        self.container: Container = container

    def display_menu(self):
        print("==================================")
        print("Enter your choice:")
        print("1. Loot item.")
        print("2. List looted items.")
        print("0. Quit.")
        print("==================================")

    def handle_choice(self, choice):
        """Handle the choice made by the user."""
        if choice == "1":
            self.handle_loot_item()
        elif choice == "2":
            self.list_looted_items()
        elif choice == "0":
            print("Exiting the program.")
            exit()
        else:
            print("Invalid choice. Try again.")
    
    def handle_loot_item(self):
        """Loot an item by asking the user for the item name."""
        while True:
            item_name = input("Enter the name of the item: ")
            item = self.items.get_item_by_name(item_name)

            if item:
                self.container.add_item(item)
                print(f"Looted \"{item.name}\".")
                break
            else:
                print(f"\"{item_name}\" not found. Try again.")

    def list_looted_items(self):
        """List all the looted items."""
        self.container.list_items()

def gameloop():
    items = ItemManager.load_items('items.csv')
    containers = ContainerManager.load_multi_magic_containers('containers.csv', 'multi_containers.csv', 'magic_multi_containers.csv')

    print_items_and_containers(items, containers)
    print("")

    # Game Loop
    container = ContainerSelectScreen(containers).run()
    MainMenu(items, container).run()