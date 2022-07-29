import json
import gspread


gc = gspread.service_account(filename='./keys/creds.json')
sh = gc.open("KazanExpress")


def write_sheet():
    with open('./data/data.json', 'r') as file:
        data = json.load(file)
    worksheet_list = sh.worksheet('вибратор').title
    sheets_list = sh.worksheets()
    for sheet in sheets_list:
        if data.get('query') == sheet.title:
            sh.values_clear(f'{data.get("query")}!A:F')


write_sheet()
