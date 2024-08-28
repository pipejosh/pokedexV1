
# Imports all the necesary libraries iin orden to run the program

import requests
import base64
from pyfiglet import figlet_format
from tabulate import tabulate
from sys import exit


class Pokedex:

    # Serves for getting user input connecting with API and return all pokemon infoc 

    def __init__(self, pokemonId):

        # Contains all of the pokemon data in variables

        self.pokemonID = pokemonId
        self.pokemonInfo = self.getPokemonInfo()
        self.pokemonId = self.pokemonInfo['id']
        self.pokemonName = self.pokemonInfo['name'].capitalize()
        self.pokemonHeight = f'{self.pokemonInfo["height"] * 10} cm'
        self.pokemonWeight = f'{int(self.pokemonInfo["weight"] // 10)} kg'
        self.pokemonTypes = ' / '.join([t['type']['name'].capitalize() for t in self.pokemonInfo['types']])
        self.pokemonAbilities = ' / '.join([a['ability']['name'].capitalize() for a in self.pokemonInfo['abilities']])
        self.pokemonWeaknesses = self.getPokemonWeaknesses()
        self.pokemonImage = self.pokemonInfo['sprites']['front_default']
        self.pokemonGeneration = self.getPokemonGeneration()

    def getPokemonWeaknesses(self):

        # Calculates the pokemon weaknesses (api does not provide this info)

        weaknesses = set()
        for typeInfo in self.pokemonInfo['types']:
            typeUrl = typeInfo['type']['url']
            typeData = requests.get(typeUrl).json()  
            for weakness in typeData['damage_relations']['double_damage_from']:
                weaknesses.add(weakness['name'].capitalize())
        return ', '.join(weaknesses)
    
    def getPokemonGeneration(self):

        # Assignates the generation of the pokemon in base of the pokemon id (api does not provide this info)

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

        # Conncect to the api and return the pokemon .json info

        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemonID}'

        pokemonInfo = requests.get(url)
        
        if pokemonInfo.status_code == 200:
            return pokemonInfo.json()
        
        else:
            raise ValueError(f"Error fetching data: {pokemonInfo.status_code}")
        
    def __str__(self):

        # Returns the pokemon stats

        return (
            f'  Name: {self.pokemonName}\n'
            f'  ID: {self.pokemonId}\n'
            f'  Generation: {self.pokemonGeneration}\n'
            f'  Height: {self.pokemonHeight}\n'
            f'  Weight: {self.pokemonWeight}\n'
            f'  Type: {self.pokemonTypes}\n'
            f'  Abilities: {self.pokemonAbilities}\n'
            f'  Weaknesses: {self.pokemonWeaknesses}\n'
            f'  Image: {self.pokemonImage}'
        )
        
    @staticmethod
    def getPokemonId():

        # Get the user input and return the class with that id or pokemon name

        while True:
        
            try:    
            
                pokemonId = input('Enter the pokemon ID or name: ').lower()

                return Pokedex(pokemonId)

            except ValueError:

                print('\nPokemon does not exist\n')


class EncryptDecrypt:

    # Serves for both encrypting and decrypting messages using the library base64

    def encryptMessage(self, message):

        # Encrypts the original message

        messageEncode = message.encode('utf-8')

        encodedMessage = base64.b16encode(messageEncode)  

        return encodedMessage.decode('utf-8')  

    def decryptMessage(self, encodedMessage):

        # Decrypt the message

        decodedMessage = base64.b16decode(encodedMessage)  

        return decodedMessage.decode('utf-8') 



def main(): 

    # Main function 

    userOption = userInterface()

    userOptions = {
        1:quickSearch,
        2:addFavoritePokemons,
        3:importFavoritePokemons,
        4:viewPokemonStatistics,
        5:exitPokedex
                   }
    
    userOptions.get(userOption, exitPokedex)()

def userInterface():

    # User interface that serves for the "frontend" of this app

    title = figlet_format('Pokedex  V 1', font = 'slant')

    print(title)

    global name

    name = input('Please enter your name: ').capitalize()

    print(f'\nHello {name} thanks for using Pokedex V1\n')

    tableInfo = [['1', 'Quick search'],
                 ['2', 'Add favorite Pokemons'],
                 ['3', 'Import Favorite Pokemons'],
                 ['4', 'View pokemon statistics'],
                 ['5', 'Exit Pokedex']]
    
    head = ['#','Option']
    
    print(tabulate(tableInfo, headers = head))
    print()

    option = input('Enter a valid option: ')


    while option not in ['1','2','3','4']:

        print()

        option = input('Please enter a valid option: ')

    return int(option)

def quickSearch():

    # 1rst function serves for a quick pokemon search using the pokedex class

    print()

    pokedex = Pokedex.getPokemonId()

    print(f'\n{pokedex}')

def addFavoritePokemons():

    # 2nd function serves for adding pokemons to a certain list and exporting that file in a .txt format (encripted) 

    encryptDecrypt = EncryptDecrypt()

    favoritePokemons = []

    print("\nWelcome you'll be prompt to write your favorite pokemon ID or name")

    exitPorgram = True

    i = 0

    while exitPorgram:

        i += 1

        print()

        pokedex = Pokedex.getPokemonId()

        favoritePokemons.append([i,pokedex.pokemonName])

        print(f'\n{pokedex.pokemonName} has been added to favorites succesfully!\n')

        if input('Add another pokemon (y/n): ').strip().lower() != 'y':

            exitPorgram = False

    head = ['#', 'Name']

    print(f"\n{name}'s favorite Pokemons\n")

    print(tabulate(favoritePokemons, headers = head))

    fileName = input('\nPlease enter the file name to export your list: ')

    with open(f'{fileName}.txt' , 'w') as outputFile:

        encryptedName = encryptDecrypt.encryptMessage(f"{name}'s favorites Pokemons\n")

        outputFile.write(encryptedName + '\n')

        for list in favoritePokemons:
                
                encryptedData = encryptDecrypt.encryptMessage(f'{str(list[0])}: {list[1]}\n')
                
                outputFile.write(encryptedData + '\n')

def importFavoritePokemons():

    # 3rd function serves for importing the pokemon list from other user and the main function decrypt the encrypted list 

    decryptMessage = EncryptDecrypt()
    fileName = input('\nPlease enter your file name or path: ')

    try:

        with open(fileName) as inputFile:

            favoritePokemons = []

            userName = None  

            for line in inputFile:
                decryptedLine = decryptMessage.decryptMessage(line.strip())
              
                if not userName and 'favorites Pokemons' in decryptedLine:

                    userName = decryptedLine.split("'s favorites Pokemons")[0]

                    continue

              
                if ':' in decryptedLine:

                    num, name = decryptedLine.split(': ')

                    favoritePokemons.append([num, name.strip()])
         
            headers = ['#', 'Name']

            if userName:

                print(f"\n{userName}'s Favorite Pokemons (Imported)\n")

            else:

                print('\nFavorite Pokemons (Imported)\n')

            
            print(tabulate(favoritePokemons, headers = headers))

        return favoritePokemons
    
    except FileNotFoundError:

        print(f'\nThe file {fileName} does not exist')

        importFavoritePokemons()

def viewPokemonStatistics():

    # 4rd function serves for viewing a certain pokemon statistic in the decrypted imported list 

    favoritePokemons = importFavoritePokemons()

    if not favoritePokemons:

        print('No Pokémon data available.')

        return
    
    headers = ['#', 'Name']

    print('\nFavorite Pokémon List:\n')

    print(tabulate(favoritePokemons, headers=headers))

    try:

        option = int(input('\nEnter the number of the Pokémon you want to see the statistics for: '))

        if 1 <= option <= len(favoritePokemons):

            pokemonName = favoritePokemons[option - 1][1]

            pokedex = Pokedex(pokemonName.lower())

            print(f'\n{pokedex}')

        else:

            print('Invalid option.')

    except ValueError:

        print('Invalid input. Please enter a number.')


def exitPokedex():

    # 5th function it just exit the pokedex usin a sys.exit()

    exit('Thanks for using Pokedex V1')

if __name__ == '__main__':
     
    #  Serves for calling the main function if the file is run by a user 
     
     main()
        


