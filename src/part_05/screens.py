class Screen:
    def display_menu(self):
        raise NotImplementedError("This method should be overridden by subclasses.")

    def get_choice(self):
        return input("Your choice: ")

    def handle_choice(self, choice):
        raise NotImplementedError("This method should be overridden by subclasses.")

    def run(self):
        while True:
            self.display_menu()
            choice = self.get_choice()
            out = self.handle_choice(choice)
            if(out):
                break
        return out