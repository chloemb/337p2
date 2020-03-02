from retriever import retrieve_dict
from ing_parser import parse_ingredients
from step_parser import parse_steps
from double_halve import double_halve
from ing_sorter import sorter
from vegetarianify import vegetarian
#from cuisine import cuisine_morph

recipe = retrieve_dict()
#Returns a dict. "Name", "Ingredients" and "Procedure" return appropriate information in a list (except name. Name is not in a list)

parsed_ingredients = parse_ingredients(recipe['Ingredients'])

deletelist = []
for ingredient,details in parsed_ingredients.items():
    if details==dict():
        deletelist.append(ingredient)
for deletething in deletelist:
    parsed_ingredients.pop(deletething)

parsed_steps = parse_steps(recipe['Procedure'], parsed_ingredients)
sorted_ings, sorted_ings_base = sorter(parsed_ingredients.keys())

print("\nRETRIEVED:", recipe, '\n')
print("PARSED INGREDIENTS", parsed_ingredients, '\n')
print("PARSED STEPS", parsed_steps, '\n')
print("SORTED INGREDIENTS", sorted_ings, sorted_ings_base, '\n')

print("Transforming", recipe['Name'], "\nPlease enter the number of the transformation you'd like to apply:")
print("1: Double Ingredients")
print("2: Halve Ingredients")
print("3: Change cuisine to ___")
print("4: Make vegetarian")
print("5: Make Italian\n")
transform = input()

if transform == "1":
    transformed_ing = double_halve(parsed_ingredients, True)
elif transform == "2":
    transformed_ing = double_halve(parsed_ingredients, False)
elif transform == "4":
    transformed_ing = vegetarian(parsed_ingredients, recipe, parsed_steps)
elif transform == "5":
    transformed_ing = cuisine_morph('italian', parsed_steps, parsed_ingredients, sorted_ings_base, sorted_ings)
else:
    transformed_ing = "Not assigned"

print(transformed_ing)
