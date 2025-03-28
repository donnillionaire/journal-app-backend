# FastAPI Backend Launch Guide

This guide provides step-by-step instructions to set up and launch the FastAPI backend after cloning from the GitHub repository.

## Prerequisites
Before starting, ensure you have the following installed:
- **Python (3.8 or later)**
- **pip** (Python package manager)
- **Git**
- **Virtual Environment (optional but recommended)**

## Step 1: Clone the Repository
Open your terminal or command prompt and run the following command to clone the repository:

```sh
git clone https://github.com/donnillionaire/journal-app-backend.git
```

## Step 2: Navigate into the Project Folder
Once the repository is cloned, move into the project directory:

```sh
cd journal-app-backend
```

## Step 3: Create and Activate a Virtual Environment (Optional but Recommended)
To avoid dependency conflicts, create a virtual environment and activate it:

### On macOS and Linux:
```sh
python3 -m venv venv
source venv/bin/activate
```

### On Windows:
```sh
python -m venv venv
venv\Scripts\activate
```

## Step 4: Install Dependencies
Install the required Python packages using:

```sh
pip install -r requirements.txt
```

## Step 5: Run Database Migrations (If Applicable)
If the project uses database migrations (e.g., Alembic), apply them using:

```sh
alembic upgrade head
```

## Step 6: Launch the FastAPI Server
Start the FastAPI application using Uvicorn:

```sh
uvicorn app.main:app --reload
```

## Step 7: Access the API
Once the server is running, you can access the API documentation at:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Troubleshooting
- If you encounter issues, ensure all dependencies are installed correctly.
- Check if the required environment variables are set.
- Verify that the database is running if the app relies on one.
- Use `uvicorn app.main:app` to see detailed logs.

## Conclusion
Following these steps will successfully launch the FastAPI backend. Ensure you have the correct configurations set up for smooth operation.

