import word_banks


def sorter(ingredients):
    sorted_dict = {}
    for ing in ingredients:
        ing_lower = ing.lower()
        if any(prot in ing_lower for prot in word_banks.proteins) \
                and not any(nprot in ing for nprot in word_banks.not_protein):
            sorted_dict.setdefault('Protein', []).append(ing)

        if any(veg in ing_lower for veg in word_banks.veggies) \
                and not any(nveg in ing for nveg in word_banks.not_veg):
            # for veg in word_banks.veggies:
            #     if veg in ing:
            #         print(veg)
            sorted_dict.setdefault('Vegetables', []).append(ing)

        if any(fr in ing_lower for fr in word_banks.fruits) \
                and not any(nfr in ing for nfr in word_banks.not_fruit):
            sorted_dict.setdefault('Fruits', []).append(ing)

        if any(sp in ing_lower for sp in word_banks.seasonings) \
                and not any(nsp in ing for nsp in word_banks.not_seasoning):
            sorted_dict.setdefault('Seasonings', []).append(ing)

        if any(med in ing_lower for med in word_banks.media):
            sorted_dict.setdefault('Cooking Medium', []).append(ing)

        if any(carb in ing_lower for carb in word_banks.carbs):
            sorted_dict.setdefault('Carbs', []).append(ing)

    return sorted_dict
