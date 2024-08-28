from unittest.mock import patch, mock_open
import project


@patch('builtins.input', side_effect=['1']) 

@patch('project.Pokedex.getPokemonId')  

def test_quickSearch(mock_getPokemonId, mock_input):

    mock_getPokemonId.return_value = project.Pokedex('pikachu')
    
    project.quickSearch()
    
    mock_getPokemonId.assert_called_once()


@patch('builtins.input', side_effect=['pikachu', 'n'])  

@patch('builtins.open', new_callable=mock_open)  

@patch('project.EncryptDecrypt.encryptMessage')  

@patch('project.Pokedex.getPokemonId')  

def test_addFavoritePokemons(mock_getPokemonId, mock_encryptMessage, mock_open, mock_input):

    mock_getPokemonId.return_value = project.Pokedex('pikachu')
    
    mock_encryptMessage.side_effect = lambda x: x[::-1]
    
    project.addFavoritePokemons()
    
    mock_getPokemonId.assert_called_once()
    
    mock_open.assert_called_once()
    
    mock_encryptMessage.assert_any_call("1: Pikachu\n")

@patch('builtins.input', side_effect=['testfile.txt'])  

@patch('builtins.open', new_callable=mock_open, read_data='626b757361206e616d657320506f6b656d6f6e\n31:20656c70696b\n')

@patch('project.EncryptDecrypt.decryptMessage')  

def test_importFavoritePokemons(mock_decryptMessage, mock_open, mock_input):

    mock_decryptMessage.side_effect = lambda x: x[::-1]  
    
    favorites = project.importFavoritePokemons()
    
    mock_open.assert_called_once_with('testfile.txt')

    mock_decryptMessage.assert_any_call('626b757361206e616d657320506f6b656d6f6e')
    
    assert favorites == [['1', 'Pikachu']]
