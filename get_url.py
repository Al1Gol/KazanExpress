import json
from selenium import webdriver

url = 'https://kazanexpress.ru/search?query=%D0%B8%D0%B3%D1%80%D1%83%D1%88%D0%BA%D0%B8'
driver = webdriver.Chrome('D:\\chromedriver\\chromedriver.exe')
driver.maximize_window()

try:
    driver.get(url=url)
    content = driver.page_source
    driver.find_element_by_css_selector('')
    with open ('index.html', 'w', encoding='utf-8') as file:
        json.dump(content, file, indent=4, ensure_ascii=False)
    
except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()
  