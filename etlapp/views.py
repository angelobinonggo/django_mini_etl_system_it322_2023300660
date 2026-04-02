import os
from django.shortcuts import render, redirect
from django.contrib import messages
from .etl import run_etl
from .models import StudentRaw, StudentClean, ETLLog


def upload_and_run(request):
    """Handle CSV upload and trigger the full ETL pipeline."""
    if request.method == "POST":
        if 'csvfile' not in request.FILES:
            messages.error(request, "No file was uploaded.")
            return redirect("etl")

        csv_file = request.FILES['csvfile']
        filename = csv_file.name

        # Validate file type
        if not filename.endswith('.csv'):
            messages.error(request, "Only CSV files are accepted.")
            return redirect("etl")

        # Save uploaded file temporarily
        save_path = os.path.join(os.getcwd(), "students.csv")
        with open(save_path, "wb+") as f:
            for chunk in csv_file.chunks():
                f.write(chunk)

        # Run ETL pipeline
        try:
            log = run_etl(filepath=save_path, filename=filename)
            messages.success(
                request,
                f"ETL completed! {log.rows_extracted} rows extracted, {log.rows_loaded} rows loaded."
            )
        except Exception as e:
            messages.error(request, f"ETL failed: {e}")

        return redirect("results")

    return render(request, "etlapp/upload.html")


def results_view(request):
    """Show raw vs. clean data and ETL logs."""
    raw_records = StudentRaw.objects.all().order_by('student_id')
    clean_records = StudentClean.objects.all().order_by('student_id')
    logs = ETLLog.objects.all()[:10]
    return render(request, "etlapp/results.html", {
        "raw_records": raw_records,
        "clean_records": clean_records,
        "logs": logs,
    })


def dashboard_view(request):
    """Landing dashboard with pipeline stats."""
    total_raw = StudentRaw.objects.count()
    total_clean = StudentClean.objects.count()
    last_log = ETLLog.objects.first()
    logs = ETLLog.objects.all()[:5]
    return render(request, "etlapp/dashboard.html", {
        "total_raw": total_raw,
        "total_clean": total_clean,
        "last_log": last_log,
        "logs": logs,
    })
