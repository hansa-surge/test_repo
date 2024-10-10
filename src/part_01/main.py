from containers import ContainerManager
from items import ItemManager

def print_items_and_containers(items:ItemManager , containers:ContainerManager):
    print(f"Initialised {items.get_count()+containers.get_count()} items including {containers.get_count()} containers.\n")
    
    print("Items:")
    items.print_items()

    print("\nContainers:")
    containers.print_containers()

if __name__ == "__main__":
    items = ItemManager.load_items('items.csv')
    containers = ContainerManager.load_containers('containers.csv')

    print_items_and_containers(items, containers)
    print("")


