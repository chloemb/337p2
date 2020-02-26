import fractions
import re
import nltk

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
            sentence = sentence + "."
            sentence_dict = {}
            #tag the words in a sentence with a POS tagger
            tokens = nltk.word_tokenize(sentence.lower())
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
                        #insert something here to get tools as well
                        #stored_info.update({"Tools": tool})
                    if pairs[1] == ':' or pairs[1] == '.':
                        #if a search hits something that indicates its a new sentence, reset search
                        stored_info.update({"Times": timing})
                        stored_info.update({"Related_Verbs": verb_list})
                        sentence_dict[''.join(most_recent_adverb + most_recent_verb)] = stored_info
                        print(sentence_dict)
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
                                if ingredient in sentence:
                                    ingredient_list.append(ingredient)
                            if ingredient not in ingredient_list:
                                if len(ingredient.split()) > 1:
                                    holder_ingredient = ingredient.split()[1]
                                    if holder_ingredient in sentence:
                                        ingredient_list.append(ingredient)
                        stored_info.update({"Ingredients": ingredient_list})
                    if pairs[1] == 'RB':
                        most_recent_adverb = pairs[0] + " "

            step_parsed[''.join(sentence)] = sentence_dict
            if sentence == '.':
                del step_parsed['.']
        steps_by_number[''.join(step)] = step_parsed
    return steps_by_number
