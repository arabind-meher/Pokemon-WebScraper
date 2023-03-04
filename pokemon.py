import logging
from os.path import join

from pandas import DataFrame
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

logging.basicConfig(
    filename='logs/pokemon.log',
    filemode='w',
    format='%(asctime)s - %(message)s',
    level=logging.INFO
)


class Pokemon:
    index = '/html/body/main/div[2]/div[2]/div/div[1]/div[2]/table/tbody/tr[1]/td/strong'
    name = '/html/body/main/h1'
    types = '/html/body/main/div[2]/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td'
    species = '/html/body/main/div[2]/div[2]/div/div[1]/div[2]/table/tbody/tr[3]/td'
    height = '/html/body/main/div[2]/div[2]/div/div[1]/div[2]/table/tbody/tr[4]/td'
    weight = '/html/body/main/div[2]/div[2]/div/div[1]/div[2]/table/tbody/tr[5]/td'
    ability = '/html/body/main/div[2]/div[2]/div/div[1]/div[2]/table/tbody/tr[6]/td'
    hp = '/html/body/main/div[2]/div[2]/div/div[2]/div[1]/div[2]/table/tbody/tr[1]/td[1]'
    attack = '/html/body/main/div[2]/div[2]/div/div[2]/div[1]/div[2]/table/tbody/tr[2]/td[1]'
    defence = '/html/body/main/div[2]/div[2]/div/div[2]/div[1]/div[2]/table/tbody/tr[3]/td[1]'
    sp_attack = '/html/body/main/div[2]/div[2]/div/div[2]/div[1]/div[2]/table/tbody/tr[4]/td[1]'
    sp_defence = '/html/body/main/div[2]/div[2]/div/div[2]/div[1]/div[2]/table/tbody/tr[5]/td[1]'
    speed = '/html/body/main/div[2]/div[2]/div/div[2]/div[1]/div[2]/table/tbody/tr[6]/td[1]'
    total = '/html/body/main/div[2]/div[2]/div/div[2]/div[1]/div[2]/table/tfoot/tr/td'
    generation = '/html/body/main/p'

    def __init__(self):
        logging.info('START')

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito")
        self.browser = webdriver.Chrome(join('driver', 'chromedriver.exe'), chrome_options=chrome_options)
        self.get_pokemon_data()

        logging.info('END')

    def get_pokemon_data(self):
        url = 'https://pokemondb.net/pokedex/bulbasaur'
        self.browser.get('https://pokemondb.net/pokedex/bulbasaur')

        pokemon_dict = dict()
        while True:
            pokemon_dict[self.browser.find_element(By.XPATH, self.index).text.strip()] = self.scrape_data(self.browser)

            try:
                self.browser.find_element(By.CLASS_NAME, 'entity-nav-next').click()
            except NoSuchElementException:
                break

        path = 'data/pokemon.csv'
        DataFrame(pokemon_dict.values()).to_csv(path, index=False)
        logging.info(f'CSV file created at "{path}"')

    def scrape_data(self, driver):
        pokemon_data = dict()

        pokemon_data['Index'] = int(driver.find_element(By.XPATH, self.index).text.strip())
        pokemon_data['Name'] = driver.find_element(By.XPATH, self.name).text.strip().title()

        logging.info(f"{'%04d' % pokemon_data['Index']}: {pokemon_data['Name']}")

        types = driver.find_element(By.XPATH, self.types).text.strip().title().split()
        if len(types) == 1:
            pokemon_data['Type 1'] = types[0]
            pokemon_data['Type 2'] = None
        else:
            pokemon_data['Type 1'] = types[0]
            pokemon_data['Type 2'] = types[1]
        del types

        pokemon_data['Species'] = driver.find_element(By.XPATH, self.species).text.strip().title()
        pokemon_data['Height'] = float(driver.find_element(By.XPATH, self.height).text.strip().split('m')[0].strip())
        pokemon_data['Weight'] = float(driver.find_element(By.XPATH, self.weight).text.strip().split('kg')[0].strip())

        ability = driver.find_element(By.XPATH, self.ability).text.strip().split('\n')
        if len(ability) == 1:
            pokemon_data['Ability 1'] = ability[0].split()[-1]
            pokemon_data['Ability 2'] = None
            pokemon_data['Ability H'] = None
        elif len(ability) == 2:
            pokemon_data['Ability 1'] = ability[0].split()[-1]
            pokemon_data['Ability 2'] = None
            pokemon_data['Ability H'] = ability[1].split()[0]
        else:
            pokemon_data['Ability 1'] = ability[0].split()[-1]
            pokemon_data['Ability 2'] = ability[1].split()[-1]
            pokemon_data['Ability H'] = ability[2].split()[0]
        del ability

        pokemon_data['HP'] = int(driver.find_element(By.XPATH, self.hp).text.strip())
        pokemon_data['Attack'] = int(driver.find_element(By.XPATH, self.attack).text.strip())
        pokemon_data['Defence'] = int(driver.find_element(By.XPATH, self.defence).text.strip())
        pokemon_data['Sp_Attack'] = int(driver.find_element(By.XPATH, self.sp_attack).text.strip())
        pokemon_data['Sp_Defence'] = int(driver.find_element(By.XPATH, self.sp_defence).text.strip())
        pokemon_data['Speed'] = int(driver.find_element(By.XPATH, self.speed).text.strip())
        pokemon_data['Total'] = int(driver.find_element(By.XPATH, self.total).text.strip())
        
        generation = driver.find_element(By.XPATH, self.generation).text.strip()
        pokemon_data['Generation'] = f"Gen {generation.split('Generation')[1].split('.')[0].strip()}"
        del generation

        return pokemon_data


if __name__ == '__main__':
    Pokemon()
