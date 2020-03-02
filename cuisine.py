import word_banks


def cuisine_morph(cuisine, ingredients, steps, sorted_ing, sorted_ing_unbase):
    protein = sorted_ing.get('Protein')
    if protein:
        new_prot = []
        for prot in protein:
            descriptor = word_banks.thing_descriptor.get(prot)
            real_ing = sorted_ing_unbase['Protein'][protein.index(prot)]
            if descriptor:
                if 'light_protein' in descriptor:
                    new_prot.append((real_ing, find_item(['light_protein'], cuisine)))
                elif 'heavy_protein' in descriptor:
                    new_prot.append((real_ing, find_item(['heavy_protein'], cuisine)))
            else:
                new_prot.append((real_ing, real_ing))
        sorted_ing['Protein'] = new_prot

    veggies = sorted_ing.get('Vegetables')
    if veggies:
        new_veg = []
        for veg in veggies:
            descriptor = word_banks.thing_descriptor.get(veg)
            real_ing = sorted_ing_unbase['Vegetables'][veggies.index(veg)]
            if descriptor:
                if 'leafy_veg' in descriptor:
                    new_veg.append((real_ing, find_item(['leafy_veg'], cuisine)))
                elif 'root_veg' in descriptor:
                    new_veg.append((real_ing, find_item(['root_veg'], cuisine)))
            else:
                new_veg.append((real_ing, real_ing))
        sorted_ing['Vegetables'] = new_veg

    seasonings = sorted_ing.get('Seasonings')
    if seasonings:
        new_sea = []
        for sea in seasonings:
            descriptor = word_banks.thing_descriptor.get(sea)
            real_ing = sorted_ing_unbase['Seasonings'][seasonings.index(sea)]
            if descriptor:
                if 'spicy_sea' in word_banks.thing_descriptor.get(sea):
                    new_sea.append((real_ing, find_item(['spicy_sea'], cuisine)))
                elif 'pungent_sea' in word_banks.thing_descriptor.get(sea):
                    new_sea.append((real_ing, find_item(['pungent_sea'], cuisine)))
                elif 'sweet_sea' in word_banks.thing_descriptor.get(sea):
                    new_sea.append((real_ing, find_item(['sweet_sea'], cuisine)))
            else:
                new_sea.append((real_ing, real_ing))
        sorted_ing['Seasonings'] = new_sea

    media = sorted_ing.get('Cooking Medium')
    if media:
        new_media = []
        for med in media:
            descriptor = word_banks.thing_descriptor.get(med)
            real_ing = sorted_ing_unbase['Cooking Medium'][media.index(med)]
            if descriptor:
                if 'oil_med' in descriptor:
                    new_media.append((real_ing, find_item(['oil_med'], cuisine)))
                elif 'acidic_med' in descriptor:
                    new_media.append((real_ing, find_item(['acidic_med'], cuisine)))
            else:
                new_media.append((real_ing, real_ing))
        sorted_ing['Cooking Medium'] = new_media

    carb = sorted_ing.get('Carbs')
    if carb:
        new_carb = []
        for car in carb:
            descriptor = word_banks.thing_descriptor.get(car)
            real_ing = sorted_ing_unbase['Carbs'][carb.index(car)]
            if descriptor:
                if 'western_pasta' in descriptor:
                    new_carb.append((real_ing, find_item(['western_pasta'], cuisine)))
                elif 'eastern_pasta' in word_banks.thing_descriptor.get(car):
                    new_carb.append((real_ing, find_item(['western_pasta'], cuisine)))
            else:
                new_carb.append((real_ing, real_ing))
        sorted_ing['Carbs'] = new_carb

    dairy = sorted_ing.get('Dairy')
    if dairy:
        new_dairy = []
        for dai in dairy:
            descriptor = word_banks.thing_descriptor.get(dai)
            real_ing = sorted_ing_unbase['Dairy'][dairy.index(dai)]
            if descriptor:
                if 'solid_dairy' in descriptor:
                    new_dairy.append((real_ing, find_item(['solid_dairy'], cuisine)))
                elif 'cream_dairy' in word_banks.thing_descriptor.get(dai):
                    new_dairy.append((real_ing, find_item(['cream_dairy'], cuisine)))
            else:
                new_dairy.append((real_ing, real_ing))
        sorted_ing['Dairy'] = new_dairy

    print("NEW SORTED ING", sorted_ing, "\n\n")

    # in sorted ing tuples, the first thing is the ingredient we're replacing,
    # the second is the thing to replace it with
    return ingredients, steps, sorted_ing


def find_item(attributes, cuisine):
    for thing, descriptors in word_banks.thing_descriptor.items():
        if all(attr in descriptors for attr in attributes) and thing in word_banks.cuisines[cuisine]:
            for word_bank_item in word_banks.cuisines[cuisine]:
                if thing in word_bank_item:
                    return word_bank_item
    print("tried to find item", attributes, cuisine)
    return "Not Found"
