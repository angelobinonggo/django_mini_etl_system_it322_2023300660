"""
etlapp/etl.py
ETL Pipeline: Extract → Transform → Load
"""

import pandas as pd
from .models import StudentRaw, StudentClean, ETLLog


# ─── EXTRACT ────────────────────────────────────────────────────────────────

def extract_csv(filepath="students.csv"):
    """Read CSV and insert all rows into StudentRaw (staging table)."""
    data = pd.read_csv(filepath)
    count = 0
    for _, row in data.iterrows():
        StudentRaw.objects.create(
            student_id=int(row['id']) if pd.notna(row['id']) else 0,
            name=row['name'] if pd.notna(row['name']) else None,
            course=row['course'] if pd.notna(row['course']) else None,
        )
        count += 1
    print(f"[EXTRACT] {count} rows extracted from '{filepath}'.")
    return count


# ─── TRANSFORM ──────────────────────────────────────────────────────────────

def transform_data():
    """Clean and standardize raw records."""
    raw_data = StudentRaw.objects.all()
    cleaned = []
    for student in raw_data:
        # Handle missing name
        name = student.name.strip() if student.name and student.name.strip() else "Unknown"
        # Handle missing course
        course = student.course.strip() if student.course and student.course.strip() else "Not Assigned"

        cleaned.append({
            "student_id": student.student_id,
            "full_name": name.title(),        # Title-case the name
            "course": course.upper(),          # Uppercase the course code
        })
    print(f"[TRANSFORM] {len(cleaned)} records transformed.")
    return cleaned


# ─── LOAD ────────────────────────────────────────────────────────────────────

def load_data(cleaned_data):
    """Insert transformed records into StudentClean (target table)."""
    count = 0
    for row in cleaned_data:
        StudentClean.objects.create(
            student_id=row['student_id'],
            full_name=row['full_name'],
            course=row['course'],
        )
        count += 1
    print(f"[LOAD] {count} records loaded into StudentClean.")
    return count


# ─── PIPELINE ────────────────────────────────────────────────────────────────

def run_etl(filepath="students.csv", filename="students.csv"):
    """
    Full ETL pipeline with logging.
    Returns the ETLLog instance.
    """
    log = ETLLog.objects.create(filename=filename, status='RUNNING')
    try:
        # Clear previous data to avoid duplication on re-runs
        StudentRaw.objects.all().delete()
        StudentClean.objects.all().delete()

        extracted = extract_csv(filepath)
        cleaned = transform_data()
        loaded = load_data(cleaned)

        log.rows_extracted = extracted
        log.rows_loaded = loaded
        log.status = 'SUCCESS'
        log.message = f"Pipeline completed successfully. {extracted} rows extracted, {loaded} rows loaded."
        log.save()
        print("[ETL] Pipeline finished successfully.")
    except Exception as e:
        log.status = 'FAILED'
        log.message = str(e)
        log.save()
        print(f"[ETL] Pipeline failed: {e}")
        raise

    return log
