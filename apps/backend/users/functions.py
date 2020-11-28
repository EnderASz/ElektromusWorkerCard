import xlsxwriter
import io
from decimal import Decimal

from .models import WorkTimestamp, Worker, AdditionalWorkTime
from django.contrib.auth.models import User
from django.utils import timezone

def add_work_time(worker: Worker, minutes: int, date=timezone.localdate()):
    current = AdditionalWorkTime.objects.filter(
        user=worker.user,
        date=date
        ).first()
    if not current:
        current = AdditionalWorkTime.objects.create(
            user=worker.user,
            date=date,
            time_minutes=minutes
        )
    else:
        current.time_minutes += minutes
    current.save()    

def update_password(user, new_password):
    user.set_password(new_password)
    user.save()

def delete_user(user: User):
    user.delete()

def create_user(auth_user, user_info):
    if auth_user.is_staff:
        user = User.objects.create_user(
            user_info.get('username'),
            None,
            user_info.get('password'))
        user.is_staff = auth_user.is_superuser and user_info.get('is_admin')
        if user_info.get('is_worker'):
            rate = float(user_info.get('rate'))
            worker = Worker.objects.create(user=user, rate_per_hour=rate)

def update_user(auth_user, user_new_info):
    if auth_user.is_staff:
        user_id = user_new_info.get('id')

        if(user_id != ""):
            forced_work_end = False
            user = User.objects.get(id=user_id)
            user.username = user_new_info['username']
            if auth_user.is_superuser:
                user.is_staff = True if user_new_info.get('is_admin') else False
            user.save()
            worker = Worker.objects.filter(user=user).first()
            if user_new_info.get('is_worker'):
                rate = float(user_new_info.get('rate'))
                if not worker:
                    worker = Worker.objects.create(user=user, rate_per_hour=rate)
                else:
                    worker.rate_per_hour = rate
                    worker.save()
            elif worker:
                worker.delete()
                last_work_start = WorkTimestamp.objects.filter(
                    user=user,
                    working_after=True
                    ).order_by('-timestamp').first()
                if last_work_start:
                    last_work_end = WorkTimestamp.objects.filter(
                    user=user,
                    working_after=False,
                    timestamp__gt=last_work_start.timestamp
                    ).first()
                    if not last_work_end:
                        last_work_end = WorkTimestamp.objects.create(
                            user=user,
                            working_after=False)
                        forced_work_end = True
            return {
                'user': user,
                'worker': worker,
                'forced_work_end': forced_work_end
            }
        return create_user(auth_user, user_new_info)
    return False

def date_range(start, end, end_included=False):
    for day_index in range(int((end - start).days) + end_included):
        yield start + timezone.timedelta(day_index)

def get_xlsx(users, start_date, end_date):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()

    border_styles = {
        'continue': 1,
        'bold_continue': 2,
        'dash_dot': 9,
        'dash': 3}
    field_formats = {
        'data_type': workbook.add_format({
            'bold': True,
            'bg_color': '#FFF200',
            'align': 'center',
            'valign': 'vcenter',
            'border': border_styles['bold_continue']}),
        'date': {
            'standard': workbook.add_format({
                'align': 'center',
                'num_format': 'dd/mm/yyyy',
                'border': border_styles['continue']}),
            'first': workbook.add_format({
                'align': 'center',
                'num_format': 'dd/mm/yyyy',
                'border': border_styles['continue'],
                'left': border_styles['bold_continue']}),
            'last': workbook.add_format({
                'align': 'center',
                'num_format': 'dd/mm/yyyy',
                'border': border_styles['continue'],
                'right': border_styles['bold_continue']})},
       'time_from': {
            'title': workbook.add_format({
                'bg_color': '#DDDDDD',
                'align': 'center',
                'right': border_styles['dash'],
                'bottom': border_styles['continue']}),
            'data': {
                'standard': workbook.add_format({
                    'bg_color': '#DDDDDD',
                    'align': 'center',
                    'num_format': 'hh:mm',
                    'left': border_styles['continue'],
                    'right': border_styles['dash'],
                    'bottom': border_styles['dash_dot']}),
                'bottom': workbook.add_format({
                    'bg_color': '#DDDDDD',
                    'align': 'center',
                    'num_format': 'hh:mm',
                    'right': border_styles['continue'],
                    'bottom': border_styles['bold_continue']})}},
        'time_to': {
            'title': {
                'standard': workbook.add_format({
                    'bg_color': '#CCCCCC',
                    'align': 'center',
                    'right': border_styles['continue'],
                    'bottom': border_styles['continue']}),
                'last': workbook.add_format({
                    'bg_color': '#CCCCCC',
                    'align': 'center',
                    'right': border_styles['bold_continue'],
                    'bottom': border_styles['continue']})},
            'data': {
                'standard': workbook.add_format({
                    'bg_color': '#CCCCCC',
                    'align': 'center',
                    'num_format': 'hh:mm',
                    'right': border_styles['dash'],
                    'bottom': border_styles['dash_dot']}),
                'bottom': workbook.add_format({
                    'bg_color': '#CCCCCC',
                    'align': 'center',
                    'num_format': 'hh:mm',
                    'right': border_styles['continue'],
                    'bottom': border_styles['bold_continue']})}},
        'additional_time' : {
            'title': {
                'standard': workbook.add_format({
                    'bg_color': '#B2B2B2',
                    'align': 'center',
                    'right': border_styles['continue'],
                    'bottom': border_styles['continue']}),
                'last': workbook.add_format({
                    'bg_color': '#B2B2B2',
                    'align': 'center',
                    'right': border_styles['bold_continue'],
                    'bottom': border_styles['continue']})},
            'data': {
                'standard': workbook.add_format({
                    'bg_color': '#B2B2B2',
                    'align': 'center',
                    'num_format': 'hh:mm',
                    'right': border_styles['continue'],
                    'bottom': border_styles['dash_dot']}),
                'bottom': workbook.add_format({
                    'bg_color': '#B2B2B2',
                    'align': 'center',
                    'num_format': 'hh:mm',
                    'right': border_styles['continue'],
                    'bottom': border_styles['bold_continue']})}
        },
        'localization': {
            'standard': workbook.add_format({
                    'bg_color': '#FFFFFF',
                    'align': 'center',
                    'right': border_styles['continue'],
                    'bottom': border_styles['dash_dot']}),
            'bottom': workbook.add_format({
                    'bg_color': '#FFFFFF',
                    'align': 'center',
                    'right': border_styles['continue'],
                    'bottom': border_styles['bold_continue']})
        },
        'worker': {
            'standard': workbook.add_format({
                'valign': 'vcenter',
                'left': border_styles['bold_continue'],
                'right': border_styles['continue'],
                'bottom': border_styles['dash_dot']
            }),
            'bottom': workbook.add_format({
                'valign': 'vcenter',
                'left': border_styles['bold_continue'],
                'right': border_styles['continue'],
                'bottom': border_styles['bold_continue']})},
        'rate': {
            'standard': workbook.add_format({
                'num_format': '#,##0.00" zł"',
                'align': 'center',
                'valign': 'vcenter',
                'left': border_styles['bold_continue'],
                'right': border_styles['continue'],
                'bottom': border_styles['dash_dot']
            }),
            'bottom': workbook.add_format({
                'num_format': '#,##0.00" zł"',
                'align': 'center',
                'valign': 'vcenter',
                'left': border_styles['bold_continue'],
                'right': border_styles['continue'],
                'bottom': border_styles['bold_continue']
            })
        },
        'salary': {
            'standard': workbook.add_format({
                'num_format': '#,##0.00"zł"',
                'align': 'center',
                'valign': 'vcenter',
                'left': border_styles['bold_continue'],
                'right': border_styles['bold_continue'],
                'bottom': border_styles['dash_dot']
            }),
            'bottom': workbook.add_format({
                'num_format': '#,##0.00" zł"',
                'align': 'center',
                'valign': 'vcenter',
                'left': border_styles['bold_continue'],
                'right': border_styles['bold_continue'],
                'bottom': border_styles['bold_continue']
            }),
        }}
    
    users_amount = len(users) if isinstance(users, list) else users.count()
    days = list(date_range(start_date, end_date, True))

    #Set data types names fields
    worksheet.set_column(0, 1, 11)
    worksheet.merge_range(
        2, 0,
        2, 1,
        "Pracownicy",
        field_formats['data_type'])
    worksheet.write(
        3, 0,
        "Nazwa",
        field_formats['data_type'])
    worksheet.write(
        3, 1,
        "Stawka/h",
        field_formats['data_type'])

    worksheet.merge_range(
        1, 2,
        1, 1+3*len(days),
        "Dni pracy",
        field_formats['data_type'])

    worksheet.write(
        3,
        2+len(days)*3,
        "Przepracowano",
        field_formats['data_type']
    )
    worksheet.write(
        3,
        3+len(days)*3,
        "Wynagrodzenie",
        field_formats['data_type']
    )
    worksheet.set_column(2+len(days)*3, 3+len(days)*3, 15)

    for d_index, day in enumerate(days):
        col = (2+d_index*3, 3+d_index*3, 4+d_index*3)
        worksheet.set_column(col[0], col[2], 5.67)
        worksheet.merge_range(
            2, col[0],
            2, col[2],
            day.strftime('%d.%m.%Y'),
            field_formats['date'][
                'last' if d_index == len(days)-1 else (
                    'first' if not d_index else 'standard')])
        worksheet.write(
            3, col[0],
            "Od",
            field_formats['time_from']['title'])
        worksheet.write(
            3, col[1],
            "Do",
            field_formats['time_to']['title']['standard'])
        worksheet.write(
            3, col[2],
            "Dodt.",
            field_formats['additional_time']['title'][
                'last' if d_index == len(days)-1 else 'standard'])

    for u_index, user in enumerate(users):
        last_user = u_index == users_amount-1
        first_row = 4+u_index*2

        work_time_minutes = 0

        worksheet.merge_range(
            first_row, 0,
            first_row+1, 0,
            user.username,
            field_formats['worker']['bottom' if last_user else 'standard']
        )
        worker = Worker.objects.filter(user=user).first()
        if worker:
            rate = worker.rate_per_hour
        else:
            rate = "N/A"
        worksheet.merge_range(
            first_row, 1,
            first_row+1, 1,
            rate,
            field_formats['rate']['bottom' if last_user else 'standard']
        )

        for d_index, day in enumerate(days):
            last_day = d_index == len(days)-1
            col = (2+d_index*3, 3+d_index*3, 4+d_index*3)

            work_start = WorkTimestamp.objects.filter(
                user=user,
                timestamp__date=day,
                working_after=True).order_by('timestamp').first()
            print(day)
            if work_start:
                localization = work_start.location
                time_from = work_start.timestamp.strftime('%H:%M')
                work_end = WorkTimestamp.objects.filter(
                    user=user,
                    timestamp__gt=work_start.timestamp,
                    working_after=False).order_by('timestamp').first()
                if work_end:
                    time_to = work_end.timestamp.strftime('%H:%M')
                    work_time_minutes += (work_end.timestamp - work_start.timestamp).seconds//60
                else:
                    time_to = "--:--"
                    work_time_minutes += (timezone.now()+timezone.timedelta(hours=1) - work_start.timestamp).seconds//60
            else:
                localization = "N/A"
                time_from, time_to = "--:--", "--:--"
            additional_time = AdditionalWorkTime.objects.filter(user=user, date=day).first()
            if additional_time:
                additional_minutes = additional_time.time_minutes
                work_time_minutes += additional_minutes
                additional_time = f'{str(additional_minutes//60).zfill(2)}:{str(additional_minutes%60).zfill(2)}'
            else:
                additional_time = "--:--"
            
            print(f"[{user.username} - {day.day}] {time_from} <-> {time_to}")

            worksheet.write(
                first_row, col[0],
                time_from,
                field_formats['time_from']['data']['standard'])
            worksheet.write(
                first_row, col[1],
                time_to,
                field_formats['time_to']['data']['standard'])
            worksheet.write(
                first_row, col[2],
                additional_time,
                field_formats['additional_time']['data']['standard'])

            if last_user:
                worksheet.merge_range(
                    first_row+1, col[0],
                    first_row+1, col[2],
                    localization,
                    field_formats['localization']['bottom'])
            else:
                worksheet.merge_range(
                    first_row+1, col[0],
                    first_row+1, col[2],
                    localization,
                    field_formats['localization']['standard'])
        worksheet.merge_range(
            first_row, 2+len(days)*3,
            first_row+1, 2+len(days)*3,
            f"{str(work_time_minutes//60).zfill(2)}:{str(work_time_minutes%60).zfill(2)}",
            field_formats['rate']['bottom' if last_user else 'standard']
        )
        worksheet.merge_range(
            first_row, 3+len(days)*3,
            first_row+1, 3+len(days)*3,
            f"{Decimal(work_time_minutes)/60*rate:.2f}zł" if rate != "N/A" else "N/A",
            field_formats['salary']['bottom' if last_user else 'standard'])

    workbook.close()
    output.seek(0)
    return output

