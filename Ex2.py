import string
from random import shuffle, randint, uniform
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
        self.generation = []
        self.fitnesses = {}

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
        for i in range(100):
            letters = list(string.ascii_lowercase)
            initial_enc = list(letters)
            shuffle(initial_enc)
            individual = {x: y for x, y in zip(letters, initial_enc)}
            self.generation.append(individual)
        # print(self.generation)

    # evaluation function for every individual in the current generation
    def calculate_generation_fitnesses(self):
        for i, individual in enumerate(self.generation):
            self.fitnesses[i] = self.calculate_fitness(individual)

    # evaluation function for one individual in the current generation
    def calculate_fitness(self, individual):
        fitness = 0
        decrypt_text = self.decrypt_text(individual)
        words = [x for x in re.split('[ \n,.\b]', decrypt_text) if x is not '']
        for word in words:
            if word in list(self.dictionary):
                fitness += 1
        return fitness

    # decrypt the text according to a given individual's decryption
    def decrypt_text(self, individual):
        decrypt_text = self.enc
        decrypt_text = list(decrypt_text)
        lowercase = list(string.ascii_lowercase)
        # decrypt the text according to current permutation
        decrypt_text = "".join(list(map(lambda x: individual[x] if x in lowercase else x, decrypt_text)))
        return decrypt_text

    # prints the solution of the genetic algo
    def printer(self, solution):
        print(self.enc)
        print("-------------------------------------------------------------------------------------------------------")
        print("********************************************decryption*************************************************")
        print("-------------------------------------------------------------------------------------------------------")
        print 'fittest: ',  solution[0]
        print 'fitness: ', solution[1]
        print 'decryption: ', solution[2]

    # create new generation using the genetic functions
    def new_generation(self):
        # get the fittest individuals
        fittest = [self.generation[i] for i in self.selection(10)[:10]]
        # create crossovers from the current population
        crossovered = self.crossover()
        crossovered.extend(fittest)
        # mutate the population and set it as the new generation
        self.generation = self.mutations(crossovered)

    # select the fittest individuals in the population
    def selection(self, n):
        return [key for key, value in self.fitnesses.items() if value in heapq.nlargest(n, self.fitnesses.values())]

    # crossover the population giving fitter individuals better chances to be crossovered
    def crossover(self):
        sorted_scores = sorted(self.fitnesses.items(), key=operator.itemgetter(1))
        sorted_scores.reverse()
        probes = []
        for cons in sorted_scores:
            probes.extend([cons[0]]*cons[1])
        next_generation = []
        # create crossovers from the current population
        for i in range(90):
            parent1 = self.generation[probes[randint(0, len(probes) - 1)]]
            parent2 = self.generation[probes[randint(0, len(probes) - 1)]]
            # merge two genes to one in random point
            genetic_cut = randint(1, len(string.ascii_lowercase) + 1)
            gene1 = take(genetic_cut, parent1.iteritems())
            gene2 = {entry for j, entry in enumerate(parent2.iteritems()) if j >= genetic_cut}
            gene1.extend(gene2)
            next_generation.append(dict(gene1))
        return next_generation

    # mutate the population by const probability
    def mutations(self, current_generation):
        # for each individual mutate it by const probability
        for individual in current_generation:
            if uniform(0, 1) <= 0.03:
                mutation_key_letter = string.ascii_lowercase[randint(1, len(string.ascii_lowercase)) - 1]
                mutation_value_letter = string.ascii_lowercase[randint(1, len(string.ascii_lowercase)) - 1]
                individual[mutation_key_letter] = mutation_value_letter
        return current_generation

    # run the main algo, create new generation till getting the solution
    def run_genetic_algo(self):
        self.initialize_permutations()
        fittest = None
        for i in range(20):
            self.calculate_generation_fitnesses()
            # check whether the current fittest is the "right" solution
            fittest = self.fittest()
            decrypt_text = self.decrypt_text(fittest)
            decrypt_len = len([x for x in re.split('[ \n,.\b]', decrypt_text) if x is not ''])
            if self.calculate_fitness(fittest)/float(decrypt_len) > 0.8:
                return [fittest, self.calculate_fitness(fittest), self.decrypt_text(fittest)]
            # create new generation
            self.new_generation()
        return [fittest, self.calculate_fitness(fittest), self.decrypt_text(fittest)]

    # return the fittest individual in thr current population
    def fittest(self):
        self.calculate_generation_fitnesses()
        fitest_index = max(self.fitnesses.iteritems(), key=operator.itemgetter(1))[0]
        return self.generation[fitest_index]

# main
a = GeneticAlgorithm()
a.read_dict_file()
a.read_enc_file()
solution = a.run_genetic_algo()
a.printer(solution)