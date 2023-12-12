This is a simple crossword solver/generator. Give it a board (with or without some words already filled in) and it will find solutions.

Once the script has tried every possibility, it will terminate and print every solution.

Update start.csv to the starting state of the crossword you want to solve.
	Mark cells with '#' if they should be filled with letters.
	Leave "dark" or "block" cells blank.



The dictionary, words.txt, is a combination of single words from [here](https://raw.githubusercontent.com/redbo/scrabble/master/dictionary.txt) and 
bigrams from [here](https://norvig.com/ngrams/count_2w.txt).

It seems like this problem is at least [NP-hard](https://arxiv.org/abs/2109.11203) in general, but we can use some tricks to make this more manageable.

TODO:
	Select the next word to try in a more intelligent manner (maybe pick the word which gives the most options for future words).
	
![](https://github.com/matthew-ritch/cword/blob/main/script_in_progress.png)