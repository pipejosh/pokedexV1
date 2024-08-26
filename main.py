import requests
import csv
from inflect import *
import re
from pyfiglet import figlet_format
from tabulate import tabulate
from sys import exit


class Pokedex():

    def __init__(self, pokemonId):

        
         
        self.pokemonID = pokemonId
        self.pokemonInfo = self.getPokemonInfo()

        # Pokemon characteristics

        self.pokemonId = self.pokemonInfo['id']
        self.pokemonName = self.pokemonInfo['name'].capitalize()
        self.pokemonHeight = f'{self.pokemonInfo['height'] * 10} cm'
        self.pokemonWeight = f'{int(self.pokemonInfo['weight'] // 10)} kg'

        # self.pokemonTypes

        types = [t['type']['name'].capitalize() for t in self.pokemonInfo['types']]
        self.pokemonTypes = ' / '.join(types)

        # self.pokemonTypes

        # self.pokemonAbilities
        
        abilities = [a['ability']['name'].capitalize() for a in self.pokemonInfo['abilities']]
        self.pokemonAbilities = ' / '.join(abilities)

        self.pokemonWeaknesses = self.getPokemonWeaknesses()
        self.pokemonImage = self.pokemonInfo['sprites']['front_default']
        self.pokemonGeneration = self.getPokemonGeneration()

        # self.pokemonAbilities

        # Pokemon characteristics

    def getPokemonWeaknesses(self):
        weaknesses = set()
        for typeInfo in self.pokemonInfo['types']:
            typeUrl = typeInfo['type']['url']
            typeData = requests.get(typeUrl).json()  
            for weakness in typeData['damage_relations']['double_damage_from']:
                weaknesses.add(weakness['name'].capitalize())
        return ', '.join(weaknesses)
    
    def getPokemonGeneration(self):

        # Asignar rangos de ID a generaciones

        if 1 <= self.pokemonId <= 151:
            return 'Generation I'
        elif 152 <= self.pokemonId <= 251:
            return 'Generation II'
        elif 252 <= self.pokemonId <= 386:
            return 'Generation III'
        elif 387 <= self.pokemonId <= 493:
            return 'Generation IV'
        elif 494 <= self.pokemonId <= 649:
            return 'Generation V'
        elif 650 <= self.pokemonId <= 721:
            return 'Generation VI'
        elif 722 <= self.pokemonId <= 809:
            return 'Generation VII'
        elif 810 <= self.pokemonId <= 898:
            return 'Generation VIII'
        elif 899 <= self.pokemonId <= 1010:
            return 'Generation IX'
        else:
            return 'Unknown Generation'

    def getPokemonInfo(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemonID}'
        pokemonInfo = requests.get(url)
        
        if pokemonInfo.status_code == 200:
            return pokemonInfo.json()
        elif pokemonInfo.status_code == 404:
            raise ValueError('Pokemon not found')
        else:
            raise Exception(f"Error fetching data: {pokemonInfo.status_code}")
        
    def __str__(self):

        return f'''
        ID: {self.pokemonId}\n
        Generation: {self.pokemonGeneration}\n
        Name: {self.pokemonName}\n
        Height: {self.pokemonHeight}\n
        Weight: {self.pokemonWeight}\n
        Type: {self.pokemonTypes}\n
        Abilities: {self.pokemonAbilities}\n
        Weaknesses: {self.pokemonWeaknesses}\n
        Image: {self.pokemonImage}
        '''
        
    @staticmethod
    def getPokemonId():

        while True:
        
            try:    
            
                pokemonId = int(input('Enter the pokemon ID: '))


                return Pokedex(pokemonId)

            except ValueError:

                print('\nPokemon does not exist\n')
                
                
            
        

def main(): 

    userOption = userInterface()

    if userOption == 1:

        quickSearch()

    elif userOption == 2:

        addFavoritePokemons()

    elif userOption == 3:

        importFavoritePokemons()

    else:

        exit('Thanks for using Pokedex V1')


def userInterface():

    title = figlet_format('Pokedex  V 1', font = 'slant')

    print(title)

    name = input('Please enter your name: ')

    print(f'\nHello {name} thanks for using Pokedex V1\n')

    tableInfo = [['1', 'Quick search'],
                 ['2', 'Add favorite Pokemons'],
                 ['3', 'Import Favorite Pokemons'],
                 ['4', 'Exit Pokedex']]
    
    head = ['#','Option']
    
    print(tabulate(tableInfo, headers = head))
    print()

    option = input('Enter a valid option: ')

    while option not in ['1','2','3','4']:

        option = input('Please enter a valid option: ')    

    return int(option)

def quickSearch():

    global pokedex

    print()

    pokedex = Pokedex.getPokemonId()

    print(f'\n{pokedex}')

def addFavoritePokemons():

    favoritePokemons = []

    exitPorgram = True

    while exitPorgram:

        print(pokedex)

def importFavoritePokemons():

    pass

if __name__ == '__main__':
     
     main()
        


