import os

class File:
    def __init__(self, name, content=""):
        self.name = name
        self.content = content

    def get_size(self):
        return len(self.content)

class Folder:
    def __init__(self, name):
        self.name = name
        self.contents = []

    def get_size(self):
        total_size = 0
        for item in self.contents:
            if isinstance(item, File):
                total_size += item.get_size()
            elif isinstance(item, Folder):
                total_size += item.get_size()
        return total_size

class FileSystem:
    def __init__(self):
        self.root = Folder("root")
        self.current_folder = self.root

    def run(self):
        while True:
            command = input("> ")
            parts = command.split(" ")
            if parts[0] == "ls":
                self.ls()
            elif parts[0] == "pwd":
                self.pwd()
            elif parts[0] == "cd":
                if len(parts) > 1:
                    self.cd(parts[1])
                else:
                    print("Missing folder name.")
            elif parts[0] == "cat":
                if len(parts) > 1:
                    self.cat(parts[1])
                else:
                    print("Missing file name.")
            elif parts[0] == "mkdir":
                if len(parts) > 1:
                    self.mkdir(parts[1])
                else:
                    print("Missing folder name.")
            elif parts[0] == "touch":
                if len(parts) > 1:
                    self.touch(parts[1])
                else:
                    print("Missing file name.")
            elif parts[0] == "rm":
                if len(parts) > 1:
                    self.rm(parts[1])
                else:
                    print("Missing file name.")
            elif parts[0] == "rmdir":
                if len(parts) > 1:
                    self.rmdir(parts[1])
                else:
                    print("Missing folder name.")
            elif parts[0] == "write":
                if len(parts) > 2:
                    self.write(parts[1], " ".join(parts[2:]))
                else:
                    print("Invalid command syntax. Usage: write <file> <content>")
            elif parts[0] == "cp":
                if len(parts) > 2:
                    self.cp(parts[1], parts[2])
                else:
                    print("Invalid command syntax. Usage: cp <source_file> <destination_file>")
            elif parts[0] == "mv":
                if len(parts) > 2:
                    self.mv(parts[1], parts[2])
                else:
                    print("Invalid command syntax. Usage: mv <source_file> <destination_file>")
            elif parts[0] == "size":
                if len(parts) > 1:
                    self.size(parts[1])
                else:
                    print("Missing file or folder name.")
            elif parts[0] == "exit":
                break
            else:
                print("Unknown command. Type 'help' for a list of available commands.")

    def ls(self):
        for item in self.current_folder.contents:
            if isinstance(item, File):
                print(item.name)
        for item in self.current_folder.contents:
            if isinstance(item, Folder):
                print(item.name + "/")

    def pwd(self):
        print(os.path.abspath(self.current_folder.name))

    def cd(self, folder_name):
        if folder_name == "..":
            if self.current_folder != self.root:
                self.current_folder = self.root
        else:
            for item in self.current_folder.contents:
                if isinstance(item, Folder) and item.name == folder_name:
                    self.current_folder = item
                    break
        self.pwd()

    def cat(self, file_name):
        for item in self.current_folder.contents:
            if isinstance(item, File) and item.name == file_name:
                print(item.content)
                return
        print(f"File '{file_name}' not found.")

    def mkdir(self, folder_name):
        for item in self.current_folder.contents:
            if isinstance(item, Folder) and item.name == folder_name:
                print(f"Folder '{folder_name}' already exists.")
                return
        new_folder = Folder(folder_name)
        self.current_folder.contents.append(new_folder)

    def touch(self, file_name):
        for item in self.current_folder.contents:
            if isinstance(item, File) and item.name == file_name:
                print(f"File '{file_name}' already exists.")
                return
        new_file = File(file_name)
        self.current_folder.contents.append(new_file)

    def rm(self, file_name):
        for item in self.current_folder.contents:
            if isinstance(item, File) and item.name == file_name:
                self.current_folder.contents.remove(item)
                return
        print(f"File '{file_name}' not found.")

    def rmdir(self, folder_name):
        for item in self.current_folder.contents:
            if isinstance(item, Folder) and item.name == folder_name:
                self.current_folder.contents.remove(item)
                return
        print(f"Folder '{folder_name}' not found.")

    def write(self, file_name, content):
        for item in self.current_folder.contents:
            if isinstance(item, File) and item.name == file_name:
                item.content = content
                return

        new_file = File(file_name, content)
        self.current_folder.contents.append(new_file)

    def read(self, file_name):
        for item in self.current_folder.contents:
            if isinstance(item, File) and item.name == file_name:
                print(self.current_folder[file_name])

    def cp(self, source_file, destination_file):
        source = None
        for item in self.current_folder.contents:
            if isinstance(item, File) and item.name == source_file:
                source = item
                break
        if not source:
            print(f"Source file '{source_file}' not found.")
            return
        for item in self.current_folder.contents:
            if isinstance(item, File) and item.name == destination_file:
                print(f"Destination file '{destination_file}' already exists.")
                return
        destination = File(destination_file, source.content)
        self.current_folder.contents.append(destination)

    def mv(self, source_file, destination_file):
        source = None
        for item in self.current_folder.contents:
            if isinstance(item, File) and item.name == source_file:
                source = item
                break
        if not source:
            print(f"Source file '{source_file}' not found.")
            return
        for item in self.current_folder.contents:
            if isinstance(item, File) and item.name == destination_file:
                print(f"Destination file '{destination_file}' already exists.")
                return
        source.name = destination_file

    def size(self, name):
        for item in self.current_folder.contents:
            if item.name == name:
                if isinstance(item, File):
                    print(f"Size of '{name}': {item.get_size()} bytes")
                elif isinstance(item, Folder):
                    print(f"Size of '{name}': {item.get_size()} bytes")
                return
        print(f"File or folder '{name}' not found.")

fs = FileSystem()
fs.run()
