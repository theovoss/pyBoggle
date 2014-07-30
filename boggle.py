import random
import pickle
import timeit
import multiprocessing as mp 

class Board:
    def __init__(self, shape=(4,4), board=None):
        self.diceVal=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','qu','r','s','t','u','v','w','x','y','z']
        self.maxWordLen=15 #28 for wordsEn.txt
        self.minWordLen=3
        self.shape = shape
#         self.board = [[ random.choice(self.diceVal) for _y in range(shape[1])] for _x in range(shape[0])]
        
        self.board = {}
        if board is None or len(board) < shape[0]*shape[1]:
            for x in range(self.shape[0]):
                for y in range(self.shape[1]):
                    self.board[(x,y)] = random.choice(self.diceVal)
        else: # load from board
            indx=0
            for x in range(self.shape[0]):
                for y in range(self.shape[1]):
                    self.board[(x,y)] = board[indx]
                    indx+=1
        
        
        self.wordhash = {}
        try:
            self.wordhash = self._loadWordHash()
        except:
            self.wordhash = self._makeWordHash(save=True)
        
    def __str__(self):
        s = '|' + '-'*(3*self.shape[1]) + '|\n'
        for x in range(self.shape[0]):
            s += '|'
            for y in range(self.shape[1]):
                s += '{:3}'.format(self.board[(x,y)])
            s += '|\n'
        s += '|' + '-'*(3*self.shape[1]) + '|\n'
        return s

    def _makeWordHash(self, save=False):
        with open('TWL06.txt', 'r') as f:
            words = f.readlines()
            
        for indx in range(len(words)):
            words[indx]=words[indx].strip().lower()
        
        wordHash = {}
        for word in words:
            for indx in range(1,len(word)+1):
                if word[:indx] not in wordHash:
                    wordHash[word[:indx]] = False
                if indx == len(word):
                    wordHash[word[:indx]] = True
        if save is True:
            with open("wordHash.pickle", 'wb') as f:
                pickle.dump(wordHash, f)
        return wordHash
    
    def _loadWordHash(self):
        with open("wordHash.pickle", 'rb') as f:
            wordHash = pickle.load(f)
        return wordHash

    def findWords(self):
        words = set()
        for x in range(self.shape[0]):
            for y in range(self.shape[1]):
                words.update(self._findWordsRec(self.board[(x,y)], [(x,y)]))
        return words
    
    def findWordsMP(self):
        words = set()

        inputs=[]
        for x in range(self.shape[0]):
            for y in range(self.shape[1]):
                inputs.append((self.board[(x,y)], [(x,y)]))
                
        pool_size = mp.cpu_count()
        if pool_size > 1:
            pool_size -= 1 #leave one core for other tasks
        pool = mp.Pool(processes=pool_size)
        pool_outputs = pool.map(self._findWordsRecMP, inputs)
        pool.close()
        pool.join()
        
        for output in pool_outputs:
            words.update(output)
            
        return words
    
    def _findWordsRecMP(self, args):
        return self._findWordsRec(*args)
    
    '''
    returns set of words possible given starting coordinates    
    '''
    def _findWordsRec(self, word, points):
        words = set()
        if len(points) < self.maxWordLen:
            for point in self._addPoint(points):
                newWord = word+self.board[point]
                if newWord in self.wordhash:
                    newPoints = list(points); newPoints.append(point)
                    words.update(self._findWordsRec(newWord, newPoints))
                    if len(newWord) >= self.minWordLen and self.wordhash[newWord]:
                        words.add(newWord)
        return words
    
    def _addPoint(self, points):
        x, y = points[-1]
        for p in [(x-1, y-1), 
                  (x-1, y  ), 
                  (x-1, y+1), 
                  (x  , y-1), 
                  (x  , y+1), 
                  (x+1, y-1), 
                  (x+1, y  ), 
                  (x+1, y+1)]:
            if 0<=p[0]<self.shape[0] and 0<=p[1]<self.shape[1] and p not in points:
                yield p

if __name__ == '__main__':
#     game = Board((10,10))
#     print(game)
#     words = game.findWords()
#     print(words)
#     words = game.findWordsMP()
#     print(words)
#     print(len(words))
#     print("findWords():   ", timeit.timeit("words=game.findWords()", "from __main__ import game, words", number=10)/10.0)
#     print("findWordsMP(): ", timeit.timeit("words=game.findWordsMP()", "from __main__ import game, words", number=4)/4.0)
    
#     import cProfile
#     cProfile.run("game.findWords()")
    
    game = Board((200,200))
    print(game)
    words = game.findWords()
    print(words)
    print(len(words))
    print("findWords():   ", timeit.timeit("words=game.findWords()", "from __main__ import game, words", number=1))
    print("findWordsMP(): ", timeit.timeit("words=game.findWordsMP()", "from __main__ import game, words", number=1))
# 
#     import cProfile
#     cProfile.run("game.findWords()")
    