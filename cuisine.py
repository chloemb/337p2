from word_banks import cuisines


def cuisine_morph(cuisine, ingredients, steps, sorted_ing):
    protein = sorted_ing['Protein']
    if protein:
        sorted_ing['Protein'] = cuisines[cuisine]['protein'][:len(protein)]
    return ingredients, steps, sorted_ing
