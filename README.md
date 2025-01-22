<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>File System API</title>
</head>
<body>
    <h1>File System API</h1>
    <p>This project implements a virtual file system using FastAPI and Python. The system supports basic file and folder management functionalities such as creating, moving, deleting, reading, and writing files, along with the ability to list the contents of directories.</p>

    <h2>Project Structure</h2>
    <ul>
        <li><strong>main.py</strong> - Contains the FastAPI application, file system logic, and API routes.</li>
        <li><strong>test_file.py</strong> - Contains the test cases to verify the correctness of the system.</li>
        <li><strong>README.html</strong> - This file!</li>
    </ul>

    <h2>Features</h2>
    <ul>
        <li>Create drives, folders, and files.</li>
        <li>Write content to files.</li>
        <li>Read content from files.</li>
        <li>Move files between folders.</li>
        <li>Delete files or folders.</li>
        <li>List contents of a folder.</li>
    </ul>

    <h2>API Endpoints</h2>
    <h3>/create</h3>
    <p><strong>Method:</strong> POST</p>
    <p><strong>Description:</strong> Creates a new drive, folder, or file.</p>
    <h4>Request Body:</h4>
    <pre>
    {
        "path": "/C",
        "entity_type": "folder",  // Options: "drive", "folder", "file"
        "name": "Documents"
    }
    </pre>
    <h4>Response:</h4>
    <pre>
    {
        "message": "Folder Documents created successfully."
    }
    </pre>

    <h3>/write</h3>
    <p><strong>Method:</strong> POST</p>
    <p><strong>Description:</strong> Writes content to a file.</p>
    <h4>Request Body:</h4>
    <pre>
    {
        "path": "/C/Documents/file1.txt",
        "content": "Hello, World!"
    }
    </pre>
    <h4>Response:</h4>
    <pre>
    {
        "message": "Content written to /C/Documents/file1.txt."
    }
    </pre>

    <h3>/read</h3>
    <p><strong>Method:</strong> GET</p>
    <p><strong>Description:</strong> Reads content from a file.</p>
    <h4>Query Parameter:</h4>
    <pre>
    path: "/C/Documents/file1.txt"
    </pre>
    <h4>Response:</h4>
    <pre>
    {
        "content": "Hello, World!"
    }
    </pre>

    <h3>/move</h3>
    <p><strong>Method:</strong> POST</p>
    <p><strong>Description:</strong> Moves a file or folder to a different location.</p>
    <h4>Request Body:</h4>
    <pre>
    {
        "source_path": "/C/Documents/file1.txt",
        "destination_path": "/C/OtherFolder"
    }
    </pre>
    <h4>Response:</h4>
    <pre>
    {
        "message": "Moved /C/Documents/file1.txt to /C/OtherFolder."
    }
    </pre>

    <h3>/delete</h3>
    <p><strong>Method:</strong> DELETE</p>
    <p><strong>Description:</strong> Deletes a file or folder.</p>
    <h4>Query Parameter:</h4>
    <pre>
    path: "/C/Documents/file1.txt"
    </pre>
    <h4>Response:</h4>
    <pre>
    {
        "message": "Entity at /C/Documents/file1.txt deleted successfully."
    }
    </pre>

    <h3>/list</h3>
    <p><strong>Method:</strong> GET</p>
    <p><strong>Description:</strong> Lists the contents of a folder.</p>
    <h4>Query Parameter:</h4>
    <pre>
    path: "/C"
    </pre>
    <h4>Response:</h4>
    <pre>
    {
        "path": "/C",
        "items": [
            {
                "name": "Documents",
                "type": "folder"
            },
            {
                "name": "file1.txt",
                "type": "file"
            }
        ]
    }
    </pre>

    <h2>Installation</h2>
    <p>Follow these steps to set up and run the project:</p>
    <ul>
        <li>Clone the repository:</li>
        <pre>git clone https://github.com/your-username/file-system-api.git</pre>
        <li>Install the required dependencies:</li>
        <pre>pip install -r requirements.txt</pre>
        <li>Run the FastAPI application:</li>
        <pre>uvicorn main:app --reload</pre>
    </ul>

    <h2>Testing</h2>
    <p>This project uses pytest for testing. To run the tests, use the following command:</p>
    <pre>pytest</pre>

    <h2>Contributing</h2>
    <p>If you'd like to contribute to this project, please fork the repository, create a feature branch, make your changes, and submit a pull request.</p>

    <h2>License</h2>
    <p>This project is licensed under the MIT License - see the <a href="LICENSE">LICENSE</a> file for details.</p>
</body>
</html>
