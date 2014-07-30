'''
Created on Jul 29, 2014

@author: jeffvanoss
'''
import unittest
import boggle

class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test1(self):
        answer = ['chield', 'etched', 'miched', 'pithed', 'teched', 'techie', 'aahed', 'ached', 'acted', 'amice', 'cheth', 'chiel', 'cited', 'deice', 'diced', 'eched', 'ethic','lethe', 'maced', 'mache', 'miche', 'theca', 'aced', 'ache', 'acid', 'ahed', 'amah', 'amid', 'amie', 'cede', 'cham', 'chid', 'chip', 'chit', 'cite', 'dice', 'died', 'diel', 'diet', 'dipt', 'dite', 'eche', 'echt', 'elhi', 'etch', 'etic', 'haha', 'held', 'heth', 'hied', 'iced', 'mace', 'mach', 'mica', 'mice', 'mite', 'pica', 'pice', 'pied', 'pima', 'pith', 'tech', 'tied', 'aah', 'ace', 'act', 'aha','ahi', 'ama', 'ami', 'cam', 'chi', 'del', 'die', 'dim', 'dip', 'dit', 'edh', 'eld', 'eth', 'hah', 'ham', 'heh', 'het', 'hic', 'hid', 'hie', 'him', 'hip', 'hit', 'ice', 'ich', 'led', 'lei', 'let', 'mac', 'mic', 'mid', 'pic', 'pie', 'pit', 'ted', 'tel', 'the', 'tic', 'tie', 'tip']
        
        b = boggle.Board((4,4), ['p', 't', 'e', 'l', 'd', 'i', 'h', 'd', 'h', 'm', 'c', 'e', 'a', 'a', 'h', 't'])
        words = b.findWords()
        
        self.assertCountEqual(answer, words)

    def test2(self):
        answer = ['ostomy', 'stomal', 'atomy', 'gogos', 'slats', 'slaty', 'stoma', 'stows', 'swots', 'atom', 'glam', 'gogo', 'lats', 'mats', 'mogs', 'most', 'mots', 'slam', 'slat', 'soma', 'sows', 'stow', 'swot', 'togs', 'tost', 'tows', 'wogs', 'wost', 'wots', 'als', 'gos', 'got', 'goy', 'lam', 'lat', 'lax', 'mat', 'max', 'mog', 'mos','mot', 'som', 'sot', 'sow', 'soy', 'sty', 'tam', 'tax', 'tog', 'tom', 'tow', 'toy', 'wog', 'wos', 'wot', 'yom', 'zax']

        b = boggle.Board((4,4), ['y', 'o', 's', 't', 'm', 't', 'g', 'o', 'a', 'x', 'g', 'w', 'z', 'l', 's', 'm'])
        words = b.findWords()
        
        self.assertCountEqual(answer, words)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()