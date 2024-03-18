# Introduction
This is a Python implementation of the classic 2048 game. The game utilizes the Tkinter library for the graphical user interface.
It also implements an automatic gameplay using AI. The main game logic is implemented in Python scripts. 

# Installation
To install and run the game, follow these steps:

1. Download repository as zip
2. Unzip folder in desired location
3. Open a terminal or command prompt and navigate to the directory
4. To use the provided code, make sure you have the required libraries installed. The code relies on the following libraries:
	Tkinter: For creating the graphical user interface.
	NumPy: For numerical operations and array manipulation.
   You can install these libraries using pip, Python's package manager. Open your command line interface and run the following commands:
	pip install tk
	pip install numpy
5. Run the game script by executing the following command:
	python game.py

# Usage
Once the game is running, you can interact with it using the following controls:

  Arrow Keys: Use the arrow keys (up, down, left, right) to move the tiles on the game board.
	'p' Key: Press the 'p' key to enable automatic gameplay using the AI algorithm.

# Features
	Graphical User Interface: The game features a graphical user interface built using Tkinter, providing an interactive gaming experience.
	AI Gameplay: The game includes an AI algorithm that can play the game automatically, making decisions based on specified depths and heuristics.
	Multiple Heuristics: The AI algorithm supports multiple heuristics for evaluating game states, allowing for experimentation and comparison.
	Statistics Tracking: The game tracks various statistics, including move counts, total scores, and game outcomes, which can be useful for analysis and optimization.
