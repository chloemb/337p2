import word_banks
from make_verb_dict import make_all_verbs


def unvegetarianify(parsed_steps, sorted_ings_base, sorted_ings, parsed_ingredients, name):
    # find first protein
    main_prot = sorted_ings_base.get('Protein')
    if main_prot:
        if main_prot[0] in word_banks.replace_with_meat.keys():
            parsed_steps = add_replace_field(parsed_steps, sorted_ings['Protein'][0], word_banks.replace_with_meat[main_prot[0]])
            parsed_ingredients.pop(sorted_ings['Protein'][0])
            parsed_ingredients[word_banks.replace_with_meat[main_prot[0]]] = {'Quantity': [8.0],
                                                    'Measurement': ['oz']}
    else:
        parsed_ingredients['chicken breast'] = {'Quantity': [8.0],
                                                'Measurement': ['oz']}
        parsed_steps = add_new_step(parsed_steps, 'chicken breast')

    steps = make_all_verbs(parsed_steps)
    return steps, parsed_ingredients


def add_replace_field(steps, to_replace, replace_with):
    for large_step, sentence_dict in steps.items():
        for sentence, sentence_things in sentence_dict.items():
            for verb, verb_things in sentence_things.items():
                if to_replace in verb_things['Ingredients']:
                    steps[large_step][sentence][verb].setdefault('replacement', []).append((to_replace, replace_with))
                else:
                    steps[large_step][sentence][verb].setdefault('replacement', [])
    return steps


def add_new_step(steps, ing_to_add):
    steps['Grill ' + ing_to_add + ' on medium heat for 7-8 minutes, or until done. Serve on top.'] = \
        {'Grill ' + ing_to_add + ' on medium heat for 7-8 minutes, or until done':
             {'heat': {'Ingredients': {ing_to_add: ''},
                       'Tools': 'grill',
                       'Times': '7-8 minutes',
                       'Related_Verbs': [],
                       'replacement': []}},
         'Serve on top':
             {'serve': {'Ingredients': {}},
              'Tools': [],
              'Times': '',
              'Related_Verbs': [],
              'replacement': []}
         }
    return steps
