import word_banks


def cuisine_morph(cuisine, ingredients, steps, sorted_ing):
    protein = sorted_ing['Protein']
    if protein:
        for prot in protein:
            if 'light_protein' in word_banks.thing_descriptor[prot]:
                find_item(('light_protein'), 'italian')
    return ingredients, steps, sorted_ing


def find_item(attributes, cuisine):
    for thing, descriptors in word_banks.thing_descriptor:
        if all(attr in descriptors for attr in attributes) and :
            return thing
    return "Not Found"
