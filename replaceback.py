import sys

def replace_back_steps(alldict,stepnew):
    #print(alldict)
    #print(alldict,"\n")
    #print(alldict,"\n",stepnew)
    entire_string = []
    for sentence, rest in alldict.items():
        finalver = sentence
        sentence=sentence.lower()
        adaptlist = []
        for verb, data in stepnew.items():
            done = True
            if verb in sentence:
                adaptlist.append(verb)
                done = False
            try:
                data['replacement'][verb]
                adaptlist.append(verb)
                done = False
            except:
                pass
        #print(adaptlist)

        for verb in adaptlist:
            if verb in sentence:
                backup = sentence
                recognizelist = []
                for replacefrom, replaceinto in stepnew[verb]['replacement']:
                    #print(stepnew[verb]['replacement'])
                    #print(replacefrom, replaceinto, finalver)
                    recognizelist += recognize_ingredient(replacefrom, sentence,replaceinto)

                recognizelist.sort(reverse=True,key=helper2)
                for thing,replace in recognizelist:
                    #print(thing,replace,finalver)
                    finalver=finalver.replace(thing,replace)
                
                #print(finalver)
                if backup != sentence:
                    stepnew.pop(verb)

        entire_string.append(finalver)
    #print(entire_string)
    return entire_string                

#recognizies ingredient in the context of a sentence
def recognize_ingredient(ingredient, sentence,replacement):

    retlist = []
    recognize = ""

    for word in range(len(sentence.split(" "))):
        if (sentence.split(" ")[word] in ingredient) and (len(sentence.split(" ")[word]) > 2) and (len(sentence.split(" ")[word]) not in ignorelist):
            while sentence.split(" ")[word] in ingredient and word < len(sentence.split(" ")):
                recognize=recognize+(sentence.split(" ")[word]+" ")
                word+=1
            recognize=recognize[:-1]
            retlist.append((recognize,replacement))
            recognize = ''
    retlist.sort(key=lenhelp,reverse=True)
    return retlist


ignorelist=['that','which','then','the','and']


def lenhelp(str):
    return len(str)

def helper2(list):
    return len(list[0])

def determine_measure(dict):
    #Behold the tragic consequences of not wanting to mess w your friends code
    #and it being awkward for the thing you were asked to do
    #and it became this ugly thing
    #it says something about the importance of open communication
    measure = []
    quantity = []
    try:
        measure = dict['Measurement']
    except:
        pass
    try:
        quantity = dict['Quantity']
    except:
        pass
    for m in measure:
        #print(m,m[:-1],m[-1])
        if m[-1]=="s":
            m=m[:-1]
    if measure ==[]:
        if quantity == []:
            return ""

        return str(sum(quantity)).replace(".0","")+ " "
    if quantity == []:
        return "A "+ measure[0].capitalize() + " of "
    
    if len(measure) == 1:
        sstring = ""
        if sum(quantity) != 1.0:
            sstring = "s"
        return str(sum(quantity)).replace(".0","") +" "+ measure[0].capitalize()+sstring+" "

    measures = {"delete":'lol'}
    measures.pop('delete') #I couldn't find the actual initialize command
    returnstr = ""
    for x in range(min(len(measure),len(quantity))):
        #print(measure,quantity,measures,x)
        try: 
            measures[measure[x]] += quantity[x]
        except:
            measures[measure[x]] = quantity[x]
    for m,q in measures.items():
        sstring = ""
        if q != 1.0:
            sstring = "s"
        returnstr += " and "  + str(q).replace(".0","")+" " +m.capitalize()+sstring
    return returnstr.replace(" and ","",1)+" "


def replace_back_ingredients(parseingredients, newdict):
    newingredients = []
    #print(newdict)
    for ingredient, details in newdict.items():
        #print(details)
        capitalized = False
        entry = "- "
        entry = determine_measure(details)
        if entry != "- ":
            capitalized=True
        #how are we supposed to handle separate prep steps?
        #That would go here regardless
        if not capitalized:
            entry += ingredient.capitalize()+"\n"
        else:
            entry+=ingredient + "\n"
        #print(entry)
        newingredients.append(entry)
    return newingredients

def render_recipe(ingredients, steps, bigsteps):
    print(ingredients,"\n",steps)
    newingredients = replace_back_ingredients(bigsteps,ingredients)
    newsteps = replace_back_steps(bigsteps,steps)
    print(newingredients,"\n",newsteps)
    sys.exit()
    print("***INGREDIENTS***\n")
    for ingredient in newingredients:
        print(ingredient)
    print("** RECIPE STEPS **")
    for step in newsteps:
        print("    "+step+"\n")
    return
    