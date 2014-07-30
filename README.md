pyBoggle
========

Boggle Solver

Call `Boggle(size, layout, wordlist)` to generate board. `size` is a tuple of 
columns and rows on the board (default 4x4). 'layout' is a row major array of
strings to map to board; if not set layout is randomly generated. `wordlist`
is wordlist is a string of valid words, or a path to a text file with valid
words. Call the `findWords()` method to search the board.