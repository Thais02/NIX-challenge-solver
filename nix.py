import pickle
import time
import random
import urllib
import os

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

try:
    from config import config, color
except:
    raise FileNotFoundError('config.py ontbreekt in deze map, kan script niet uitvoeren')


def load_faces():
    """
    Load faces.pkl from local storage, otherwise initialize new empty dictionary

    :return: Dictionary of known filenames as {str, bool} with bool = id_vragen?
    """
    try:
        with open('faces.pkl', 'rb') as file:
            names = pickle.load(file)
        print(f'Bekende gezichten: {len(names)}')
    except:
        names = {}
        print(f'\n{color.red}Kan faces.pkl niet importeren, ik begin opnieuw met trainen...{color.end}')
    return names


def initialize_browser():
    """
    Initialize new Chrome browser with appropriate options.\n
    Browser will HTTP(S) GET config.URL

    :return: WebDriver-object
    """
    chrome_options = Options()
    # os.environ['WDM_LOG_LEVEL'] = '0'  # Suppresses ALL WebDriver output
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    if config.KEEP_OPEN:
        chrome_options.add_experimental_option("detach", True)
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    browser.get(config.URL)
    return browser


def skip_info_pages(browser):
    """
    Either skips the information pages automatically or waits for the user to do it.\n
    Auto skips 2 pages in config.FINAL mode else 3 pages

    :param browser: WebDriver-object
    """
    if config.AUTO_START:
        # 3 explanation pages to confirm, 2 in final
        for i in range(2 if config.AUTO_START_FINAL else 3):
            start_btns = browser.find_elements(by=By.CLASS_NAME, value='button-wrapper')
            if len(start_btns) >= 2:
                start_btns[1].click()
            else:
                start_btns[0].click()
    else:
        print(f'\n{color.yellow}Je moet het spel zelf starten')
        if config.AUTO_CLICK:
            print(f'Daarna neem ik het over{color.end}')
        else:
            print(f'Daarna geef ik je hints wat het juiste antwoord is{color.end}')
        id_btns = []
        while len(id_btns) < 2:
            id_btns = browser.find_elements(by=By.CLASS_NAME, value='round-button-wrapper')


def play(browser, names):
    """
    Plays the main game.\n
    Either automatically clicks the correct option, guesses and store the correct result or instructs the user.\n
    Keeps going until no image is detected on screen anymore

    :param browser: WebDriver-object
    :param dict names: Dictionary of known filenames and boolean id_vragen?
    :raise Exception: If the correct buttons cannot be found on screen
    """
    prev_img = ''
    index = 0
    while True:
        img = 'assets/img/preloader.gif'
        background_final = True
        while img == 'assets/img/preloader.gif' or background_final:
            html = browser.page_source
            soup = BeautifulSoup(html, features='html.parser')
            try:
                img = soup.find('img', attrs={'class': 'mat-card-image'}, recursive=True).get('src')
            except:
                img = 'assets/img/preloader.gif'
                try:
                    id_btns = browser.find_elements(by=By.CLASS_NAME, value='round-button-wrapper')
                except:
                    break
            try:
                background = soup.find('div',
                                       attrs={'fxlayout': 'column',
                                              'fxlayoutalign': 'space-between none',
                                              'fxlayoutalign.gt-sm': 'center none'},
                                       recursive=True)
                background_final = 'bg-correct' in background.get('class') or 'bg-incorrect' in background.get(
                    'class')
            except:
                background_final = False

        if 'assets/img/persons/' not in img:  # Game is finished
            break

        if img == prev_img:
            continue

        index += 1

        try:
            id_btns = browser.find_elements(by=By.CLASS_NAME, value='round-button-wrapper')
        except:
            if config.AUTO_CLICK:
                raise Exception(f'\n{color.red}ERROR: kan knoppen niet vinden{color.end}')

        try:
            ask = names[img.replace("assets/img/persons/", "")]
        except:
            # Not seen before
            if config.AUTO_CLICK:
                id_btns[1].click()  # Always guess 'wel vragen' if correct answer is unknown
                time.sleep(1)
            else:
                print(f'{index}: {color.yellow}NIEUW GEZICHT{color.end}')
                if config.DOWNLOAD:
                    try:
                        urllib.request.urlretrieve(f'https://nixchallenge.nl/{img}',
                                                   f'persons\\{index}__{img.replace("assets/img/persons/", "")}')
                    except:
                        try:
                            urllib.request.urlretrieve(f'https://finale.nixchallenge.nl/{img}',
                                                       f'persons\\{index}__{img.replace("assets/img/persons/", "")}')
                        except:
                            pass
                prev_img = img
                continue
            html = browser.page_source
            soup = BeautifulSoup(html, features='html.parser')
            background = soup.find('div',
                                   attrs={'fxlayout': 'column',
                                          'fxlayoutalign': 'space-between none',
                                          'fxlayoutalign.gt-sm': 'center none'},
                                   recursive=True)
            if config.DOWNLOAD:
                try:
                    urllib.request.urlretrieve(f'https://nixchallenge.nl/{img}',
                                               f'persons\\{index}__{img.replace("assets/img/persons/", "")}')
                except:
                    try:
                        urllib.request.urlretrieve(f'https://finale.nixchallenge.nl/{img}',
                                                   f'persons\\{index}__{img.replace("assets/img/persons/", "")}')
                    except:
                        pass
            names[img.replace("assets/img/persons/", "")] = 'bg-correct' in background.get('class')
            print(
                f'NIEUW GEZICHT: ID vragen? -> {color.green if "bg-correct" in background.get("class") else color.red}'
                f'{"bg-correct" in background.get("class")}{color.end}')
        else:
            # Already know the correct answer
            if config.AUTO_CLICK:
                id_btns[1].click() if ask else id_btns[0].click()
                time.sleep(1)
            else:
                print(f'{index}: AL GEZIEN: ID VRAGEN? -> {color.green if ask else color.red}{ask}{color.end}')
                prev_img = img
                continue


def fill_form(browser):
    """
    Tries to open and fill the form with information defined in config.PERSON

    :param browser: WebDriver-object
    :return: True on success, else False
    """
    # Left-most button: 'WINACTIE'
    start_btns = browser.find_elements(by=By.CLASS_NAME, value='button-wrapper')
    if start_btns[0].text == 'WINACTIE':
        start_btns[0].click()

        # Form
        try:
            field = browser.find_element(by=By.XPATH,
                                         value="//input[@formcontrolname='first_name']")
        except:
            print(f'\n{color.red}WINACTIE formulier niet zoals verwacht{color.end}')
            return False  # could not find form properly
        field.send_keys(config.PERSON.VOORNAAM)

        field = browser.find_element(by=By.XPATH,
                                     value="//input[@formcontrolname='last_name']")
        field.send_keys(config.PERSON.ACHTERNAAM)

        field = browser.find_element(by=By.XPATH,
                                     value="//input[@formcontrolname='email']")
        field.send_keys(config.PERSON.EMAIL.format(random.randint(100000, 999999)))

        field = browser.find_element(by=By.XPATH,
                                     value="//input[@formcontrolname='city']")
        field.send_keys(config.PERSON.PLAATSNAAM)

        field = browser.find_element(by=By.XPATH,
                                     value="//input[@formcontrolname='retail_name']")
        field.send_keys(config.PERSON.WINKELNAAM)

        field = browser.find_element(by=By.XPATH,
                                     value="//input[@type='checkbox']")
        field.send_keys(' ')
        field = browser.find_element(by=By.XPATH,
                                     value="//mat-select[@formcontrolname='retail_chain']")
        field.click()

        time.sleep(1)

        field = browser.find_element(by=By.XPATH,
                                     value=f"//mat-option[@id='mat-option-{config.PERSON.KETEN_ID}']")
        field.click()

        if config.SEND_FORM:
            start_btns = browser.find_elements(by=By.CLASS_NAME, value='button-wrapper')
            start_btns[0].click()
        return True
    else:
        print(f'\n{color.red}WINACTIE formulier niet beschikbaar{color.end}')
        return False


def main():
    """main controller"""
    if config.DOWNLOAD:
        try:
            os.mkdir('persons/')
        except:
            pass

    if not config.AUTO_CLICK:
        print(f'\n{color.yellow}HANDMATIGE MODUS{color.end}')

    names = load_faces()

    for _ in range(config.GAMES_TO_PLAY):  # How many times to play a full game
        browser = initialize_browser()

        skip_info_pages(browser)

        play(browser, names)

        # Skip secretary message
        start_btns = browser.find_elements(by=By.CLASS_NAME, value='button-wrapper')
        start_btns[0].click()

        if config.FILL_FORM:
            if not fill_form(browser):
                continue

    print(f'\nBekende gezichten: {len(names)}')
    with open('faces.pkl', 'wb') as file:
        pickle.dump(names, file)


if __name__ == '__main__':
    main()
