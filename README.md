# File Upload

This is a simple Flask-based file upload service that allows users to upload files with a specified expiration time. The uploaded files are stored in a designated folder (`uploads`) on the server.

## Features

- **File Upload**: Users can upload files through the provided interface.
- **Expiration**: Uploaded files have a configurable expiration time. After the specified time, the files are automatically deleted from the server.
- **RESTful API**: The service provides a RESTful API for uploading files and retrieving uploaded files.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/glad432/temp-file.git
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the Flask application:

    ```bash
    python app.py
    ```

2. Access the application in your browser at `http://localhost:5000`.

## Endpoints

- `GET /`: Homepage with file upload interface.
- `POST /upload`: Endpoint to upload files with optional expiration time.
- `GET /uploads/<filename>`: Endpoint to retrieve uploaded files.

## Configuration

- `UPLOAD_FOLDER`: Directory where uploaded files are stored.
- `DEFAULT_EXPIRATION_HOURS`: Default expiration time for uploaded files (in hours).