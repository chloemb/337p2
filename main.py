from retriever import retrieve_dict
from ing_parser import parse_ingredients
from step_parser import parse_steps
from double_halve import double_halve

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

print("\nRETRIEVED:", recipe, '\n')
print("PARSED INGREDIENTS", parsed_ingredients, '\n')
print("PARSED STEPS", parsed_steps, '\n')

print("Transforming", recipe['Name'], ". Please enter the number of the transformation you'd like to apply:")
print("1: Double Ingredients \n")
print("2: Halve Ingredients \n")
print("3: Change cuisine to ___\n")
transform = input()

if transform == "1":
    transformed_ing = double_halve(parsed_ingredients, True)
elif transform == "2":
    transformed_ing = double_halve(parsed_ingredients, False)
else:
    transformed_ing = "Not assigned"

print(transformed_ing)
