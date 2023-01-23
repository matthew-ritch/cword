This is a simple crossword solver/generator. Give it a board (with or without some words already filled in) and it will find solutions.

Once the script has tried every possibility, it will terminate and print every solution.

Update start.csv to the starting state of the crossword you want to solve.
	Mark cells with '#' if they should be filled with letters.
	Leave "dark" or "block" cells blank.

The dictionary, words.txt, is from [here](https://raw.githubusercontent.com/redbo/scrabble/master/dictionary.txt)

TODO:
	Update the dictionary to include common n-grams
	Select the next word to try in a more intelligent manner (maybe pick the word which gives the most options for future words)
