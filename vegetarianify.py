from word_banks import not_vegetarian
import sys

def vegetarian(ingredients,recipe,steps):
    
    newsteps = {}
    for step,thing in steps.items():
        for why,actually in thing.items():
            for key,contents in actually.items():
                newsteps[key]=contents
                newsteps[key]['replacement']=[]


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


    for problem in non_veg:
        resolved = False
        #deal w specific things (spices, bouillon)
        for edge, replace in edgefoods.items():
            if edge in problem:
                resolved=True
                ingredients[replace] = ingredients[problem]
                for stepverb, stepstuff in newsteps.items():
                    if problem in stepstuff['Ingredients']:
                        stepstuff['Ingredients'][replace] = ''
                        stepstuff['Ingredients'].pop(problem)
                        stepstuff['replacement'].append((problem,replace))
                ingredients.pop(problem)
        if not resolved:
            adapt(ingredients,newsteps,problem, recipe)
            

    return ingredients, newsteps

        

        
    
             
def decide_replace(problem,newsteps,recipe):
    #try to figure protein recommendation based on type of food
    foodtype = ""
    #try to figure protein recommendation based on things done to ingredients here
    #fancier version will add probabilities or something
    for stepv,stepstuff in newsteps.items():
        if problem not in stepstuff['Ingredients']:
            continue
        for classifier in [main,stewey,greenmix]:
            if any(verb in stepstuff['Related_Verbs'] for verb in classifier['steps']):
                return classifier['ret']
    if foodtype == "":
        for classifier in [main,stewey,greenmix]:
            for foodgroup in classifier['title']:
                if foodgroup in recipe['Name']:
                    return classifier['ret']
    #we can default to hard tofu. its the stereotype for a reason
    return 'hard tofu'

    #main replacement loop
    #first we deal with edge foods
    #Then we replace standard uses of the things



def adapt(ingredients, newsteps,problem,recipe):
    new = decide_replace(problem,newsteps,recipe)
    #if its already there, all we have to do is add seitan and switch mentions of problem ingredient to seitan.
    try:
        ingredients[new]['quantity'] += ingredients[new]['quantity']
        for stepverb, stepstuff in newsteps.items():
            if problem in stepstuff['Ingredients']:
                if (problem,replacement) not in stepstuff['replacement']:
                    stepstuff['replacement'].append((problem,new))
                stepstuff['Ingredients'][new]=""
                stepstuff['Ingredients'].pop(problem)
        ingredients.pop(problem)
        return
    #else for ingredients we make it take the quantity and details of the original
    #for steps we append basic prep for the ingredient in question
    except:
        ingredients[new] = ingredients[problem]
        for stepverb, stepstuff in newsteps.items():
            if problem in stepstuff['Ingredients']:
                if (problem,new) not in stepstuff['replacement']:
                    stepstuff['replacement'].append((problem,new))
                stepstuff['Ingredients'][new]=''
                stepstuff['Ingredients'].pop(problem)
            #also add prep for the ingredient??
        ingredients.pop(problem)
        



    


#aim is to return the same dict as before, replace title, ingredients and steps

#for small bits of flavor and dishes where this is supposed to be the main, seitan makes the most sense
main = {'title':['taco','burrito','rice bowl','roast'],'steps':['stir-fry','roast','grill','dress'],'ret':'seitan'}

#if we're sinking it into the flavor of something, tofu is the only one that makes sense
stewey = {'title':['soup','curry','stew'],'steps':['marinate','steep','steam','brew','roast'],'ret':'soft tofu'}

#Basically no salads will look weird substituting w tempeh
greenmix = {'title':['salad','greens'],'steps':['toss'],'ret':'tempeh'}

#add more to these?
edgefoods = {'bouillon':'vegetable bouillon','broth':'vegetable broth','fat':'lard','seasoning':'allspice','meat':'dish'}