# Student Management System

This project is a Student Management System with functionalities for managing student data including pagination and filtering.

## Backend (BE) Setup

### Prerequisites

- Python 3.x
- Django 3.x
- Django REST Framework
- SQLite (default database used in Django)


### Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd backend # Navigate to the Backend directory
2. Set up a virtual environment (optional but recommended):
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows use env\Scripts\activate

3. Install dependencies:
    ```bash 
   pip install -r requirements.txt

4. Apply migrations to set up the database:
    ```bash 
   python manage.py migrate
    
5. Load initial student data (optional):
    ```bash 
   python manage.py import_students # this will generate the required csvfile
   python manage.py import_students <pathToDataFile> # You can provide the custom CSV or JSON data file. coulmns are [name, total_marks]
    
6. Run the development server:
    ```bash 
   python manage.py runserver
The backend server will start at http://localhost:8000.

## Pagination and Filtering
Pagination: Use query parameters page and page_size to paginate through student data.

Example:
    GET http://localhost:8000/api/students/?page=1&page_size=10

Filtering: Use query parameters to filter student data.

Example:
GET http://localhost:8000/api/students/?name=John&total_marks_min=80&total_marks_max=100

## Frontend (FE) Setup
#### Prerequisites
Node.js (with npm or yarn)
1.  Installation
Navigate to the frontend directory:
    ```bash 
    cd frontend

2. Install dependencies:
    ```bash 
    npm install  # or `yarn install`
3. Start the frontend development server:
    ```bash 
    npm start  # or `yarn start`
### Usage
- Open your web browser and go to http://localhost:3000.
- Use the provided interface to filter and paginate through the list of students.
#### Example Usage
1. Pagination: Navigate through pages using the navigation buttons or input fields.

2. Filtering: Enter filter criteria such as student name, minimum and maximum total marks, and click or press enter to apply filters.





