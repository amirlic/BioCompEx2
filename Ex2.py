import string
from random import shuffle, randint
import re
import heapq
from itertools import islice
import operator


def take(n, iterable):
    # Return first n items of the iterable as a list
    return list(islice(iterable, n))


# the main class.
class GeneticAlgorithm:
    def __init__(self):
        self.dictionary = ""
        self.enc = ""
        self.decrypt = []
        self.generation = []
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
    def initialize_permutations(self):
        for i in range(20):
            letters = list(string.ascii_lowercase)
            initial_enc = list(letters)
            shuffle(initial_enc)
            individual = {x: y for x, y in zip(letters, initial_enc)}
            self.reverse_permutation = {v: k for k, v in individual.items()}
            self.generation.append(individual)
        print(self.generation)

    # init the score of every letter in the current permutation.
    def initialize_score(self):
        letters = list(string.ascii_lowercase)
        for letter in letters:
            self.score[letter] = 0
        print(self.score)

    # evaluation function for every letter in the current permutation
    def calculate_fitness(self):
        for i, permutation in enumerate(self.generation):
            score = 0
            decrypt_text = self.enc
            decrypt_text = list(decrypt_text)
            lowercase = list(string.ascii_lowercase)
            decrypt_text = "".join(list(map(lambda x: permutation[x] if x in lowercase else x, decrypt_text)))
            words = [x for x in re.split('[ \n,.\b]', decrypt_text) if x is not '']
            for word in words:
                if word in list(self.dictionary):
                    score += 1
            self.score[i] = score
        print(self.score)

    # printer function
    def printer(self):
        print(self.enc)
        print("-------------------------------------------------------------------------------------------------------")
        print("*********************************************enc*******************************************************")
        print(self.decrypt)

    def new_generation(self):
        fittest = self.selection(2)[:2]
        crossovered = self.crossover()
        pass

    def selection(self, n):
        return [key for key, value in self.score.items() if value in heapq.nlargest(n, self.score.values())]

    def crossover(self):
        sorted_scores = sorted(self.score.items(), key=operator.itemgetter(1))
        sorted_scores.reverse()
        probes = []
        for cons in sorted_scores:
            probes.extend([cons[0]]*cons[1])
        next_generation = []
        for i in range(18):
            parent1 = self.generation[probes[randint(0, len(probes))]]
            parent2 = self.generation[probes[randint(0, len(probes))]]
            genetic_cut = randint(1, len(string.ascii_lowercase) + 1)
            genes1 = take(genetic_cut, parent1.iteritems())
            pass


a = GeneticAlgorithm()
a.read_dict_file()
a.read_enc_file()
a.initialize_permutations()
a.calculate_fitness()
a.new_generation()
a.printer()
