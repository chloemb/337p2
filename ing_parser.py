import fractions
import re
import unicodedata
import sys
import string
from word_banks import measurement_bank
from word_banks import prep_words


def parse_ingredients(ingredients):
    ingredients_parsed = {}
    for ing in ingredients:
        item_dict = {}

        # remove things within parentheses (revisit this later)
        if '('  in ing or ')' in ing:
            try:
                pre, paren = ing.split('(')
                paren, post = paren.split(')')
                if any(measure in paren for measure in measurement_bank):
                    if len(post) >= len(pre):
                        ing = paren + post
                    else:
                        ing = pre + paren
                else:
                    ing = re.sub(r'\([^)]*\)', '', ing) #original solution  
            except:
                ing = re.sub(r'\([^)]*\)', '', ing) #original solution

        # # remove punctuation except for . and / and , (revisit this as well)
        # ing = re.sub(r'[^\w\s/.,]', '', ing)

        parse_this = ing.split()
        not_words = []
        i = 0
        while i < len(parse_this)-1:
            # see if word is a fraction/number
            try:
                try:
                    frac = unicodedata.numeric(parse_this[i])
                    frac = fractions.Fraction(frac)
                except:
                    frac = fractions.Fraction(parse_this[i])
            except:
                frac = False

            # see if next word is a fraction/number
            try:
                try:
                    next_frac = unicodedata.numeric(parse_this[i+1])
                    next_frac = fractions.Fraction(next_frac)
                except:
                    next_frac = fractions.Fraction(parse_this[i+1])
            except:
                next_frac = False

            # if this word is a quantity
            if frac:
                quantity = frac
                not_words.append(parse_this[i])
                # if mixed number
                if next_frac and '/' in parse_this[i+1]:
                    quantity += next_frac
                    item_dict.setdefault('Quantity', []).append(float(quantity))
                    not_words.append(parse_this[i+1])
                    check_measure = 2
                # if not mixed number
                else:
                    item_dict.setdefault('Quantity', []).append(float(quantity))
                    check_measure = 1
                # find measurement associated with this quantity
                if any(measure_word in parse_this[i+check_measure] for measure_word in measurement_bank):
                    item_dict.setdefault('Measurement', []).append(parse_this[i+check_measure])
                    not_words.append(parse_this[i+check_measure])
                    i += 1+check_measure
                else:
                    i += check_measure
            else:
                i += 1

        # get out words ending in "ed" for preparation. also get rid of "and"
        for word in parse_this:
            if any(prep_word in word for prep_word in prep_words):
                item_dict.setdefault('Preparation', []).append(word)
                not_words.append(word)
            if 'and' in word:
                not_words.append(word)

        # remove measurement and quantity words from the string, leaving only the item
        for word in not_words:
            if word in parse_this:
                parse_this.remove(word)

        # remove remaining measure words
        for word in parse_this:
            if word in measurement_bank:
                parse_this.remove(word)

        # add item to parsed ingredients. if item is already in parsed ingredients, add * to it before adding. can only
        # handle a max of two same ingredients.
        ing_to_add = re.sub(r'[^\w\s]', '', ' '.join(parse_this))
        if ingredients_parsed.get(ing_to_add):
            ingredients_parsed[ing_to_add]["Quantity"] = item_dict["Quantity"] + ingredients_parsed[ing_to_add]["Quantity"]
            item_dict.setdefault('Measurement', [])
            ingredients_parsed[ing_to_add].setdefault('Measurement', []).append(item_dict["Measurement"])
            ingredients_parsed[ing_to_add]["Measurement"].append(item_dict["Measurement"])
        else:
            ingredients_parsed[ing_to_add] = item_dict
    return ingredients_parsed

