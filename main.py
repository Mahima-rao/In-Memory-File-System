# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# import time
# from typing import Union, Dict

# class FileSystemError(Exception):
#     pass

# class Entity:
#     def __init__(self, name):
#         self.name = name

# class File(Entity):
#     def __init__(self, name):
#         super().__init__(name)
#         self.content = ""
#         self.size = 0
#         self.created_at = time.time()
#         self.updated_at = time.time()
    
#     def write(self, content):
#         self.content = content
#         self.size = len(content)
#         self.updated_at = time.time()
    
#     def read(self):
#         return self.content

# class Folder(Entity):
#     def __init__(self, name):
#         super().__init__(name)
#         self.children: Dict[str, Union[Folder, File]] = {}
#         self.created_at = time.time()
#         self.updated_at = time.time()

# class Drive(Folder):
#     def __init__(self, name):
#         super().__init__(name)
#         self.total_size = 1000  # For simplicity, assume 1000 units of space
#         self.used_size = 0
#         self.available_size = self.total_size

# class FileSystem:
#     def __init__(self):
#         self.drives: Dict[str, Drive] = {}

#     def create(self, path: str, entity_type: str, name: str):
#         if entity_type not in ("file", "folder", "drive"):
#             raise FileSystemError("Invalid entity type.")

#         if entity_type == "drive":
#             if name in self.drives:
#                 raise FileSystemError(f"Drive {name} already exists.")
#             self.drives[name] = Drive(name)
#         else:
#             parent = self._find_entity(path)
#             if not isinstance(parent, Folder):
#                 raise FileSystemError(f"Cannot create {entity_type} under a non-folder entity.")
#             if name in parent.children:
#                 raise FileSystemError(f"{entity_type.capitalize()} {name} already exists in {path}.")

#             if entity_type == "file":
#                 parent.children[name] = File(name)
#             elif entity_type == "folder":
#                 parent.children[name] = Folder(name)

#     def delete(self, path: str):
#         parent, name = self._get_parent_and_name(path)
#         if name not in parent.children:
#             raise FileSystemError(f"Entity {name} does not exist at {path}.")
#         del parent.children[name]

#     def move(self, source_path: str, destination_path: str):
#         parent, name = self._get_parent_and_name(source_path)
#         if name not in parent.children:
#             raise FileSystemError(f"Entity {name} does not exist at {source_path}.")
        
#         entity = parent.children[name]
#         del parent.children[name]

#         destination = self._find_entity(destination_path)
#         if not isinstance(destination, Folder):
#             raise FileSystemError(f"Cannot move to non-folder destination {destination_path}.")
#         if name in destination.children:
#             raise FileSystemError(f"An entity with the name {name} already exists in {destination_path}.")

#         destination.children[name] = entity

#     def write(self, path: str, content: str):
#         entity = self._find_entity(path)
#         if not isinstance(entity, File):
#             raise FileSystemError(f"Cannot write to non-file entity {path}.")
#         entity.write(content)

#     def read(self, path: str):
#         entity = self._find_entity(path)
#         if not isinstance(entity, File):
#             raise FileSystemError(f"Cannot read from non-file entity {path}.")
#         return entity.read()

#     def _find_entity(self, path: str):
#         parts = path.strip("/").split("/")
#         if not parts or parts[0] not in self.drives:
#             raise FileSystemError(f"Drive {parts[0]} does not exist.")

#         current = self.drives[parts[0]]
#         for part in parts[1:]:
#             if part not in current.children or not isinstance(current.children[part], Entity):
#                 raise FileSystemError(f"Path {path} does not exist.")
#             current = current.children[part]

#         return current

#     def _get_parent_and_name(self, path: str):
#         parts = path.strip("/").split("/")
#         if len(parts) < 2:
#             raise FileSystemError(f"Invalid path {path}.")

#         parent = self._find_entity("/" + "/".join(parts[:-1]))
#         name = parts[-1]
#         return parent, name

# app = FastAPI()
# fs = FileSystem()

# class EntityCreateRequest(BaseModel):
#     path: str
#     entity_type: str
#     name: str

# class WriteRequest(BaseModel):
#     path: str
#     content: str

# @app.post("/create")
# def create_entity(request: EntityCreateRequest):
#     try:
#         fs.create(request.path, request.entity_type, request.name)
#         return {"message": f"{request.entity_type.capitalize()} {request.name} created successfully at {request.path}."}
#     except FileSystemError as e:
#         raise HTTPException(status_code=400, detail=str(e))

# @app.post("/write")
# def write_file(request: WriteRequest):
#     try:
#         fs.write(request.path, request.content)
#         return {"message": f"Content written to {request.path}."}
#     except FileSystemError as e:
#         raise HTTPException(status_code=400, detail=str(e))

# @app.get("/read")
# def read_file(path: str):
#     try:
#         content = fs.read(path)
#         return {"content": content}
#     except FileSystemError as e:
#         raise HTTPException(status_code=400, detail=str(e))

# @app.post("/move")
# def move_entity(source_path: str, destination_path: str):
#     try:
#         fs.move(source_path, destination_path)
#         return {"message": f"Moved {source_path} to {destination_path}."}
#     except FileSystemError as e:
#         raise HTTPException(status_code=400, detail=str(e))

# @app.delete("/delete")
# def delete_entity(path: str):
#     try:
#         fs.delete(path)
#         return {"message": f"Deleted {path}."}
#     except FileSystemError as e:
#         raise HTTPException(status_code=400, detail=str(e))


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

# Custom exception for the file system
class FileSystemError(Exception):
    pass

# Entity classes
class Entity:
    def __init__(self, name: str):
        self.name = name

class File(Entity):
    def __init__(self, name: str):
        super().__init__(name)
        self.content = ""

class Folder(Entity):
    def __init__(self, name: str):
        super().__init__(name)
        self.children: Dict[str, Entity] = {}

class Drive(Folder):
    def __init__(self, name: str):
        super().__init__(name)

# File system implementation
class FileSystem:
    def __init__(self):
        self.drives: Dict[str, Drive] = {}

    def create(self, path: str, entity_type: str, name: str):
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
            parent.children[name] = File(name) if entity_type == "file" else Folder(name)

    def delete(self, path: str):
        parent, name = self._get_parent_and_name(path)
        if name not in parent.children:
            raise FileSystemError(f"Entity {name} does not exist at {path}.")
        del parent.children[name]

    def move(self, source_path: str, destination_path: str):
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

    def write(self, path: str, content: str):
        entity = self._find_entity(path)
        if not isinstance(entity, File):
            raise FileSystemError(f"Cannot write to non-file entity {path}.")
        entity.content = content

    def read(self, path: str) -> str:
        entity = self._find_entity(path)
        if not isinstance(entity, File):
            raise FileSystemError(f"Cannot read from non-file entity {path}.")
        return entity.content

    def _find_entity(self, path: str) -> Entity:
        parts = path.strip("/").split("/")
        if not parts or parts[0] not in self.drives:
            raise FileSystemError(f"Drive {parts[0]} does not exist.")

        current = self.drives[parts[0]]
        for part in parts[1:]:
            if part not in current.children or not isinstance(current.children[part], Entity):
                raise FileSystemError(f"Path {path} does not exist.")
            current = current.children[part]

        return current

    def _get_parent_and_name(self, path: str):
        parts = path.strip("/").split("/")
        if len(parts) < 2:
            raise FileSystemError(f"Invalid path {path}.")
        parent = self._find_entity("/" + "/".join(parts[:-1]))
        name = parts[-1]
        return parent, name


# API Models
class CreateRequest(BaseModel):
    path: str
    entity_type: str
    name: str

class WriteRequest(BaseModel):
    path: str
    content: str

class MoveRequest(BaseModel):
    source_path: str
    destination_path: str


# FastAPI app
app = FastAPI()

fs = FileSystem()

@app.post("/create")
def create_entity(request: CreateRequest):
    try:
        fs.create(request.path, request.entity_type, request.name)
        return {"message": f"{request.entity_type.capitalize()} {request.name} created successfully."}
    except FileSystemError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/delete")
def delete_entity(path: str):
    try:
        fs.delete(path)
        return {"message": f"Entity at {path} deleted successfully."}
    except FileSystemError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/move")
def move_entity(request: MoveRequest):
    try:
        fs.move(request.source_path, request.destination_path)
        return {"message": f"Moved {request.source_path} to {request.destination_path}."}
    except FileSystemError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/write")
def write_to_file(request: WriteRequest):
    try:
        fs.write(request.path, request.content)
        return {"message": f"Content written to {request.path}."}
    except FileSystemError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/read")
def read_from_file(path: str):
    try:
        content = fs.read(path)
        return {"path": path, "content": content}
    except FileSystemError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/list")
def list_entities(path: str):
    try:
        entity = fs._find_entity(path)
        if isinstance(entity, Folder):
            items = [{"name": name, "type": "folder" if isinstance(child, Folder) else "file"} for name, child in entity.children.items()]
            return {"path": path, "items": items}
        else:
            raise FileSystemError(f"Path {path} is not a folder.")
    except FileSystemError as e:
        raise HTTPException(status_code=400, detail=str(e))
