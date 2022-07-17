from cryptography.fernet import Fernet


class PasswordManager:

    def __init__(self):
        self.key = None
        self.password_file = None
        self.password_dict = {}

    def create_key(self, path):
        self.key = Fernet.generate_key()
        with open(path, 'wb') as f:
            f.write(self.key)

    def load_key(self, path):
        if path.endswith('.key'):
            with open(path, 'rb') as f:
                self.key = f.read()
        print("ERROR: Invalid Key File")

    def create_password_file(self, path, initial_values=None):
        self.password_file = path

        if initial_values is not None:
            for key, value in initial_values.items():
                self.add_password(key, value)

    def load_password_file(self, path):
        self.password_file = path
        with open(path, 'r') as f:
            for line in f:
                website, encrypted = line.split(":")
                self.password_dict[website] = Fernet(self.key).decrypt(encrypted.encode()).decode()

    def add_password(self, website, password):
        self.password_dict[website] = password
        if self.password_file is not None:
            with open(self.password_file, 'a+') as f:
                encrypted_password = Fernet(self.key).encrypt(password.encode())
                f.write(website + ":" + encrypted_password.decode() + "\n")

    def get_password(self, website):
        return self.password_dict[website]

    def remove_password(self, website):
        with open(self.password_file, 'r') as f:
            lines = f.readlines()
        with open(self.password_file, 'w') as f:
            for line in lines:
                test = line.find(website)
                if test != 0:
                    f.write(line)


def main():
    password = {
        "email": "test@test.com",
        "facebook": "test",
        "youtube": "test",
    }
    pm = PasswordManager()

    print(
        """
    What do you want to do ?
    
    (1). Create a new Key
    (2). Load an existing key
    (3). Create new password file
    (4). Load existing password file
    (5). Add a new password
    (6). Get a password
    (7). Delete a password
    (q). Quit
    
    """)

    done = False
    while not done:
        choice = input("Enter your choice: ")
        if choice == "1":
            path = input("Enter your path: ")
            pm.create_key(path)
        elif choice == "2":
            path = input("Enter your path: ")
            try:
                pm.load_key(path)
            except FileNotFoundError:
                print("ERROR: File not Found!")
        elif choice == "3":
            path = input("Enter your path: ")
            pm.create_password_file(path, password)
        elif choice == "4":
            path = input("Enter your path: ")
            try:
                pm.load_password_file(path)
            except FileNotFoundError:
                print("ERROR: File not Found!")
        elif choice == "5":
            website = input("Enter the website : ")
            password = input("Enter the password : ")
            pm.add_password(website, password)
        elif choice == "6":
            website = input("Which site? : ")
            password = pm.get_password(website)
            print(f"Password for  {website} is {password}")
        elif choice == "7":
            website = input("Which site? : ")
            try:
                pm.remove_password(website)
                print(f"Password for {website} removed successfully")
            except KeyError:
                print("ERROR: Website not found!")
        elif choice == "q":
            done = True
            print("Thank you for using me, See you again!")
        else:
            print("Invalid Choice, Please try again! ")


if __name__ == "__main__":
    main()
