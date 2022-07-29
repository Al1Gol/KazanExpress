import json
import time

import googleapiclient.discovery
import httplib2
from oauth2client.service_account import ServiceAccountCredentials

from config import creds_json, table_id, query
from data_parser import get_data

sheet_id = None
shop_row = []

# Функция подключения к Google Sheets


def get_service_sacc():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        creds_json, ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    )

    httpAuth = credentials.authorize(httplib2.Http())  # Авторизируемся в системе
    return googleapiclient.discovery.build("sheets", "v4", http=httpAuth)


# Функция записи в Google Sheets


def write_sheet(query):
    # Получаем данные из парсера
    data = get_data(query)
    #with open("./data/data.json", "r") as file:
    #    data = json.load(file)

    service = get_service_sacc().spreadsheets()

    # Если листа нет, то создаем. Если есть - очищаем старый
    sheets_title = {}
    sheet_metadata = service.get(spreadsheetId=table_id).execute()
    sheets = sheet_metadata.get("sheets", "")
    for item in sheets:
        sheets_title[item.get("properties").get("title")] = item

    if query in sheets_title.keys():
        sheet_id = sheets_title.get(query).get("properties").get("sheetId")

        body = {
            "requests": [
                {
                    "deleteDimension": {
                        "range": {"sheetId": sheet_id, "dimension": "ROWS", "startIndex": 1, "endIndex": 99999}
                    }
                }
            ]
        }

        response = service.batchUpdate(spreadsheetId=table_id, body=body).execute()

        body = {
            "requests": [
                {
                    "repeatCell": {
                        "range": {
                            "sheetId": sheet_id,
                            "startRowIndex": 0,
                            "endRowIndex": 1,
                        },
                        "cell": {
                            "userEnteredFormat": {
                                "textFormat": {"bold": False},
                                "horizontalAlignment": "LEFT",
                                "backgroundColor": {
                                    "green": 1,
                                    "red": 1,
                                    "blue": 1,
                                },
                            }
                        },
                        "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)",
                    }
                }
            ]
        }
        spreadsheet = service.batchUpdate(spreadsheetId=table_id, body=body).execute()

    else:

        # Создаем новый лист
        body = {"requests": {"addSheet": {"properties": {"title": query}}}}

        response = service.batchUpdate(spreadsheetId=table_id, body=body).execute()

        sheet_metadata = service.get(spreadsheetId=table_id).execute()
        sheets = sheet_metadata.get("sheets", "")

        for item in sheets:
            title = item.get("properties").get("title")

            if query == title:
                sheet_id = item.get("properties").get("sheetId")

    # Формируем тело запроса
    body = {
        "valueInputOption": "USER_ENTERED",
        "data": [
            {
                "range": f'{query}!A1:F99999',
                "majorDimension": "ROWS",  # Сначала заполнять строки, затем столбцы
                "values": [
                    [
                        "Ссылка",
                        "Магазин (название)",
                        "Наименование товара",
                        "Место выдачи (позиция)",
                        "Рейтинг",
                        "Количество заказов",
                    ],
                    # Заполняем первую строку
                ],
            }
        ],
    }

    for item in data["data"]:
        body.get("data")[0].get("values").append(item)
        if "hornY rabbiT" in item:
            shop_row.append(item[3])

    spreadsheet = service.values().batchUpdate(spreadsheetId=table_id, body=body).execute()

    # Добавляем форматирование для строк магазина
    body = {
        "requests": [
            {
                "repeatCell": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": 0,
                        "startColumnIndex": 0,
                        "endColumnIndex": 6,
                        "endRowIndex": 1,
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "backgroundColor": {
                                "green": 0.7,
                                "red": 0.3,
                                "blue": 0.9,
                            },
                            "horizontalAlignment": "CENTER",
                            "wrapStrategy": "WRAP",
                            "textFormat": {"fontSize": 11, "bold": True},
                        },
                    },
                    "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment, wrapStrategy)",
                }
            },
            {
                "repeatCell": {
                    "range": {
                        "sheetId": sheet_id,
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "wrapStrategy": "WRAP",
                        },
                    },
                    "fields": "userEnteredFormat(wrapStrategy)",
                }
            },
            {
                "updateDimensionProperties": {
                    "range": {"sheetId": sheet_id, "dimension": "COLUMNS", "startIndex": 2, "endIndex": 3},
                    "properties": {"pixelSize": 300},
                    "fields": "pixelSize",
                }
            },
                        {
            "updateDimensionProperties": {
                    "range": {"sheetId": sheet_id, "dimension": "COLUMNS", "startIndex": 0, "endIndex": 1},
                    "properties": {"pixelSize": 300},
                    "fields": "pixelSize",
                }
            },
        ]
    }
    for item in shop_row:
        range = {
            "repeatCell": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": item,
                    "startColumnIndex": 0,
                    "endColumnIndex": 6,
                    "endRowIndex": item + 1,
                },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": {
                            "green": 1,
                            "red": 0.8,
                            "blue": 0.7,
                        },
                    },
                },
                "fields": "userEnteredFormat(backgroundColor)",
            }
        }

        body.get("requests").append(range)
    spreadsheet = service.batchUpdate(spreadsheetId=table_id, body=body).execute()

def main():
    for item in query:
        #start_time = time.time()
        write_sheet(item)
        #print("--- %s seconds ---" % (time.time() - start_time))

if "__main__" == __name__:
    main()
