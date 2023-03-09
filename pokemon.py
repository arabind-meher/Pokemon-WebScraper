import logging
from os import mkdir
from os.path import join, exists

from pandas import DataFrame
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from database import Base, session, engine
from model import PokemonDB

logging.basicConfig(
    filename='logs/pokemon.log',
    filemode='w',
    format='%(asctime)s - %(message)s',
    level=logging.INFO
)


class Pokemon:
    def __init__(self):
        logging.info('START')

        if not exists('data'):
            mkdir('data')

        if not exists('logs'):
            mkdir('logs')

        self.initialize_db()
        logging.info('DATABASE CREATED')

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito")
        self.browser = webdriver.Chrome(join('driver', 'chromedriver.exe'), chrome_options=chrome_options)
        self.db = session()

        self.get_pokemon_data()

        self.db.close()
        self.browser.close()

        logging.info('END')

    @staticmethod
    def initialize_db():
        Base.metadata.create_all(engine)

    def get_pokemon_data(self):
        self.browser.get('https://pokemondb.net/pokedex/bulbasaur')

        pokemon_dict = dict()
        iterator = 0

        while True:
            tabs = self.browser.find_element(
                By.CLASS_NAME, 'sv-tabs-tab-list'
            ).find_elements(
                By.CLASS_NAME, 'sv-tabs-tab'
            )

            if len(tabs) == 1:
                poke_data = self.scrape_data(self.browser, self.get_xpath(1))
                pokemon_dict[iterator] = poke_data
                self.upload_data(poke_data)
            else:
                for i, tab in enumerate(tabs, 1):
                    tab.click()
                    poke_data = self.scrape_data(tab, self.get_xpath(i), tab)
                    pokemon_dict[iterator] = poke_data
                    self.upload_data(poke_data)

                    iterator += 1

            try:
                self.browser.find_element(By.CLASS_NAME, 'entity-nav-next').click()
                iterator += 1
            except NoSuchElementException:
                break

        path = join('data', 'pokemon.xlsx')
        DataFrame(pokemon_dict.values()).to_excel(path, sheet_name='pokemon', index=False)
        logging.info(f'Excel file created at "{path}"')

    def upload_data(self, poke_data):
        pokemon = PokemonDB()
        pokemon.index = poke_data['Index']
        pokemon.name = poke_data['Name']
        pokemon.form = poke_data['Form']
        pokemon.type_1 = poke_data['Type 1']
        pokemon.type_2 = poke_data['Type 2']
        pokemon.species = poke_data['Species']
        pokemon.height = poke_data['Height']
        pokemon.weight = poke_data['Weight']
        pokemon.ability_1 = poke_data['Ability 1']
        pokemon.ability_2 = poke_data['Ability 2']
        pokemon.ability_h = poke_data['Ability H']
        pokemon.hp = poke_data['HP']
        pokemon.attack = poke_data['Attack']
        pokemon.defence = poke_data['Defence']
        pokemon.sp_attack = poke_data['Sp_Attack']
        pokemon.sp_defence = poke_data['Sp_Defence']
        pokemon.speed = poke_data['Speed']
        pokemon.total = poke_data['Total']

        self.db.add(pokemon)
        self.db.commit()

    @staticmethod
    def scrape_data(driver, xpath, tab=None):
        pokemon_data = dict()

        pokemon_data['Index'] = int(driver.find_element(By.XPATH, xpath['index']).text.strip())
        pokemon_data['Name'] = driver.find_element(By.XPATH, xpath['name']).text.strip().title()

        if tab and pokemon_data['Name'] != tab.text.strip():
            pokemon_data['Form'] = tab.text.strip()
        else:
            pokemon_data['Form'] = None

        if pokemon_data['Form']:
            logging.info(f"{'%04d' % pokemon_data['Index']}: {'%15s' % pokemon_data['Name']} = {pokemon_data['Form']}")
        else:
            logging.info(f"{'%04d' % pokemon_data['Index']}: {'%15s' % pokemon_data['Name']} = {pokemon_data['Name']}")

        types = driver.find_element(By.XPATH, xpath['types']).text.strip().title().split()
        if len(types) == 1:
            pokemon_data['Type 1'] = types[0]
            pokemon_data['Type 2'] = None
        else:
            pokemon_data['Type 1'] = types[0]
            pokemon_data['Type 2'] = types[1]
        del types

        pokemon_data['Species'] = driver.find_element(By.XPATH, xpath['species']).text.strip().title()

        try:
            pokemon_data['Height'] = float(driver.find_element(
                By.XPATH, xpath['height']
            ).text.strip().split('m')[0].strip())
        except ValueError:
            pokemon_data['Height'] = None

        try:
            pokemon_data['Weight'] = float(driver.find_element(
                By.XPATH, xpath['weight']
            ).text.strip().split('kg')[0].strip())
        except ValueError:
            pokemon_data['Weight'] = None

        ability = driver.find_element(By.XPATH, xpath['ability']).text.strip().split('\n')
        if ability[0] == '—':
            pokemon_data['Ability 1'] = None
            pokemon_data['Ability 2'] = None
            pokemon_data['Ability H'] = None
        elif len(ability) == 1:
            pokemon_data['Ability 1'] = ability[0].split('.')[-1].strip()
            pokemon_data['Ability 2'] = None
            pokemon_data['Ability H'] = None
        elif len(ability) == 2:
            pokemon_data['Ability 1'] = ability[0].split('.')[-1].strip()
            pokemon_data['Ability 2'] = None
            pokemon_data['Ability H'] = ability[1].split('(')[0].strip()
        else:
            pokemon_data['Ability 1'] = ability[0].split('.')[-1].strip()
            pokemon_data['Ability 2'] = ability[1].split('.')[-1].strip()
            pokemon_data['Ability H'] = ability[2].split('(')[0].strip()
        del ability

        pokemon_data['HP'] = int(driver.find_element(By.XPATH, xpath['hp']).text.strip())
        pokemon_data['Attack'] = int(driver.find_element(By.XPATH, xpath['attack']).text.strip())
        pokemon_data['Defence'] = int(driver.find_element(By.XPATH, xpath['defence']).text.strip())
        pokemon_data['Sp_Attack'] = int(driver.find_element(By.XPATH, xpath['sp_attack']).text.strip())
        pokemon_data['Sp_Defence'] = int(driver.find_element(By.XPATH, xpath['sp_defence']).text.strip())
        pokemon_data['Speed'] = int(driver.find_element(By.XPATH, xpath['speed']).text.strip())
        pokemon_data['Total'] = int(driver.find_element(By.XPATH, xpath['total']).text.strip())

        return pokemon_data

    @staticmethod
    def get_xpath(itr):
        xpath = dict()
        xpath['index'] = f'/html/body/main/div[2]/div[2]/div[{itr}]/div[1]/div[2]/table/tbody/tr[1]/td/strong'
        xpath['name'] = '/html/body/main/h1'
        xpath['types'] = f'/html/body/main/div[2]/div[2]/div[{itr}]/div[1]/div[2]/table/tbody/tr[2]/td'
        xpath['species'] = f'/html/body/main/div[2]/div[2]/div[{itr}]/div[1]/div[2]/table/tbody/tr[3]/td'
        xpath['height'] = f'/html/body/main/div[2]/div[2]/div[{itr}]/div[1]/div[2]/table/tbody/tr[4]/td'
        xpath['weight'] = f'/html/body/main/div[2]/div[2]/div[{itr}]/div[1]/div[2]/table/tbody/tr[5]/td'
        xpath['ability'] = f'//html/body/main/div[2]/div[2]/div[{itr}]/div[1]/div[2]/table/tbody/tr[6]/td'
        xpath['hp'] = f'/html/body/main/div[2]/div[2]/div[{itr}]/div[2]/div[1]/div[2]/table/tbody/tr[1]/td[1]'
        xpath['attack'] = f'/html/body/main/div[2]/div[2]/div[{itr}]/div[2]/div[1]/div[2]/table/tbody/tr[2]/td[1]'
        xpath['defence'] = f'/html/body/main/div[2]/div[2]/div[{itr}]/div[2]/div[1]/div[2]/table/tbody/tr[3]/td[1]'
        xpath['sp_attack'] = f'/html/body/main/div[2]/div[2]/div[{itr}]/div[2]/div[1]/div[2]/table/tbody/tr[4]/td[1]'
        xpath['sp_defence'] = f'/html/body/main/div[2]/div[2]/div[{itr}]/div[2]/div[1]/div[2]/table/tbody/tr[5]/td[1]'
        xpath['speed'] = f'/html/body/main/div[2]/div[2]/div[{itr}]/div[2]/div[1]/div[2]/table/tbody/tr[6]/td[1]'
        xpath['total'] = f'/html/body/main/div[2]/div[2]/div[{itr}]/div[2]/div[1]/div[2]/table/tfoot/tr/td'

        return xpath


if __name__ == '__main__':
    Pokemon()
