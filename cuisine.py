import word_banks


def cuisine_morph(cuisine, steps, sorted_ing, sorted_ing_unbase):
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

    for ing_type in ingredient_types:
        ing_list = sorted_ing.get(ing_type)
        if ing_list:
            new_ing_list = []
            for ing in ing_list:
                # find descriptors of certain ingredient
                descriptor = word_banks.thing_descriptor.get(ing)
                real_ing = sorted_ing_unbase[ing_type][ing_list.index(ing)]
                not_yet = True
                if descriptor:
                    # for each kind of this certain ing type, find one in the appropriate cuisine
                    for ing_type_type in ingredient_type_types[ing_type]:
                        if ing_type_type in descriptor:
                            not_yet = False
                            new_ing = find_item([ing_type_type], cuisine, (ing, real_ing))
                            new_ing_list.append((real_ing, new_ing))
                            # note replacement in steps
                            steps = add_replace_field(steps, real_ing, new_ing)
                            # LEAVE THIS PRINT STATEMENT IN
                            if new_ing not in real_ing:
                                print("Replacing", real_ing, "with", new_ing)
                if not_yet:
                    new_ing_list.append((real_ing, real_ing))
            sorted_ing[ing_type] = new_ing_list

    # print("NEW SORTED ING", sorted_ing, "\n\n")
    #
    # print("NEW STEPS", steps)

    # in sorted ing tuples, the first thing is the ingredient we're replacing,
    # the second is the thing to replace it with
    return steps, sorted_ing


def find_item(attributes, cuisine, ing_pair):
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
    return "Not Found"


def add_replace_field(steps, to_replace, replace_with):
    for large_step in steps.keys():
        for sentence in steps[large_step].keys():
            sentence_dict = steps[large_step][sentence]
            sentence_dict.setdefault('replacement', []).append((to_replace, replace_with))
    return steps
