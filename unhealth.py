from word_banks import descriptor_thing
import sys


def unhealthy(ingredients,recipe,steps):
    #insert random honduras joke here    
    newsteps = {}
    for step,thing in steps.items():
        for why,actually in thing.items():
            for key,contents in actually.items():
                newsteps[key]=contents
                newsteps[key]['replacement'] = []

    
    #python why like actually python why I miss C so so much python WHY
    #ngl Im sure theres a less ugly but still ugly way to python this but
    #literally shouldnt have to
    adaptlist = []
    doubled = []
    for yummy,replace in foods.items():
        for ingredient,details in ingredients.items():
            if decide_replace(ingredient,yummy):
                fixreplace = compile_ingredient(ingredient,yummy,replace)
                adaptlist.append((ingredient, fixreplace))
                #print(yummy, ingredient)
            else:
                if any(bad in ingredient for bad in bad_health):
                    try:
                        if ingredient not in doubled:
                            #print("problem")
                            details['Quantity'] *= 2
                            #print("nonexistent")
                            doubled.append(ingredient)
                    except:
                        pass
    for ingredient, replace in adaptlist:
        adapt_thing(ingredients,newsteps,ingredient,replace)

    for yummy,replace in methods.items():
        for verb, rest in newsteps.items():
            if verb in yummy or yummy in verb:
                adapt_method(yummy, replace, newsteps,ingredients)

    return ingredients, newsteps

bad_health = ['fat','cream','cheese','lard','flavoring','seasoning','salt','sauce','oil']

def compile_ingredient(ingredient, yummy, replace):
    preserve = ["broth",'sauce','chunks','bouillon']
    if any(p in ingredient for p in preserve):
        if ingredient.replace(yummy,replace) != ingredient:
            return ingredient.replace(yummy,replace)
    return replace

        
def decide_replace(problem, listentry):
    if (problem in listentry or listentry in problem) and problem != listentry:
        if not any(ignore in problem for ignore in ignore_list):
            return True
    return False
             
def decide_replace_thing(problem,steps):
    #try to figure protein recommendation based on things done to ingredients here
    #fancier version will add probabilities or something
    for replacefrom,replaceinto in foods.items():
        if (replacefrom in problem or problem in replacefrom) and problem != replacefrom:
            return replaceinto
    # print("Error: Caught unknown ingredient")
    #we can default to hard tofu. its the stereotype for a reason
    return 'hard tofu'



def adapt_thing(ingredients, newsteps,problem,replace):
    if problem == replace:
        return
    #if its already there, all we have to do is add seitan and switch mentions of problem ingredient to its replacement.
    try:
        ingredients[replace]['Quantity'] += ingredients[problem]['Quantity'] * 2
        for stepverb, stepstuff in newsteps.items():
            if problem in stepstuff['Ingredients']:
                if (problem,replace) not in stepstuff['replacement']:
                    stepstuff['replacement'].append(problem,replace)
                stepstuff['Ingredients'].append(replace)
                stepstuff['Ingredients'].remove(problem)
        ingredients.pop(problem)
        return
    #else for ingredients we make it take the quantity and details of the original
    #for steps we append basic prep for the ingredient in question
    except:
        #print(problem,replace,ingredients)
        ingredients[replace] = ingredients[problem]
        try:
            ingredients[replace]['Quantity'] = ingredients[replace]['Quantity'] * 2
        except:
            pass
        for stepverb, stepstuff in newsteps.items():
            if problem in stepstuff['Ingredients']:
                if (problem,replace) not in stepstuff['replacement']:
                    stepstuff['replacement'].append((problem,replace))
                stepstuff['Ingredients'][replace] = ''
                stepstuff['Ingredients'].pop(problem)
            #also add prep for the ingredient??
        ingredients.pop(problem)
        

def adapt_method(problem, replace,newsteps,ingredients):

    newsteps[replace] = newsteps[problem]
    newsteps.pop(problem)
    for tool in newsteps[replace]["Tools"]:
        if tool in large_tools:
            newsteps[replace]["Tools"].remove(tool)
            newsteps[replace]['replacement'].append((problem,replace))
    newsteps[replace]["Tools"].append(methodtools[replace])




#aim is to return the same dict as before, replace title, ingredients and steps

#for small bits of flavor and dishes where this is supposed to be the main, seitan makes the most sense
foods = {'margerine':'butter', 'tempeh':'bacon', 'tofu':'pork', 'zucchini cheese':'cheese', 'Splenda':'sugar', 'chicken':'pork','beef':'pork','chicken':'pork','brown rice': 'rice','bread':'whole-grain bread','olive oil':'lard','yogurt':'sour cream','egg whites':'egg','unsweetened cocoa':'sweetened cocoa'}



ignore_list = {'seasoning','bouillon'}

methods = {'grill':'saute', 'boil':'fry', 'steam':'fry'}
methodtools = {'grill':'grill','saute':'skillet','fry':'frier', 'boil':'pot','roast':'pan','steam':'steamer'}

toollist = ['dipper', 'brasero', 'fillet knife', 'skillet', 'cheesemelter', 'range', 'processor', 'oven', 'thermometer',
            'opener', 'boiler', 'tamis', 'reamer', 'kyoto box', 'lame', 'tongs', 'pestle and mortar', 'stove',
            'multicooker', 'potato ricer', 'scoop', 'susceptor', 'regulator', 'piercer', 'fryer', 'poacher',
            'coffeemaker', 'frother', 'corer', 'shaker', 'iron', 'microplane', 'kettle', '  dispenser', 'spoon',
            'twine', 'scaler', 'roasting jack', 'brazier', 'steamer', 'rotimatic', 'shichirin', 'shears', 'machine',
            'corkscrew', 'Cheesecloth', 'baster', 'circulator', 'haybox', 'needle', 'mandoline', 'tray', 'peeler',
            'comal', 'rotisserie', 'curler', 'nutcracker', 'board', 'crepe maker', 'mezzaluna', 'pot-holder', 'baller',
            'chocolatera', 'knife', 'cutter', 'tandoor', 'mortar and pestle', 'separator', 'maker', 'brush',
            'lobster pick', 'timer', 'tenderiser', 'docker', 'sieve', 'scales', 'mess kit', 'torch', 'remoska',
            'press', 'ladle', 'spatula', 'bowl', 'blender', 'burjiko', 'squeezer', 'scissors', 'sifter',
            'measuring cup', 'Pie bird', 'glove', 'boilers', 'percolator', 'cleaver', 'saucepan','saucer',
            'crab cracker', 'grinder', 'bag', 'roaster', 'colander', 'slotted spoon', 'samovar', 'grill', 'mill',
            'horno', 'masher', 'tangia', 'roller', 'beanpot', 'whisk', 'kitchen', 'microwave', 'pitter',
            'edible tableware', 'hot box', 'strainer', 'Rice polisher', 'cooker', 'scraper', 'pot', 'broiler',
            'plate', 'Zester', 'kamado', 'grater', 'chopper', 'sabbath mode', 'rolling pin', 'makiyakinabe',
            'blow torch', 'chinois', 'funnel', 'mated colander pot', 'heater', 'slicer', 'bottle opener',
            'server', 'kujiejun', 'toaster']
large_tools = ['skillet','range', 'oven','boiler', 'stove','multicooker', 'fryer', 'steamer','boilers','saucepan','saucer','roaster','grill','microwave', 'cooker', 'broiler']