from retriever import retrieve_dict
from ing_parser import parse_ingredients
from step_parser import parse_steps
from double_halve import double_halve
from ing_sorter import sorter
from vegetarianify import vegetarian
from cuisine import cuisine_morph
from health import health
from replaceback import replace_back_steps, replace_back_ingredients,render_recipe
#from cuisine import cuisine_morph
import sys
from unvegetarianify import unvegetarianify

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

# print("\nRETRIEVED:", recipe, '\n')
# print("PARSED INGREDIENTS", parsed_ingredients, '\n')
# print("PARSED STEPS", parsed_steps, '\n')
# print("SORTED INGREDIENTS", sorted_ings, '\n', sorted_ings_base, '\n')

print("Transforming", recipe['Name'], "\nPlease enter the number of the transformation you'd like to apply:")
print("1: Double Ingredients")
print("2: Halve Ingredients")
print("3: Change cuisine to a more Italian style")
print("4: Make vegetarian")
print("5: Make not vegetarian")
print("6: Make healthy")
print("7: Make unhealthy\n")

# <<<<<<< HEAD
while True:
    transform = input()
    if transform == "1":
        print("Doubling the recipe for", recipe['Name'], ":")
        new_steps, transformed_ing = double_halve(parsed_steps, parsed_ingredients, True)
        render_recipe(transformed_ing, new_steps, parsed_steps)
        sys.exit()
    elif transform == "2":
        print("Halving the recipe for", recipe['Name'], ":")
        new_steps, transformed_ing = double_halve(parsed_steps, parsed_ingredients, False)
        render_recipe(transformed_ing, new_steps, parsed_steps)
        sys.exit()
    elif transform == "3":
        print("Making", recipe['Name'], "Italian:")
        print(sorted_ings)
        new_steps, new_ing = cuisine_morph('italian', parsed_steps, sorted_ings_base, sorted_ings, parsed_ingredients)
        render_recipe(new_ing, new_steps, parsed_steps)
        print(new_steps)
        sys.exit()
    elif transform == "4":
        print("Making", recipe['Name'], "vegetarian:")
        transformed_ing = vegetarian(parsed_ingredients, recipe, parsed_steps)
        render_recipe(transformed_ing[0],transformed_ing[1],parsed_steps,"veg")
        sys.exit()
    elif transform == "5":
        print("Making", recipe['Name'], "not vegetarian:")
        new_steps, new_ing = unvegetarianify(parsed_steps, sorted_ings_base, sorted_ings, parsed_ingredients, recipe['Name'])
        render_recipe(new_ing, new_steps, parsed_steps)
        sys.exit()
    elif transform == "6":
        print("Making", recipe['Name'], "healthy:")
        transformed_ing = health(parsed_ingredients,recipe,parsed_steps)
        # print(transformed_ing[1])
        render_recipe(transformed_ing[0],transformed_ing[1],parsed_steps)
        sys.exit()
    else:
        print("That's not an option - please try again!")
# =======
# transform = input()
#
# if transform == "1":
#     new_steps, transformed_ing = double_halve(parsed_steps, parsed_ingredients, True)
#     render_recipe(transformed_ing, new_steps, parsed_steps)
# elif transform == "2":
#     new_steps, transformed_ing = double_halve(parsed_steps, parsed_ingredients, False)
#     render_recipe(transformed_ing, new_steps, parsed_steps)
# elif transform == "4":
#     transformed_ing = vegetarian(parsed_ingredients, recipe, parsed_steps)
#     #print(parsed_steps)
#     #print(replace_back_steps(parsed_steps,transformed_ing[1]))
#     #replace_back_ingredients(parsed_ingredients,transformed_ing[0])
#     render_recipe(transformed_ing[0],transformed_ing[1],parsed_steps)
#     #replace_back_steps(parsed_steps,transformed_ing[1])
#     pass
# elif transform == "5":
#     new_steps, new_ing = cuisine_morph('italian', parsed_steps, sorted_ings_base, sorted_ings, parsed_ingredients)
#     print(new_steps,"\n")
#     #print("new steps", new_steps)
#     render_recipe(new_ing, new_steps, parsed_steps)
# elif transform == "6":
#     transformed_ing = health(parsed_ingredients,recipe,parsed_steps)
#     render_recipe(transformed_ing[0],transformed_ing[1],parsed_steps)
# else:
#     transformed_ing = "Not assigned"
#
# #print(transformed_ing)
# >>>>>>> de9b18cd7228e4d6e11bee70d4a5e452684ef9c5
