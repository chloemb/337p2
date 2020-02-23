import fractions
import re


def parse_ingredients(ingredients):
    ingredients_parsed = {}
    for ing in ingredients:
        item_dict = {}

        # remove all punctuation except for / (for fractions) from the ingredient string
        ing = re.sub(r'[^\w\s/]', '', ing)

        words = ing.split()
        not_words = []
        for i in range(len(words)-1):
            # see if word is a fraction/number
            try:
                frac = fractions.Fraction(words[i])
            except:
                frac = False

            # see if next word is a fraction/number
            try:
                next_frac = fractions.Fraction(words[i+1])
            except:
                next_frac = False

            # if word is a fraction/number, add it as a quantity
            if frac:
                item_dict.setdefault('Quantity', []).append(words[i])
                not_words.append(words[i])
                # if the word after it is not a fraction/number and is also not the last word, add it as a measurement
                if not next_frac and not i+1 == len(words)-1:
                    item_dict.setdefault('Measurement', []).append(words[i+1])
                    not_words.append(words[i+1])

        # remove measurement and quantity words from the string, leaving only the item
        for word in not_words:
            words.remove(word)

        # add item to parsed ingredients
        ingredients_parsed[' '.join(words)] = item_dict
    return ingredients_parsed
