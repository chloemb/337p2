import word_banks
from make_verb_dict import make_all_verbs


def cuisine_morph(cuisine, steps, sorted_ing, sorted_ing_unbase, parsed_ings):
    # categories that ingredients can be sorted into
    ingredient_types = ['Protein', 'Vegetables', 'Seasonings', 'Cooking Medium', 'Carbs', 'Dairy', 'Fruits']

    # found in descriptor_thing in word_banks.py
    ingredient_type_types = {'Protein': ['light_protein', 'heavy_protein'],
                             'Vegetables': ['leafy_veg', 'root_veg'],
                             'Seasonings': ['spicy_sea', 'pungent_sea', 'sweet_sea'],
                             'Carbs': ['pasta', 'grain'],
                             'Dairy': ['solid_dairy', 'cream_dairy'],
                             'Cooking Medium': ['oil_med', 'acidic_med'],
                             'Fruits': ['soft_fruit', 'sweet_fruit', 'citrus_fruit']}

    new_parsed_ing = {}

    been_replaced = []

    for ing_type in ingredient_types:
        ing_list = sorted_ing.get(ing_type)
        if ing_list:
            new_ing_list = []
            for ing in ing_list:
                # find descriptors of certain ingredient
                descriptor = word_banks.thing_descriptor.get(ing)
                # print("ing", ing, "with descriptor", descriptor)
                real_ing = sorted_ing_unbase[ing_type][ing_list.index(ing)]
                if descriptor:
                    # for each kind of this certain ing type, find one in the appropriate cuisine
                    for ing_type_type in ingredient_type_types[ing_type]:
                        if ing_type_type in descriptor:
                            new_ing = find_item([ing_type_type], cuisine, (ing, real_ing))
                            if new_ing:
                                been_replaced.append(ing)
                                new_ing_list.append((real_ing, new_ing))
                                # note replacement in steps
                                steps = add_replace_field(steps, real_ing, new_ing)
                                # note replacement in parsed ing
                                if parsed_ings.get(real_ing):
                                    new_parsed_ing[real_ing] = parsed_ings[real_ing]
                                    parsed_ings.pop(real_ing)
                                # LEAVE THIS PRINT STATEMENT IN
                                if new_ing not in real_ing:
                                    print("REPLACING", real_ing, "with", new_ing)
                if ing not in been_replaced:
                    if parsed_ings.get(real_ing):
                        new_parsed_ing[real_ing] = parsed_ings[real_ing]
                        parsed_ings.pop(real_ing)
                    new_ing_list.append((real_ing, real_ing))
            sorted_ing[ing_type] = new_ing_list

    # for all_ing in parsed_ings.keys():
    #     if all_ing not in new_parsed_ing.keys():
    #         new_parsed_ing[all_ing] = parsed_ings[all_ing]

    # print("NEW SORTED ING", sorted_ing, "\n\n")
    #
    # print("NEW STEPS", steps)

    new_parsed_ing.update(parsed_ings)

    # in sorted ing tuples, the first thing is the ingredient we're replacing,
    # the second is the thing to replace it with
    steps = make_all_verbs(steps)
    return steps, new_parsed_ing


def find_item(attributes, cuisine, ing_pair):
    # print("finding", attributes, cuisine)
    if any(item in ing_pair[1] for item in word_banks.cuisines[cuisine]):
        return ing_pair[0]
    if any(item in ing_pair[0] for item in word_banks.cuisines[cuisine]):
        return ing_pair[1]
    for thing, descriptors in word_banks.thing_descriptor.items():
        if all(attr in descriptors for attr in attributes) and thing in word_banks.cuisines[cuisine]:
            for word_bank_item in word_banks.cuisines[cuisine]:
                if thing in word_bank_item:
                    return word_bank_item
    # print("tried to find item", attributes, cuisine)
    return False


def add_replace_field(steps, to_replace, replace_with):
    for large_step, sentence_dict in steps.items():
        for sentence, sentence_things in sentence_dict.items():
            for verb, verb_things in sentence_things.items():
                if to_replace in verb_things['Ingredients']:
                    steps[large_step][sentence][verb].setdefault('replacement', []).append((to_replace, replace_with))
                else:
                    steps[large_step][sentence][verb].setdefault('replacement', [])
    return steps
