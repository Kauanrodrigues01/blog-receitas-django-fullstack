from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from decouple import config

ROOT_PATH = Path(__file__).parent.parent
CHROMEDRIVER_NAME = 'chromedriver.exe'
CHROMEDRIVER_PATH = ROOT_PATH / 'bin' / CHROMEDRIVER_NAME

def make_chrome_browser(*options):
    chrome_options = webdriver.ChromeOptions()
    if options is not None:
        for option in options:
            try:
                chrome_options.add_argument(option)
            except:
                print(f'Não foi possivel adicionar a opção: {option} para o chrome')
                
    if config('SELENIUM_HEADLESS') == '1':
        chrome_options.add_argument('--headless')
        
    chrome_service = Service(executable_path=CHROMEDRIVER_PATH)
    browser = webdriver.Chrome(service=chrome_service, options=chrome_options)
    return browser

if __name__ == '__main__':
    browser = make_chrome_browser('--headless')
    browser.get('http://www.udemy.com.br/')
    input("Pressione Enter para fechar o navegador...")
    browser.quit()