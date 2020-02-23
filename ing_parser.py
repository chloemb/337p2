import fractions
import re

measurement_bank = ('teaspoon', 'tablespoon', 'cup', 'lb', 'package', 'pinch', 'sprinkle', 'ounce', 'oz', 'stalk',
                    'whole', 'sprig', 'leaf', 'bottle', 'liter', 'pound', 'can', 'clove', 'head')

def parse_ingredients(ingredients):
    ingredients_parsed = {}
    for ing in ingredients:
        item_dict = {}

        # remove things within parentheses (revisit this later)
        ing = re.sub(r'\([^)]*\)', '', ing)

        # # remove punctuation except for . and / and , (revisit this as well)
        # ing = re.sub(r'[^\w\s/.,]', '', ing)

        words = ing.split(', ')
        words_0, words_1 = words[0].split(), words[1:]
        not_words = []
        i = 0
        while i < len(words_0)-1:
            # see if word is a fraction/number
            try:
                frac = fractions.Fraction(words_0[i])
            except:
                frac = False

            # see if next word is a fraction/number
            try:
                next_frac = fractions.Fraction(words_0[i+1])
            except:
                next_frac = False

            # if this word is a quantity
            if frac:
                not_words.append(words_0[i])
                # if mixed number
                if next_frac and '/' in words_0[i+1]:
                    item_dict.setdefault('Quantity', []).append(' '.join([words_0[i], words_0[i+1]]))
                    not_words.append(words_0[i+1])
                    check_measure = 2
                # if not mixed number
                else:
                    item_dict.setdefault('Quantity', []).append(words_0[i])
                    check_measure = 1
                # find measurement associated with this quantity
                if any(measure_word in words_0[i+check_measure] for measure_word in measurement_bank):
                    item_dict.setdefault('Measurement', []).append(words_0[i+check_measure])
                    not_words.append(words_0[i+check_measure])
                    i += 1+check_measure
                else:
                    i += check_measure
            else:
                i += 1

        if not words_1 == []:
            item_dict['Other'] = words_1

        # remove measurement and quantity words from the string, leaving only the item
        for word in not_words:
            words_0.remove(word)

        # add item to parsed ingredients
        ingredients_parsed[' '.join(words_0)] = item_dict
    return ingredients_parsed
