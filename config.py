class john:
    # Dit zijn de gegevens die de bot kan invullen in het winactie-formulier
    VOORNAAM = 'John'
    ACHTERNAAM = 'Doe'
    EMAIL = 'john_{}@example.com'  # Voeg ergens {} toe om daar elk spel een willekeurig nummer te plaatsen
    KETEN_ID = 0  # Plek in lijst van winkels, tellen begint bij 0! Dus de 1ste winkel is 0, de 2e is 1, enz.
    PLAATSNAAM = 'Amsterdam'
    WINKELNAAM = 'Stadhuis'


class config:
    PERSON = john  # Moet bevatten: VOORNAAM, ACHTERNAAM. EMAIL, KETEN_ID, PLAATSNAAM, WINKELNAAM
    URL: str = 'https://nixchallenge.nl/'  # Zet hier bijv. https://nixchallenge.nl/ of je finale-link
    GAMES_TO_PLAY: int = 1

    AUTO_CLICK: bool = True  # Speel het spel helemaal zelf, anders geeft de bot hints welk antwoord je zelf moet aanklikken
    AUTO_FINAL: bool = False  # Probeer de finale automatisch te spelen (experimenteel)

    KEEP_OPEN: bool = True  # Houd de browser van elk spel open

    DOWNLOAD: bool = True  # Download de foto's van nieuwe gezichten naar de map 'persons'

    FILL_FORM: bool = False  # Vul het winactie-formulier automatisch in met de gegevens van PERSON
    SEND_FORM: bool = False  # Verzend het formulier automatisch


class color:
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'
    bold = '\033[1m'
    end = '\033[0m'
