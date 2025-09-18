# EECS 581 Minesweeper Project

A classic Minesweeper game implementation using Python and Pygame.

## Features

- 10x10 grid with customizable mine count (10-20 mines)
- Left-click to reveal cells, right-click to flag
- First click is always safe (grid regenerates if needed)
- HUD with remaining flag count and game status
- Retry and quit buttons

## Requirements

- Python 3.x
- Pygame

## Installation

Install Pygame:

```bash
pip install pygame
```

## Running the Game

```bash
python main.py
```

## How to Play

1. Select the number of mines (10-20) from the main menu
2. Click "Start Game" to begin
3. Left-click to reveal cells
4. Right-click to place/remove flags
5. Win by revealing all non-mine cells
6. Use retry button to restart or quit to return to menu

## Project Structure

- `main.py` - Main game loop and state management
- `Minesweeper.py` - Core game logic and rendering
- `main_menu.py` - Main menu interface
- `BoardGenerator.py` - Mine placement and numbering logic
- `grid.py` - Individual cell management
- `gamestate_manager.py` - Game state transitions
- `Sprites/` - Game graphics and icons

## Project Board

https://docs.google.com/spreadsheets/d/1rNYyRiaY8A9GMTUM2Clc8Q7ZwGMd4fgtmcrUFs2kyS0/edit?gid=0#gid=0
