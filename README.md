# Murder_Mystery_AI
## Overview
This project is a Python-based murder mystery game built using Pygame. The player must investigate the murder by interacting with characters, collecting clues, and making deductions to identify the murderer. The game includes a menu system, an interactive game screen, buttons for interaction, and an API integration for making in-game calls.
## File Structure
### `menu.py`
Handles the game’s main menu, allowing players to start the game or access settings.
#### Classes:
- `Menu`: Manages the menu screen and button interactions.
#### Features:
- Displays the game title and background.
- Provides buttons to start the game and open settings.
- Uses the `Button` class for UI interactions.
#### Example:
```python
class Menu:
    def __init__(self, screen, start_game, open_settings):
        self.screen = screen
        self.bg_image = pygame.image.load("assets/menu_background.jpg")
        self.bg_image = pygame.transform.scale(self.bg_image, self.screen.get_size())
```
---
### `game.py`
Contains the core gameplay logic, including character interactions and detective work.
#### Classes:
- `Game`: Manages game state, character interactions, and evidence collection.
#### Features:
- Assigns roles randomly (murderer, victim, witnesses, etc.).
- Loads backgrounds and character sprites.
- Uses an API to simulate in-game phone calls.
- Displays alibis and allows accusations.
#### Example:
```python
self.murderer_list = ['father', 'mother', 'son', 'neighbour', 'grandfather', 'cook']
self.dead_person_list = [p for p in self.murderer_list if p != self.murderer]
self.murder_weapon_list = ['knife', 'strangulation', 'poison', 'bat', 'pan']
```
---
### `button.py`
Defines a generic button class used throughout the game.
#### Classes:
- `Button`: Represents an interactive UI button.
#### Features:
- Detects hover and click interactions.
- Changes color on hover.
- Calls an assigned function when clicked.
#### Example:
```python
class Button:
    def __init__(self, x, y, width, height, text, font, color, hover_color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.base_color = color
```
---
### `API.py`
Handles API communication to simulate phone calls within the game.
#### Classes:
- `APIWrapper`: Manages API interactions for in-game phone calls.
#### Features:
- Sends API requests to initiate phone calls.
- Checks call status via an external API.
- Passes alibi data and murder details for immersive dialogues.
- **Note:** The API key has been removed for privacy reasons.
#### Example:
```python
class APIWrapper():
    def __init__(self, phone_num, alibi_data):
        self.headers = {
            'authorization': 'REMOVED_FOR_PRIVACY',
            "Content-Type": "application/json"
        }
```
---
## How to Run
1. Ensure Python and Pygame are installed:
   ```sh
   pip install pygame
   ```
2. Start the game:
   ```sh
   python menu.py
   ```
## Dependencies
- `pygame`: For graphics and UI.
- `requests`: For API interactions.
## Future Improvements
- Add more animations and interactions.
- Enhance AI for deeper character interactions.
- Implement a scoring system.
- Expand API capabilities for realistic phone interactions.
## More side information
Our team of 4 had 5 days from monday to finish and present this wonderful idea! On day one it was idea generation. We ended up settling on the Murder Mystery. On Tuesday we all had taken different our own suspect and worked on scripting. We spent Tuesday scripting the suspsects and were later altered, but sufficed for testing. On wednseday we had produced the original scripting and a basic API framwork. To which on thursday the basic GUI was developed and we had spent just over 7 hours developing and re-working the scripts to make them more dynamic so every time a user played it would be a different experience. Some of us stayed up late to re-work the API_module and experiment a bit further with the API. At 9AM on the Friday we met up before the presentation to make any finishing touches. At 1PM we had our presentation, that went to shambles, we didn't actually plan how we would present. But, at the end of the day we got the 'Most Technical', which is an absolute win!
