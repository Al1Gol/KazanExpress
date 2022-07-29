# KazanExpress
Парсинг сайта KazanExpress https://kazanexpress.ru/

Установка необходимых пакетов из директории проекта:
pip install -r requirements.txt

Проверить версию бразуера Google Chrome:
Если версия Google Chrome отличается от "вер. 102.0.5005.61", то:
- либо скачать версию бразуера "вер. 102.0.5005.61";
- либо скачать с сайта https://chromedriver.chromium.org/downloads версию chromedriver,
сооветсвующую версии вашего бразера и распаковать ее в папку "./chromedriver/", расположенную
в корне проекта.

Запуск скрипта из директории проекта:
python run.py

Ссылка на таблицу в Google Sheets:
https://docs.google.com/spreadsheets/d/1KJBarCH76G2EyCPH7x6XyH2HK5QNfgKnkRerX73RFAM

Изменения и добавление нового запроса:
В файле config.py изменить значение переменной query. Каждый текст запроса должен быть выделен кавычками и находиться внутри 
квадратных скобок.