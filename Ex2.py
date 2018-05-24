import string
from random import shuffle


# the main class.
class GeneticAlgorithm:
    def __init__(self):
        self.dictionary = ""
        self.enc = ""
        self.decrypt = ""
        self.permutation = {}
        self.reverse_permutation = {}
        self.score = {}

    # read the encrypt file to string var
    def read_enc_file(self):
        with open("enc1.txt", 'r') as enc_file:
            self.enc = enc_file.read()

    # read the dict file to string var
    def read_dict_file(self):
        with open("dict.txt", 'r') as dict_file:
            self.dictionary = dict_file.read()

    # init the permutation var
    def initialize_permutation(self):
        letters = list(string.ascii_lowercase)
        initial_enc = list(letters)
        shuffle(initial_enc)
        initial_permutation = {x: y for x, y in zip(letters, initial_enc)}
        self.reverse_permutation = {v: k for k, v in initial_permutation.items()}
        self.permutation = initial_permutation
        print(self.permutation)

    # init the score of every letter in the current permutation.
    def initialize_score(self):
        letters = list(string.ascii_lowercase)
        for letter in letters:
            self.score[letter] = 0
        print(self.score)

    # evaluation function for every letter in the current permutation
    def evaluation(self):
        word = ""
        copy_text = self.enc
        copy_text = list(copy_text)
        abc = list(string.ascii_lowercase)
        copy_text = list(map(lambda x: self.permutation[x] if x in abc else x, copy_text))
        self.decrypt = "".join(copy_text)
        for letter in self.decrypt:
            if letter != ' ' and letter != '\n':
                word = word + letter
                if word in list(self.dictionary) and len(word) > 1:
                    print(word)
                    for l in word:
                        self.score[self.reverse_permutation[l]] += 1
            else:
                word = ""
        print(self.score)

    # printer function
    def printer(self):
        print(self.enc)
        print("-------------------------------------------------------------------------------------------------------")
        print("*********************************************enc*******************************************************")
        print(self.decrypt)


a = GeneticAlgorithm()
a.read_dict_file()
a.read_enc_file()
a.initialize_permutation()
a.initialize_score()
a.evaluation()
#a.printer()
