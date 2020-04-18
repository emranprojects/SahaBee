import io
import openpyxl
from persiantools.jdatetime import JalaliDate
import datetime
import pytz
from django.conf import settings


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

    def __init__(self, rollouts, starting_date):
        self.rollouts = rollouts
        self.starting_date = starting_date
        self.starting_date_jalali = JalaliDate(starting_date)

    def get_excel_file(self):
        workbook = openpyxl.load_workbook("./timesheet-template.xlsx")
        sheet = workbook.active
        self.__fill_header_info(sheet)
        self.__fill_days(sheet)
        self.__fill_data(sheet)
        return io.BytesIO(openpyxl.writer.excel.save_virtual_workbook(workbook))

    def __fill_days(self, sheet):
        total_days = JalaliDate.days_in_month(
            month=self.starting_date_jalali.month, year=self.starting_date_jalali.year)
        for i in range(0, total_days):
            day = self.starting_date + datetime.timedelta(days=i)
            week_day_str = self.WEEK_DAY_STRS[day.weekday()]
            sheet[self.__get_cell_label(self.DATA_FIRST_ROW + i, self.DATA_FIRST_COLUMN - 1)] = week_day_str

    @staticmethod
    def __get_cell_label(row, col):
        return f"{openpyxl.utils.get_column_letter(col)}{row}"

    def __fill_header_info(self, sheet):
        sheet[self.__get_cell_label(1,1)] = self.starting_date_jalali.month
        sheet[self.__get_cell_label(2,1)] = self.starting_date_jalali.year

    def __fill_data(self, sheet):
        current_row_number = self.DATA_FIRST_ROW - 1
        last_day = -1
        current_column_number = self.DATA_FIRST_COLUMN
        for rollout in self.rollouts:
            day_of_month = JalaliDate(rollout.time).day
            if last_day != day_of_month:
                current_row_number += 1
                current_column_number = self.DATA_FIRST_COLUMN
                last_day = day_of_month

            while (current_row_number - self.DATA_FIRST_ROW + 1) < day_of_month:
                current_row_number += 1
            sheet[self.__get_cell_label(current_row_number,
                                        current_column_number)] \
                = rollout.time.astimezone(pytz.timezone(settings.TIME_ZONE)).strftime('%H:%M')
            current_column_number += 1
