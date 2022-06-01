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

from config import config, color


def main():
    if config.DOWNLOAD:
        try:
            os.mkdir('persons/')
        except:
            pass
    for _ in range(config.GAMES_TO_PLAY):  # How many times to play a full game
        try:
            with open('faces.pkl', 'rb') as file:
                names = pickle.load(file)
            print(f'Faces seen: {len(names)}')
        except:
            names = {}
            print('KAN faces.pkl NIET IMPORTEREN')

        chrome_options = Options()
        if config.KEEP_OPEN:
            chrome_options.add_experimental_option("detach", True)
        browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        browser.get(config.URL)

        time.sleep(2)

        # 3 explanation pages to confirm, 2 in final
        if config.AUTO_CLICK:
            for i in range(2 if config.AUTO_FINAL else 3):
                start_btns = browser.find_elements(by=By.CLASS_NAME, value='button-wrapper')
                if len(start_btns) >= 2:
                    start_btns[1].click()
                else:
                    start_btns[0].click()
        else:
            print(f'{color.yellow}\nHANDMATIGE MODUS{color.end}')
            input('Druk hier op [enter] zodra spel is begonnen...')
            print()  # \n

        # Play game
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
                    raise Exception('KAN KNOPPEN NIET VINDEN')

            try:
                ask = names[img.replace("assets/img/persons/", "")]
            except:
                # Not seen before
                if config.AUTO_CLICK:
                    id_btns[1].click()
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

        time.sleep(3)

        print(f'Faces seen: {len(names)}')
        with open('faces.pkl', 'wb') as file:
            pickle.dump(names, file)

        if not config.AUTO_CLICK:
            continue

        # Secretary message
        start_btns = browser.find_elements(by=By.CLASS_NAME, value='button-wrapper')
        start_btns[0].click()

        if config.FILL_FORM:
            # Left-most button: 'winactie'
            start_btns = browser.find_elements(by=By.CLASS_NAME, value='button-wrapper')
            start_btns[0].click()

            # Form
            try:
                field = browser.find_element(by=By.XPATH,
                                             value="//input[@formcontrolname='first_name']")
            except:
                continue
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


if __name__ == '__main__':
    main()
