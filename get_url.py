import json
import time
from selenium import webdriver

def get_urls(pages_count):
    links_dict = []

    for i in range (pages_count):
        url = f'https://kazanexpress.ru/search?query=%D0%B2%D0%B8%D0%B1%D1%80%D0%B0%D1%82%D0%BE%D1%80&currentPage={i+1}'
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', options=options)
        driver.maximize_window()

        try:
            count = 0
            driver.get(url=url)
            time.sleep(1)
            elems = driver.find_elements_by_css_selector('a.tap-noselect.noselect.is-vertical')
            for elem in elems:
                count = count+1
                links_dict.append(elem.get_attribute('href'))
        except Exception as ex:
            print(ex)
        finally:
            driver.close()
            driver.quit()
    return links_dict

if "__main__" == __name__:
    result = get_urls(2)
    print(result)
    print(len(result))