from io import BytesIO
import openpyxl
from persiantools.jdatetime import JalaliDate, JalaliDateTime
import datetime
import pytz
from django.conf import settings

from rollcall.models import Rollout


class ExcelConverter:
    DATA_FIRST_ROW = 5
    DATA_FIRST_COLUMN = 4
    WEEK_DAY_STRS = [
        'شنبه',
        'یکشنبه',
        'دوشنبه',
        'سه شنبه',
        'چهارشنبه',
        'پنجشنبه',
        'جمعه',
    ]

    @staticmethod
    def generateExcelFile(user, j_year, j_month) -> BytesIO:
        date_from = JalaliDateTime(year=j_year, month=j_month, day=1).to_gregorian()
        next_j_month = j_month % 12 + 1
        date_to = JalaliDateTime(year=j_year, month=next_j_month, day=1).to_gregorian()
        rollouts = Rollout.objects \
            .filter(user=user) \
            .filter(time__gte=date_from,
                    time__lt=date_to) \
            .order_by('time')
        excel_file = ExcelConverter(user, rollouts, starting_date=date_from).get_excel_file()
        return excel_file

    def __init__(self, user, rollouts, starting_date):
        self.rollouts = rollouts
        self.user = user
        self.starting_date = starting_date
        self.starting_date_jalali = JalaliDate(starting_date)

    def get_excel_file(self):
        workbook = openpyxl.load_workbook("./timesheet-template.xlsx")
        sheet = workbook.active
        self.__fill_header_info(sheet)
        self.__fill_date_info(sheet)
        self.__fill_days(sheet)
        self.__fill_data(sheet)
        return BytesIO(openpyxl.writer.excel.save_virtual_workbook(workbook))

    def __fill_days(self, sheet):
        total_days = JalaliDate.days_in_month(
            month=self.starting_date_jalali.month, year=self.starting_date_jalali.year)
        for i in range(0, total_days):
            day = self.starting_date_jalali + datetime.timedelta(days=i)
            week_day_str = self.WEEK_DAY_STRS[day.weekday()]
            sheet[self.__get_cell_label(self.DATA_FIRST_ROW + i, self.DATA_FIRST_COLUMN - 1)] = week_day_str

    @staticmethod
    def __get_cell_label(row, col):
        return f"{openpyxl.utils.get_column_letter(col)}{row}"

    def __fill_date_info(self, sheet):
        sheet[self.__get_cell_label(44, 2)] = self.starting_date_jalali.month
        sheet[self.__get_cell_label(44, 3)] = self.starting_date_jalali.year - 1398

    def __fill_header_info(self, sheet):
        sheet['R1'] = self.user.first_name + ' ' + self.user.last_name
        sheet['R2'] = self.user.detail.personnel_code
        sheet['R3'] = self.user.detail.manager_name
        sheet['E3'] = self.user.detail.unit

    def __fill_data(self, sheet):
        for row in range(self.DATA_FIRST_ROW, self.DATA_FIRST_ROW + 31):
            for col in range(self.DATA_FIRST_COLUMN, self.DATA_FIRST_COLUMN + 11):
                sheet[self.__get_cell_label(row, col)] = '00:00'

        current_row_number = self.DATA_FIRST_ROW - 1
        last_day = -1
        current_column_number = self.DATA_FIRST_COLUMN
        for rollout in self.rollouts:
            rtime = rollout.time.astimezone(pytz.timezone(settings.TIME_ZONE))
            day_of_month = JalaliDateTime(rtime).day
            if last_day != day_of_month:
                current_row_number += 1
                current_column_number = self.DATA_FIRST_COLUMN
                last_day = day_of_month

            while (current_row_number - self.DATA_FIRST_ROW + 1) < day_of_month:
                current_row_number += 1
            sheet[self.__get_cell_label(current_row_number,
                                        current_column_number)] \
                = rtime.strftime('%H:%M')
            current_column_number += 1
