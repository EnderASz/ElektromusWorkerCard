from apps.backend.users.models import WorkTimestamp, Worker
from datetime import date

def worked(worker: Worker, date: date) -> bool:
    return WorkTimestamp.objects.filter(
        user=worker.user,
        working_after=True,
        timestamp__date=date
    ).exists()

def get_work(worker: Worker, date: date):
    work_start = WorkTimestamp.objects.filter(
        user=worker.user,
        timestamp__date=date,
        working_after=True).first()
    if work_start:
        work_end = WorkTimestamp.objects.filter(
            user=worker.user,
            working_after=False,
            timestamp__gt=work_start.timestamp
            ).order_by('timestamp').first()
        return (work_start, work_end, work_start.location)
    return None
