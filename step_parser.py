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
            most_recent_adjective = ''
            possible_compound = ''
            #allows us to set things within the key for their associated verb even several words later
            for pairs in tagged:
                print(pairs)
                if pairs[1] == 'ADJ':
                    most_recent_adjective = pairs[0]
                if pairs[1] == 'ADV':
                    most_recent_adverb = pairs[0]
                if start_verb is True:
                    if part_of_time is True:
                        # otherwise, add it to time
                        timing = timing + " " + pairs[0]
                    if pairs[0] in list_of_time_words:
                        part_of_time = True
                        timing = timing + " " + pairs[0]
                    if pairs[1] == 'NN' or "JJ":
                        if most_recent_adjective + pairs[0] in ingredients:
                            old_ingreds = stored_info["Ingredients"]
                            old_ingreds.append(most_recent_adjective + pairs[0])
                            most_recent_adjective = ''
                            stored_info.update({"Ingredients": old_ingreds})
                            # if the noun is an ingredient, add it to ingredients
                        elif most_recent_adjective + possible_compound + pairs[0] in ingredients:
                            old_ingreds = stored_info["Ingredients"]
                            old_ingreds.append(most_recent_adjective + possible_compound + pairs[0])
                            most_recent_adjective = ''
                            possible_compound = ''
                            stored_info.update({"Ingredients": old_ingreds})
                        else:
                            possible_compound = pairs[0] + " "
                        #insert something here to get tools as well
                        #stored_info.update({"Tools": tool})
                    if pairs[1] == ':' or pairs[1] == '.':
                        #if a search hits something that indicates its a new sentence, reset search
                        print(stored_info)
                        stored_info.update({"Times": timing})
                        sentence_dict[''.join(most_recent_adverb + most_recent_verb)] = stored_info
                        most_recent_adverb = ''
                        start_verb = False
                        part_of_time = False

                else:
                    if pairs[1] == 'VB' or 'VBD' or "VBZ":
                        start_verb = True
                        most_recent_verb = pairs[0]
                        stored_info = {"Ingredients": [], "Tools": [], "Times": []}

            step_parsed[''.join(sentence)] = sentence_dict
        steps_by_number[''.join(step)] = step_parsed
    return steps_by_number
