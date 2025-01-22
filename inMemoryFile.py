class FileSystemError(Exception):
    pass

class Entity:
    def __init__(self, name):
        self.name = name

class File(Entity):
    def __init__(self, name):
        super().__init__(name)
        self.content = ""

class Folder(Entity):
    def __init__(self, name):
        super().__init__(name)
        self.children = {}

class Drive(Folder):
    def __init__(self, name):
        super().__init__(name)

class FileSystem:
    def __init__(self):
        self.drives = {}

    def create(self, path, entity_type, name):
        if entity_type not in ("file", "folder", "drive"):
            raise FileSystemError("Invalid entity type.")

        if entity_type == "drive":
            if name in self.drives:
                raise FileSystemError(f"Drive {name} already exists.")
            self.drives[name] = Drive(name)
        else:
            parent = self._find_entity(path)
            if not isinstance(parent, Folder):
                raise FileSystemError(f"Cannot create {entity_type} under a non-folder entity.")
            if name in parent.children:
                raise FileSystemError(f"{entity_type.capitalize()} {name} already exists in {path}.")

            if entity_type == "file":
                parent.children[name] = File(name)
            elif entity_type == "folder":
                parent.children[name] = Folder(name)

    def delete(self, path):
        parent, name = self._get_parent_and_name(path)
        if name not in parent.children:
            raise FileSystemError(f"Entity {name} does not exist at {path}.")
        del parent.children[name]

    def move(self, source_path, destination_path):
        parent, name = self._get_parent_and_name(source_path)
        if name not in parent.children:
            raise FileSystemError(f"Entity {name} does not exist at {source_path}.")

        entity = parent.children[name]
        del parent.children[name]

        destination = self._find_entity(destination_path)
        if not isinstance(destination, Folder):
            raise FileSystemError(f"Cannot move to non-folder destination {destination_path}.")
        if name in destination.children:
            raise FileSystemError(f"An entity with the name {name} already exists in {destination_path}.")

        destination.children[name] = entity

    def write(self, path, content):
        entity = self._find_entity(path)
        if not isinstance(entity, File):
            raise FileSystemError(f"Cannot write to non-file entity {path}.")
        entity.content = content

    def read(self, path):
        entity = self._find_entity(path)
        if not isinstance(entity, File):
            raise FileSystemError(f"Cannot read from non-file entity {path}.")
        return entity.content

    def _find_entity(self, path):
        parts = path.strip("/").split("/")
        if not parts or parts[0] not in self.drives:
            raise FileSystemError(f"Drive {parts[0]} does not exist.")

        current = self.drives[parts[0]]
        for part in parts[1:]:
            if part not in current.children or not isinstance(current.children[part], Entity):
                raise FileSystemError(f"Path {path} does not exist.")
            current = current.children[part]

        return current

    def _get_parent_and_name(self, path):
        parts = path.strip("/").split("/")
        if len(parts) < 2:
            raise FileSystemError(f"Invalid path {path}.")

        parent = self._find_entity("/" + "/".join(parts[:-1]))
        name = parts[-1]
        return parent, name

# Interactive CLI
def main():
    fs = FileSystem()
    print("Welcome to the In-Memory File System")
    print("Available commands: drive, folder, file, write, move, delete, read, list, exit")

    while True:
        command = input("Enter command (drive, folder, file, write, move, delete, read, list, exit): ").strip().lower()
        if command == "exit":
            print("Exiting the file system. Goodbye!")
            break

        try:
            if command == "drive":
                drive_name = input("Enter drive name: ").strip()
                fs.create("", "drive", drive_name)
                print(f"Drive {drive_name} created successfully.")

            elif command == "folder":
                print("Available drives and folders:")
                for drive in fs.drives:
                    print(f"- /{drive}")

                path = input("Enter the path where you want to create the folder (e.g., /C): ").strip()
                try:
                    entity = fs._find_entity(path)
                    if isinstance(entity, Folder) or isinstance(entity, Drive):
                        print(f"Available items in {path}:")
                        for item in entity.children.values():
                            if isinstance(item, Folder):
                                print(f"[Folder] {item.name}")
                            elif isinstance(item, File):
                                print(f"[File] {item.name}")
                except FileSystemError:
                    print(f"Path {path} not found.")

                folder_name = input("Enter folder name: ").strip()
                fs.create(path, "folder", folder_name)
                print(f"Folder {folder_name} created at {path}.")

            elif command == "file":
                print("Available drives and folders:")
                for drive in fs.drives:
                    print(f"- /{drive}")

                path = input("Enter the path where you want to create the file (e.g., /C): ").strip()
                try:
                    entity = fs._find_entity(path)
                    if isinstance(entity, Folder) or isinstance(entity, Drive):
                        print(f"Available items in {path}:")
                        for item in entity.children.values():
                            if isinstance(item, Folder):
                                print(f"[Folder] {item.name}")
                            elif isinstance(item, File):
                                print(f"[File] {item.name}")
                except FileSystemError:
                    print(f"Path {path} not found.")

                file_name = input("Enter file name: ").strip()
                fs.create(path, "file", file_name)
                print(f"File {file_name} created at {path}.")

            elif command == "write":
                file_path = input("Enter the file path (e.g., /C/Documents/notes.txt): ").strip()
                content = input("Enter the content to write: ").strip()
                fs.write(file_path, content)
                print(f"Content written to {file_path}.")

            elif command == "read":
                file_path = input("Enter the file path (e.g., /C/Documents/notes.txt): ").strip()
                content = fs.read(file_path)
                print(f"Content of {file_path}: {content}")

            elif command == "move":
                source_path = input("Enter the source path (e.g., /C/Documents/file.txt): ").strip()
                destination_path = input("Enter the destination path (e.g., /C/OtherFolder): ").strip()
                fs.move(source_path, destination_path)
                print(f"Moved {source_path} to {destination_path}.")

            elif command == "delete":
                path = input("Enter the path to delete (e.g., /C/Documents): ").strip()
                fs.delete(path)
                print(f"Deleted {path}.")

            elif command == "list":
                path = input("Enter the path to list items (e.g., /C): ").strip()
                try:
                    entity = fs._find_entity(path)
                    if isinstance(entity, Folder) or isinstance(entity, Drive):
                        print(f"Items in {path}:")
                        for item in entity.children.values():
                            if isinstance(item, Folder):
                                print(f"[Folder] {item.name}")
                            elif isinstance(item, File):
                                print(f"[File] {item.name}")
                except FileSystemError:
                    print(f"Path {path} not found.")

            else:
                print("Invalid command. Please try again.")

        except FileSystemError as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
