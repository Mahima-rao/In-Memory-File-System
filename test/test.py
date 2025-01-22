import sys
import os
import pytest
from fastapi.testclient import TestClient

# Add the parent directory to the Python module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import app, FileSystem

client = TestClient(app)

@pytest.fixture
def setup_fs():
    """
    Fixture to initialize the virtual file system for testing.
    """
    fs = FileSystem()
    fs.create("", "drive", "C")
    fs.create("/C", "folder", "Documents")
    fs.create("/C/Documents", "file", "file1.txt")
    return fs


def test_create_folder():
    """
    Test creating a folder in the virtual file system.
    """
    client.post("/create", json={"path": "", "entity_type": "drive", "name": "C"})  # Ensure /C exists
    response = client.post("/create", json={"path": "/C", "entity_type": "folder", "name": "NewFolder"})
    print(response.json())  # Debug response
    assert response.status_code == 200
    assert response.json()["message"] == "Folder NewFolder created successfully."


def test_create_file():
    """
    Test creating a file in the virtual file system.
    """
    client.post("/create", json={"path": "", "entity_type": "drive", "name": "C"})  # Ensure /C exists
    client.post("/create", json={"path": "/C", "entity_type": "folder", "name": "Documents"})  # Ensure /C/Documents exists
    response = client.post("/create", json={"path": "/C/Documents", "entity_type": "file", "name": "notes.txt"})
    print(response.json())  # Debug response
    assert response.status_code == 200
    assert response.json()["message"] == "File notes.txt created successfully."


def test_write_and_read_file():
    """
    Test writing content to a file and reading it back.
    """
    client.post("/create", json={"path": "", "entity_type": "drive", "name": "C"})  # Ensure /C exists
    client.post("/create", json={"path": "/C", "entity_type": "folder", "name": "Documents"})  # Ensure /C/Documents exists
    client.post("/create", json={"path": "/C/Documents", "entity_type": "file", "name": "file1.txt"})  # Ensure file exists

    response = client.post("/write", json={"path": "/C/Documents/file1.txt", "content": "Hello, World!"})
    print(response.json())  # Debug response
    assert response.status_code == 200
    assert response.json()["message"] == "Content written to /C/Documents/file1.txt."

    response = client.get("/read?path=/C/Documents/file1.txt")
    print(response.json())  # Debug response
    assert response.status_code == 200
    assert response.json()["content"] == "Hello, World!"


def test_move_file():
    """
    Test moving a file from one location to another.
    """
    client.post("/create", json={"path": "", "entity_type": "drive", "name": "C"})  # Ensure /C exists
    client.post("/create", json={"path": "/C", "entity_type": "folder", "name": "Documents"})  # Ensure /C/Documents exists
    client.post("/create", json={"path": "/C", "entity_type": "folder", "name": "OtherFolder"})  # Ensure target exists
    client.post("/create", json={"path": "/C/Documents", "entity_type": "file", "name": "file1.txt"})  # Ensure file exists

    response = client.post(
        "/move",
        json={"source_path": "/C/Documents/file1.txt", "destination_path": "/C/OtherFolder"}
    )
    print(response.json())  # Debug response
    assert response.status_code == 200
    assert response.json()["message"] == "Moved /C/Documents/file1.txt to /C/OtherFolder."


def test_list_contents():
    """
    Test listing the contents of a folder.
    """
    client.post("/create", json={"path": "", "entity_type": "drive", "name": "C"})  # Ensure /C exists
    client.post("/create", json={"path": "/C", "entity_type": "folder", "name": "Documents"})  # Ensure /C/Documents exists
    client.post("/create", json={"path": "/C/Documents", "entity_type": "file", "name": "file1.txt"})  # Add file

    response = client.get("/list?path=/C")
    print(response.json())  # Debug response
    assert response.status_code == 200

    # Extract folder and file names for comparison
    items = response.json()["items"]
    item_names = {item["name"] for item in items}
    assert "Documents" in item_names


def test_delete_file():
    """
    Test deleting a file in the virtual file system.
    """
    client.post("/create", json={"path": "", "entity_type": "drive", "name": "C"})  # Ensure /C exists
    client.post("/create", json={"path": "/C", "entity_type": "folder", "name": "Documents"})  # Ensure /C/Documents exists
    client.post("/create", json={"path": "/C/Documents", "entity_type": "file", "name": "file1.txt"})  # Ensure file exists

    response = client.delete("/delete?path=/C/Documents/file1.txt")
    print(response.json())  # Debug response
    assert response.status_code == 200
    assert response.json()["message"] == "Entity at /C/Documents/file1.txt deleted successfully."
