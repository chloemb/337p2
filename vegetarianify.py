from word_banks import not_vegetarian

def vegetarian(ingredients,recipe,steps):
    #check to see if anything needs to be done
    #if it does, store non-vegetarian things in a list
    vegetarian = True
    non_veg = []
    for yummy in not_vegetarian:
        for ingredient in ingredients:
            #we check like this to catch the likes of "beef bouillon"
            if yummy in ingredient:
                vegetarian = False
                non_veg.append(ingredient)
    if vegetarian:
        return ingredients,recipe,steps

    #try to figure protein recommendation based on type of food
    foodtype = ""
    for classifier in [main,stewey,greenmix]:
        for foodgroup in classifier['title']:
            if foodgroup in recipe['title']:
                foodtype = classifier['ret']
    if foodtype == "":
        #try to figure protein recommendation based on things done to ingredients here
        #fancier version will add probabilities or something
        for classifier in [main,stewey,greenmix]:
            for verb in classifier['steps']:
                if verb in steps:
                    foodtype = classifier['ret']
    #we can default to hard tofu. its the stereotype for a reason
    if foodtype == "":
        foodtype = 'generic'


    #main replacement loop
    #first we deal with edge foods
    #Then we replace standard uses of the things
    replacements = {}
    for problem in non_veg:
        resolved = False
    
             

    

    


#aim is to return the same dict as before, replace title, ingredients and steps

#for small bits of flavor and dishes where this is supposed to be the main, seitan makes the most sense
main = {'title':['taco','burrito','rice bowl','roast'],'steps':['stir-fry','roast','grill','dress'],'ret':'main'}

#if we're sinking it into the flavor of something, tofu is the only one that makes sense
stewey = {'title':['soup','curry','stew'],'steps':['marinate','steep','steam','brew'],'ret':'stew'}

#Basically no salads will look weird substituting w tempeh
greenmix = {'title':['salad','greens'],'steps':['toss'],'ret':'salad'}

#add more to these?
edgefoods = {'bouillon':'vegetable bouillon','broth':'vegetable broth','fat':'lard'}