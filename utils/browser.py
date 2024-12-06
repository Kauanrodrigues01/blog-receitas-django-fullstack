from pathlib import Path
from selenium import webdriver
from decouple import config

ROOT_DIR = Path(__file__).parent.parent
CHROMEDRIVER_NAME = 'chromedriver.exe'
CHROMEDRIVER_DIR = ROOT_DIR / 'bin' / CHROMEDRIVER_NAME

def make_chrome_browser(*options):
    chrome_options = webdriver.ChromeOptions()
    
    if options is not None:
        for option in options:
            chrome_options.add_argument(option)
            
    if config('SELENIUM_HEADLESS', cast=bool):
        chrome_options.add_argument('--headless')
    
    chrome_service = webdriver.ChromeService(executable_path=CHROMEDRIVER_DIR)
    browser = webdriver.Chrome(options=chrome_options, service=chrome_service)
    return browser

if __name__ == '__main__':
    browser = make_chrome_browser()
    browser.get('http://www.udemy.com/')
    input('Precione qualquer tecla para sair do navegador')
    browser.quit()