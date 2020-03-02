import fractions
import re
import nltk
from word_banks import toollist, measurement_bank

# problems: words that are shortened in steps (oil for olive oil),
# mischaracterizing specific words (verbs as nouns, nouns as other things),
# things being capitalized as ingredients (steps have to be lower to catch verbs)

list_of_time_words = ["until", "for"]

def parse_steps(steps, ingredients):
    steps_by_number = {}
    #loop through the steps
    for step in steps:
        step_parsed = {}
        sentences = step.split('.')
        #loop through the sentences in a step
        for sentence in sentences:
            sentence_mod = sentence + " ."
            sentence_dict = {}
            #tag the words in a sentence with a POS tagger
            tokens = nltk.word_tokenize(sentence_mod.lower())
            tagged = nltk.pos_tag(tokens)
            #have a bool that marks when you should be storing things within an associated verb
            start_verb = False
            #loop through the words in a sentence
            most_recent_verb = ''
            timing = ''
            part_of_time = False
            most_recent_adverb = ''
            for pairs in tagged:
                if start_verb is True:
                    if part_of_time is True:
                        # otherwise, add it to time
                        timing = timing + " " + pairs[0]
                    if pairs[0] in list_of_time_words:
                        part_of_time = True
                        timing = timing + " " + pairs[0]
                    if pairs[0] in toollist:
                        #insert something here to get tools as well
                        stored_info.update({"Tools": pairs[0]})
                    if pairs[1] == ':' or pairs[1] == '.':
                        #if a search hits something that indicates its a new sentence, reset search
                        stored_info.update({"Times": timing})
                        stored_info.update({"Related_Verbs": verb_list})
                        sentence_dict[''.join(most_recent_adverb + most_recent_verb)] = stored_info
                        most_recent_adverb = ''
                        start_verb = False
                        part_of_time = False
                    if 'VB' in pairs[1] and pairs[1] != 'VBZ' \
                            and pairs[1] != 'VBD' and pairs[1] != 'VBN' \
                            and pairs[1] != "VBP" and pairs[1] != 'VBG':
                        verb_list.append(pairs[0])

                else:
                    if pairs[1] != "RB" and pairs[1] != ':' and pairs[1] != '.':
                        start_verb = True
                        most_recent_verb = pairs[0]
                        stored_info = {"Ingredients": [], "Tools": [], "Times": [], "Related_Verbs": []}
                        ingredient_list = []
                        verb_list = []
                        for ingredient in ingredients:
                            if ingredient not in ingredient_list:
                                if re.search(" " + ingredient + " ", sentence_mod):
                                    ingredient_list.append(ingredient)
                                    quantity = []
                                    for word in sentence_mod:
                                        print(word)
                                        if word in measurement_bank:
                                            qunatity.append(word)
                            if ingredient not in ingredient_list:
                                if len(ingredient.split()) > 1:
                                    j = len(ingredient.split())
                                    while j > 0:
                                        print(j)
                                        i = 0
                                        while i < j:
                                            holder = ingredient.split()[i:j]
                                            print(holder)
                                            holder_ingredient = ''
                                            for k in holder:
                                                holder_ingredient = holder_ingredient + k + ' '
                                            print(holder_ingredient)
                                            if re.search(" " + holder_ingredient, sentence_mod):
                                                ingredient_list.append(ingredient)
                                                print("break1")
                                                break
                                            i = i + 1
                                        if ingredient in ingredient_list:
                                            print("break2")
                                            break
                                        j = j - 1
                        stored_info.update({"Ingredients": ingredient_list})
                    if pairs[1] == 'RB':
                        most_recent_adverb = pairs[0] + " "

            step_parsed[''.join(sentence)] = sentence_dict
            if sentence == '.':
                del step_parsed['.']
        steps_by_number[''.join(step)] = step_parsed
    print(steps_by_number)
    return steps_by_number