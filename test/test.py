import requests
import os
import json
import datetime
from persiantools.jdatetime import JalaliDate
import openpyxl
from io import BytesIO

API_URL = 'https://localhost'
USER = os.environ.get('TEST_USER')
PASS = os.environ.get('TEST_PASS')
API_URL_AUTHED = f'https://{USER}:{PASS}@localhost'

def test_service_available():
    response = requests.get(API_URL, verify=False)
    assert response.status_code == 200

def test_excel_data():
    response = requests.post(f"{API_URL_AUTHED}/rollouts/", verify=False)
    print("Create Rollout Response: " + response.content)
    response_json = json.loads(response.content)
    time_str = response_json.get('time')
    time = datetime.datetime.fromisoformat(time_str)
    jdate = JalaliDate(time)

    response = requests.get(f"{API_URL}/{USER}/{jdate.year}/{jdate.month}/timesheet.xlsx", verify=False)
    workbook = openpyxl.load_workbook(BytesIO(response.content))
    sheet = workbook.active
    assert sheet[f'D{4 + jdate.day}'].value == time.strftime('%H:%M')
    
def test_user_details():
    jdate = JalaliDate(datetime.datetime.now())
    response = requests.get(f"{API_URL}/{USER}/{jdate.year}/{jdate.month}/timesheet.xlsx", verify=False)
    workbook = openpyxl.load_workbook(BytesIO(response.content))
    sheet = workbook.active
    assert sheet['R1'].value == 'سردار آزمون'
    assert sheet['R2'].value == '1234'
    assert sheet['R3'].value == 'علی'