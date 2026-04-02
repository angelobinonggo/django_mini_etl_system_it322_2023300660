from django.db import models


# Source table - raw extracted data
class StudentRaw(models.Model):
    student_id = models.IntegerField()
    name = models.CharField(max_length=100, null=True, blank=True)
    course = models.CharField(max_length=50, null=True, blank=True)
    extracted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Raw Student Record"
        verbose_name_plural = "Raw Student Records"

    def __str__(self):
        return f"RAW [{self.student_id}] {self.name or 'N/A'}"


# Target table - cleaned/transformed data
class StudentClean(models.Model):
    student_id = models.IntegerField()
    full_name = models.CharField(max_length=100)
    course = models.CharField(max_length=50)
    loaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Clean Student Record"
        verbose_name_plural = "Clean Student Records"

    def __str__(self):
        return f"CLEAN [{self.student_id}] {self.full_name}"


# ETL Run log - tracks each pipeline execution
class ETLLog(models.Model):
    STATUS_CHOICES = [
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
        ('RUNNING', 'Running'),
    ]
    run_at = models.DateTimeField(auto_now_add=True)
    filename = models.CharField(max_length=255, default='students.csv')
    rows_extracted = models.IntegerField(default=0)
    rows_loaded = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='RUNNING')
    message = models.TextField(blank=True)

    class Meta:
        verbose_name = "ETL Log"
        verbose_name_plural = "ETL Logs"
        ordering = ['-run_at']

    def __str__(self):
        return f"ETL Run @ {self.run_at:%Y-%m-%d %H:%M} — {self.status}"
