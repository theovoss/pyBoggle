'''
Created on Jul 29, 2014

@author: jeffvanoss
'''
import unittest
import timeit
import boggle


class AccuracyTests(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test1(self):
        answer = ['chield', 'etched', 'miched', 'pithed', 'teched', 'techie', 'aahed', 'ached', 'acted', 'amice', 'cheth', 'chiel', 'cited', 'deice', 'diced', 'eched', 'ethic', 'lethe', 'maced', 'mache', 'miche', 'theca', 'aced', 'ache', 'acid', 'ahed', 'amah', 'amid', 'amie', 'cede', 'cham', 'chid', 'chip', 'chit', 'cite', 'dice', 'died', 'diel', 'diet', 'dipt', 'dite', 'eche', 'echt', 'elhi', 'etch', 'etic', 'haha', 'held', 'heth', 'hied', 'iced', 'mace', 'mach', 'mica', 'mice', 'mite', 'pica', 'pice', 'pied', 'pima', 'pith', 'tech', 'tied', 'aah', 'ace', 'act', 'aha', 'ahi', 'ama', 'ami', 'cam', 'chi', 'del', 'die', 'dim', 'dip', 'dit', 'edh', 'eld', 'eth', 'hah', 'ham', 'heh', 'het', 'hic', 'hid', 'hie', 'him', 'hip', 'hit', 'ice', 'ich', 'led', 'lei', 'let', 'mac', 'mic', 'mid', 'pic', 'pie', 'pit', 'ted', 'tel', 'the', 'tic', 'tie', 'tip']

        b = boggle.Board((4, 4), ['p', 't', 'e', 'l', 'd', 'i', 'h', 'd', 'h', 'm', 'c', 'e', 'a', 'a', 'h', 't'])
        words = b.findWords()

        self.assertCountEqual(answer, words)

    def test2(self):
        answer = ['ostomy', 'stomal', 'atomy', 'gogos', 'slats', 'slaty', 'stoma', 'stows', 'swots', 'atom', 'glam', 'gogo', 'lats', 'mats', 'mogs', 'most', 'mots', 'slam', 'slat', 'soma', 'sows', 'stow', 'swot', 'togs', 'tost', 'tows', 'wogs', 'wost', 'wots', 'als', 'gos', 'got', 'goy', 'lam', 'lat', 'lax', 'mat', 'max', 'mog', 'mos', 'mot', 'som', 'sot', 'sow', 'soy', 'sty', 'tam', 'tax', 'tog', 'tom', 'tow', 'toy', 'wog', 'wos', 'wot', 'yom', 'zax']

        b = boggle.Board((4, 4), ['y', 'o', 's', 't', 'm', 't', 'g', 'o', 'a', 'x', 'g', 'w', 'z', 'l', 's', 'm'])
        words = b.findWords()

        self.assertCountEqual(answer, words)


class SpeedTests(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test10x10Serial(self):
        print("10x10   findWords():   ", timeit.timeit("game.findWords()", "import boggle; game=boggle.Board((10, 10))", number=10) / 10.0)

    def test10x10Parallel(self):
        print("10x10   findWordsMP(): ", timeit.timeit("game.findWordsMP()", "import boggle; game=boggle.Board((10, 10))", number=4) / 4.0)

    def test100x100Serial(self):
        print("100x100 findWords():   ", timeit.timeit("game.findWords()", "import boggle; game=boggle.Board((100, 100))", number=1))

    def test100x100Parallel(self):
        print("100x100 findWordsMP(): ", timeit.timeit("game.findWordsMP()", "import boggle; game=boggle.Board((100, 100))", number=1))

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
