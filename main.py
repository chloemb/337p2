from retriever import retrieve_dict
from ing_parser import parse_ingredients
from step_parser import parse_steps

recipe = retrieve_dict()
#Returns a dict. "Name", "Ingredients" and "Procedure" return appropriate information in a list (except name. Name is not in a list)

parsed_ingredients = parse_ingredients(recipe['Ingredients'])

deletelist = []
for ingredient,details in parsed_ingredients.items():
    if details==dict():
        deletelist.append(ingredient)
for deletething in deletelist:
    parsed_ingredients.pop(deletething)

parse_steps(recipe['Procedure'], parsed_ingredients)
#parsed_steps = parse_steps(recipe['Procedure'])

print("\nRETRIEVED:", recipe, '\n')
print("PARSED INGREDIENTS", parsed_ingredients, '\n')