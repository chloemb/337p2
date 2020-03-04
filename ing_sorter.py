import word_banks


def sorter(ingredients):
    sorted_dict = {}
    sorted_dict_base = {}
    for ing in ingredients:
        ing_lower = ing.lower()
        if any(prot in ing_lower for prot in word_banks.proteins) \
                and not any(nprot in ing_lower for nprot in word_banks.not_protein):
            sorted_dict.setdefault('Protein', []).append(ing)
            sorted_dict_base.setdefault('Protein', []).append(find_which_ing(ing, word_banks.proteins))

        if any(veg in ing_lower for veg in word_banks.veggies) \
                and not any(nveg in ing_lower for nveg in word_banks.not_veg):
            # for veg in word_banks.veggies:
            #     if veg in ing:
            #         print(veg)
            sorted_dict.setdefault('Vegetables', []).append(ing)
            sorted_dict_base.setdefault('Vegetables', []).append(find_which_ing(ing, word_banks.veggies))

        if any(fr in ing_lower for fr in word_banks.fruits) \
                and not any(nfr in ing_lower for nfr in word_banks.not_fruit):
            sorted_dict.setdefault('Fruits', []).append(ing)
            sorted_dict_base.setdefault('Fruits', []).append(find_which_ing(ing, word_banks.fruits))

        if any(sp in ing_lower for sp in word_banks.seasonings) \
                and not any(nsp in ing_lower for nsp in word_banks.not_seasoning):
            sorted_dict.setdefault('Seasonings', []).append(ing)
            sorted_dict_base.setdefault('Seasonings', []).append(find_which_ing(ing, word_banks.seasonings))

        if any(med in ing_lower for med in word_banks.media) \
                and not any(nmed in ing_lower for nmed in word_banks.not_med):
            sorted_dict.setdefault('Cooking Medium', []).append(ing)
            sorted_dict_base.setdefault('Cooking Medium', []).append(find_which_ing(ing, word_banks.media))

        if any(carb in ing_lower for carb in word_banks.carbs) \
                and not any(ncarb in ing_lower for ncarb in word_banks.not_carbs):
            sorted_dict.setdefault('Carbs', []).append(ing)
            sorted_dict_base.setdefault('Carbs', []).append(find_which_ing(ing, word_banks.carbs))

        if any(top in ing_lower for top in word_banks.toppings):
            sorted_dict.setdefault('Toppings', []).append(ing)
            sorted_dict_base.setdefault('Toppings', []).append(find_which_ing(ing, word_banks.toppings))

        if any(dai in ing_lower for dai in word_banks.dairy):
            sorted_dict.setdefault('Dairy', []).append(ing)
            sorted_dict_base.setdefault('Dairy', []).append(find_which_ing(ing, word_banks.dairy))

    return sorted_dict, sorted_dict_base


def find_which_ing(ing, ing_list):
    for item in ing_list:
        if item in ing:
            return item
