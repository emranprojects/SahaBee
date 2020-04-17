import requests
import os
import json
import datetime
from persiantools.jdatetime import JalaliDate
import openpyxl
from io import BytesIO

API_URL = 'http://localhost:8000'
USER = os.environ.get('TEST_USER')
PASS = os.environ.get('TEST_PASS')
API_URL_AUTHED = f'http://{USER}:{PASS}@localhost:8000'

def test_service_available():
    response = requests.get(API_URL)
    assert response.status_code == 200

def test_excel_data():
    response = requests.post(f"{API_URL_AUTHED}/rollouts/")
    response_json = json.loads(response.content)
    time = datetime.datetime.fromisoformat(response_json.get('time'))
    jdate = JalaliDate(time)

    response = requests.get(f"{API_URL}/{USER}/{jdate.year}/{jdate.month}/timesheet.xlsx")
    workbook = openpyxl.load_workbook(BytesIO(response.content))
    sheet = workbook.active
    assert sheet[f'D{4 + jdate.day}'].value == time.strftime('%H:%M')