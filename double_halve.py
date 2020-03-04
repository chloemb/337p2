import unicodedata
import fractions


def double_halve(steps, ing_dict, to_double):
    new_ing_list = []
    for ing in ing_dict.keys():
        new_entry = ing_dict[ing]
        for quant_entry in ing_dict[ing]['Quantity']:
            if to_double:
                new_entry['Quantity'][ing_dict[ing]['Quantity'].index(quant_entry)] = \
                    ing_dict[ing]['Quantity'][ing_dict[ing]['Quantity'].index(quant_entry)] * 2
            else:
                new_entry['Quantity'][ing_dict[ing]['Quantity'].index(quant_entry)] = \
                    ing_dict[ing]['Quantity'][ing_dict[ing]['Quantity'].index(quant_entry)] / 2
        measure = new_entry.get('Measurement')[0] if new_entry.get('Measurement') else ""
        other = new_entry.get('Other')[0] if new_entry.get('Other') else ""
        to_append = str(new_entry['Quantity'][0]) + " " + measure + " " + ing
        if other:
            to_append += ", " + other
        new_ing_list.append(to_append)
        ing_dict[ing]['Quantity'] = new_entry['Quantity']
    steps = add_replace_field(steps, to_double)
    print("STEPS WITH REPLACE", steps)
    steps = make_all_verbs(steps)
    return steps, ing_dict


def add_replace_field(steps, to_double):
    for large_step, sentence_dict in steps.items():
        for sentence, sentence_things in sentence_dict.items():
            for verb, verb_things in sentence_things.items():
                ings = verb_things['Ingredients']
                for ing, ing_value in ings.items():
                    if ing_value != '':
                        split_measure = ing_value.split()
                        # see if word is a fraction/number
                        try:
                            try:
                                frac = unicodedata.numeric(split_measure[0])
                                frac = fractions.Fraction(frac)
                            except:
                                frac = fractions.Fraction(split_measure[0])
                        except:
                            frac = False

                        if frac:
                            if to_double:
                                new_quantity = float(frac) * 2
                            else:
                                new_quantity = float(frac) / 2
                            replace_with = str(new_quantity) + ' ' + split_measure[1]
                            steps[large_step][sentence][verb].setdefault('replacement', []).\
                                append((ing_value, replace_with))
                steps[large_step][sentence][verb].setdefault('replacement', [])
    return steps


def make_all_verbs(steps):
    new_steps = {}
    for large_step, sentence_dict in steps.items():
        for sentence, sentence_things in sentence_dict.items():
            for verb, verb_things in sentence_things.items():
                new_steps[verb] = verb_things
    return new_steps
