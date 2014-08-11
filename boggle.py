import random
import pickle
import multiprocessing as mp
import os
import string


class Board:
    def __init__(self, shape=(4, 4), layout=None, wordlist=None):
        '''
        Create a boggle board. Board can be a rectangle of any size. If layout
        is not specified, it will be randomly generated.

        :param shape: an iterable where first two values are integers that
                      represent number of columns and rows respectively.
        :param layout: a board layout to use. Must be string of separated
                       letters, or an array of strings (each string
                       representing one dice position). If layout is not
                       provided or not parsable, a random layout will be
                       determined
        :param wordlist: A string containing either a valid path to a text file
                         that contains word list, or a string of words
        '''
        diceVal = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                   'j', 'k', 'l', 'm', 'n', 'o', 'p', 'qu', 'r',
                   's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        self.minWordLen = 3
        self.shape = (int(shape[0]), int(shape[1]))

        # load word list into a dictionary.
        # Try from various methods of interpreting passed word list
        self.wordhash = {}
        if isinstance(wordlist, str):
            if os.path.exists(wordlist):
                # string might be a path to a text file of words
                with open(wordlist, 'r') as f:
                    wordlist = f.read().lower().split(string.digits + string.whitespace + string.punctuation)
                    self.wordhash = self._makeWordHash(wordlist)
            else:
                # string must list of words separated by a non letter character
                wordlist = wordlist.lower().split(string.digits + string.whitespace + string.punctuation)
                self.wordhash = self._makeWordHash(wordlist)
        else:
            try:
                # see if the pass object will parse
                self.wordhash = self._makeWordHash(wordlist)
            except:
                # load from previously saved file or load from default word list
                try:
                    self.wordhash = self._loadWordHash()
                except:
                    path = 'TWL06.txt'
                    if os.path.exists(path):
                        with open(path, 'r') as f:
                            wordlist = f.read().lower().split(string.digits + string.whitespace + string.punctuation)
                            self.wordhash = self._makeWordHash(wordlist)

        # Try to parse input layout into array of strings, otherwise, generate
        # a random layout
        self.board = {}
        if isinstance(layout, str):
            layout = layout.lower().split(string.digits + string.whitespace + string.punctuation)
        if layout is None or len(layout) < shape[0] * shape[1]:
            layout = [random.choice(diceVal) for _i in range(self.shape[0] * self.shape[1])]

        # Construct board. Internally board is represented
        # as dictionary where keys are tuple coordinates, (row, column),
        # and values are strings.
        indx = 0
        for x in range(self.shape[0]):
            for y in range(self.shape[1]):
                self.board[(x, y)] = layout[indx]
                indx += 1

    def __str__(self):
        '''
        Pretty Print the board layout
        '''
        s = '|' + '-' * (3 * self.shape[1]) + '|\n'
        for x in range(self.shape[0]):
            s += '|'
            for y in range(self.shape[1]):
                s += '{:3}'.format(self.board[(x, y)])
            s += '|\n'
        s += '|' + '-' * (3 * self.shape[1]) + '|\n'
        return s

    def _makeWordHash(self, words):
        '''
        Create dictionary of words and word prefixes. Saves to file for fast
        recall

        :param words: list of strings, one word each
        '''
        wordHash = {}
        for word in words:
            for indx in range(1, len(word) + 1):
                if word[:indx] not in wordHash:
                    wordHash[word[:indx]] = False
                if indx == len(word):
                    wordHash[word[:indx]] = True

        with open("wordHash.pickle", 'wb') as f:
            pickle.dump(wordHash, f)
        return wordHash

    def _loadWordHash(self):
        '''
        Load previously saved dictionary of words
        '''
        with open("wordHash.pickle", 'rb') as f:
            wordHash = pickle.load(f)
        return wordHash

    def findWords(self):
        '''
        Find words in the board. Uses serial search
        '''
        words = set()
        for x in range(self.shape[0]):
            for y in range(self.shape[1]):
                words.update(self._findWordsRec(self.board[(x, y)], [(x, y)]))
        return words

    def findWordsMP(self):
        '''
        Find words in the board. Uses parallel search
        '''
        words = set()

        inputs = []
        for x in range(self.shape[0]):
            for y in range(self.shape[1]):
                inputs.append((self.board[(x, y)], [(x, y)]))

        pool_size = mp.cpu_count()
        if pool_size > 1:
            pool_size -= 1  # leave one core for other tasks
        pool = mp.Pool(processes=pool_size)
        pool_outputs = pool.map(self._findWordsRecMP, inputs)
        pool.close()
        pool.join()

        for output in pool_outputs:
            words.update(output)

        return words

    def _findWordsRecMP(self, args):
        '''
        Recursive call for findWordsMP(), since the multiprocessing.pool.map()
        function can only pass one argument to each pool process, this
        intermediate function unpacks the arguments.
        :param args:
        '''
        return self._findWordsRec(*args)

    def _findWordsRec(self, prefix, points):
        '''
        Recursive search function. Return set of words possible given starting
        coordinates.

        :param prefix: word prefix represented by points
        :param points: sequential coordinates on the board
        '''
        words = set()
        for point in self._addPoint(points):
            newWord = prefix + self.board[point]
            if newWord in self.wordhash:
                newPoints = list(points) + [point]
                words.update(self._findWordsRec(newWord, newPoints))
                if len(newWord) >= self.minWordLen and self.wordhash[newWord]:
                    words.add(newWord)
        return words

    def _addPoint(self, points):
        '''
        Return generator of viable points given a list of previously chosen
        points. A viable point is one space horizontally, vertically, or
        diagonally from the last coordinate in points. The new point is inside
        the board boundaries and not in the passed points list.

        :param points: sequential coordinates on the board
        '''
        x, y = points[-1]
        for p in [(x - 1, y - 1),
                  (x - 1, y),
                  (x - 1, y + 1),
                  (x, y - 1),
                  (x, y + 1),
                  (x + 1, y - 1),
                  (x + 1, y),
                  (x + 1, y + 1)]:
            if 0 <= p[0] < self.shape[0] and 0 <= p[1] < self.shape[1] and p not in points:
                yield p

if __name__ == '__main__':
    pass
