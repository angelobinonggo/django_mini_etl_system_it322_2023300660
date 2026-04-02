# Mini ETL System (Django)

A mini Extract, Transform, Load (ETL) pipeline built with Django. This system allows you to upload CSV files, extract the raw data, clean and standardize it (handling missing values, formatting text), and load it into a final structured database table, all managed via a web interface dashboard.

## Features

- **Dashboard**: View pipeline status, total records extracted, transformed, and loaded.
- **Data Upload**: Upload CSV files containing raw data (e.g., student files).
- **Data Extraction**: Extract raw data from CSV files and load it into a staging database table.
- **Data Transformation**: Clean missing data, standardize string formats, and process records.
- **Data Loading**: Move processed records into clean reporting tables.
- **Results View**: View and compare the data after it passes through the pipeline.

## Technologies Used

- **Backend**: Python, Django
- **Frontend**: HTML, CSS 
- **Database**: SQLite (default Django database)
- **Data Processing**: Python csv module

## Setup & Execution

### Prerequisites

- Python 3.8+ installed
- `pip` for installing packages

### Installation

1. **Navigate to the project directory*:
   ```bash
   cd django_mini_etl_system_2023300660
   ```

2. **Create a virtual environment (optional but recommended)**:
   ```bash
   python -m venv venv
   # Activate on Windows:
   venv\Scripts\activate
   # Activate on macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install django
   ```

4. **Apply database migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

### Usage

1. Open your web browser and go to `http://127.0.0.1:8000/`.
2. Follow the steps provided in the dashboard starting with uploading a valid CSV file (e.g., `students.csv`).
3. Proceed step-by-step to Extract, Transform, and Load the data.
4. You can monitor the operation status directly on the dashboard page.

## Project Structure

- `etlproject/`: Main Django project directory containing settings and root URL configuration.
- `etlapp/`: Core Django app handling the ETL logic, models, views, and urls.
- `templates/`: HTML templates for rendering the web interface.
- `students.csv`: A sample dataset provided to test the ETL workflow.
