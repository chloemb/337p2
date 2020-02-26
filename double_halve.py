import fractions


def double_halve(ing_dict, to_double):
    new_ing_list = []
    for ing in ing_dict.keys():
        new_entry = ing_dict[ing]
        if to_double:
            new_entry['Quantity'][0] = float(ing_dict[ing]['Quantity'][0] * 2)
        else:
            new_entry['Quantity'][0] = float(ing_dict[ing]['Quantity'][0] / 2)
        measure = new_entry.get('Measurement')[0] if new_entry.get('Measurement') else ""
        other = new_entry.get('Other')[0] if new_entry.get('Other') else ""
        to_append = str(new_entry['Quantity'][0]) + " " + measure + " " + ing
        if other:
            to_append += ", " + other
        new_ing_list.append(to_append)
    return new_ing_list
