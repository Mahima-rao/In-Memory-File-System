# File System API

This project implements a virtual file system using FastAPI and Python. The system supports basic file and folder management functionalities such as creating, moving, deleting, reading, and writing files. Additionally, it allows users to list the contents of directories, making it a fully functional virtual file management system.

## Features
- **Create drives, folders, and files**: Create new entities in the file system.
- **Write content to files**: Write data to files within the virtual file system.
- **Read content from files**: Read the content stored in any file.
- **Move files between folders**: Move files or folders to different locations.
- **Delete files or folders**: Delete files or entire directories.
- **List contents of a folder**: View the files and folders within any given directory.

## Project Structure
- **`main.py`**: Contains the FastAPI application, file system logic, and API routes.
- **`test_file.py`**: Contains the test cases to verify the correctness of the system.
- **`README.md`**: This file!

## Installation and Setup

To set up the project on your local machine, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/file-system-api.git
    ```

2. **Navigate to the project directory**:
    ```bash
    cd file-system-api
    ```

3. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the FastAPI application**:
    ```bash
    uvicorn main:app --reload
    ```

The application will be available at `http://127.0.0.1:8000`.

## Postman Requests

You can use Postman to interact with the API. Here are some sample commands for testing:

### Create Folder
- **Method**: `POST`
- **URL**: `http://127.0.0.1:8000/create`
- **Body (JSON)**:
    ```json
    {
        "path": "/C",
        "entity_type": "folder",
        "name": "Documents"
    }
    ```

### Write Content to File
- **Method**: `POST`
- **URL**: `http://127.0.0.1:8000/write`
- **Body (JSON)**:
    ```json
    {
        "path": "/C/Documents/file1.txt",
        "content": "Hello, World!"
    }
    ```

### Read Content from File
- **Method**: `GET`
- **URL**: `http://127.0.0.1:8000/read?path=/C/Documents/file1.txt`

### Move File
- **Method**: `POST`
- **URL**: `http://127.0.0.1:8000/move`
- **Body (JSON)**:
    ```json
    {
        "source_path": "/C/Documents/file1.txt",
        "destination_path": "/C/OtherFolder"
    }
    ```

### Delete File
- **Method**: `DELETE`
- **URL**: `http://127.0.0.1:8000/delete?path=/C/Documents/file1.txt`

### List Contents of Folder
- **Method**: `GET`
- **URL**: `http://127.0.0.1:8000/list?path=/C`

## Testing

### The test_file.py file contains the tests that verify if the File System API is functioning correctly. Here's a brief overview of the tests performed:

### What the test file does:
**Test Case for Creating Entities:**
***Verifies that files, folders, and drives are created correctly when a valid request is made.***
***Checks that the appropriate success message is returned.***

**Test Case for Writing Content to Files:**
***Verifies that content is written to a file when a valid request is made.***

**Test Case for Reading Content from Files:**
***Ensures that the correct content is returned when reading a file.***

**Test Case for Moving Files:**
***Tests the ability to move a file from one folder to another and ensures the file is in the destination folder after the move.***

**Test Case for Deleting Entities:**
***Verifies that files and folders are deleted correctly when requested, and checks that the appropriate success message is returned.***

**Test Case for Listing Directory Contents:**
***Ensures that the contents of a folder are listed correctly, including verifying that files and folders are correctly identified and listed.***

**This project uses pytest for testing. To run the tests, use the following command:**

```bash
pytest test\test.py
