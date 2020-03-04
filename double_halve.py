import unicodedata
import fractions


def double_halve(steps, ing_dict, to_double):
    new_ing_list = []
    for ing in ing_dict.keys():
        new_entry = ing_dict[ing]
        if to_double:
            new_entry['Quantity'][0] = ing_dict[ing]['Quantity'][0] * 2
        else:
            new_entry['Quantity'][0] = ing_dict[ing]['Quantity'][0] / 2
        measure = new_entry.get('Measurement')[0] if new_entry.get('Measurement') else ""
        other = new_entry.get('Other')[0] if new_entry.get('Other') else ""
        to_append = str(new_entry['Quantity'][0]) + " " + measure + " " + ing
        if other:
            to_append += ", " + other
        new_ing_list.append(to_append)
    steps = add_replace_field(steps, to_double)
    print('NEW STEPS', steps)
    return steps, new_ing_list


def add_replace_field(steps, to_double):
    for large_step in steps.keys():
        for sentence in steps[large_step].keys():
            sentence_dict = steps[large_step][sentence]
            verbs_here = sentence_dict.keys()
            for verb in verbs_here:
                ings_here = sentence_dict[verb].get('Ingredients')
                print(ings_here)
                if ings_here:
                    for ing in ings_here.keys():
                        print('ing', ing)
                        if ings_here[ing] is not '':
                            split_measure = ings_here[ing].split()
                            # see if word is a fraction/number
                            try:
                                try:
                                    frac = unicodedata.numeric(split_measure[0])
                                    frac = fractions.Fraction(frac)
                                except:
                                    frac = fractions.Fraction(split_measure[0])
                            except:
                                frac = False

                            if to_double:
                                new_quantity = float(frac) * 2
                            else:
                                new_quantity = float(frac) / 2

                            replace_with = str(new_quantity) + ' ' + split_measure[1]
                            print('replace with', replace_with)
                            sentence_dict[verb].setdefault('replacement', []).append((ings_here[ing], replace_with))
    return steps
