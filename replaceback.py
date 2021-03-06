import sys

def replace_back_steps(alldict,stepnew,transform = ""):
    # print(alldict)
    #print(alldict,"\n")
    #print(alldict,"\n",stepnew)

    entire_string = []

    for sentence, rest in alldict.items():
        
        finalver = sentence
        sentence=sentence.lower()
        adaptlist = []
        for verb, data in stepnew.items():
            if verb in sentence:
                adaptlist.append(verb)
            try:
                data['replacement'][verb]
                adaptlist.append(verb)
            except:
                pass
        recognizelist = []
        for verb in adaptlist:
            if verb in sentence:
                backup = sentence
                recognizelist = []
                # print("CHECK REPLACE", stepnew[verb])
                if not stepnew[verb].get('replacement'):
                    continue
                for replacefrom, replaceinto in stepnew[verb]['replacement']:
                    # print("REPLACING HERE",stepnew[verb]['replacement'])
                    #print(replacefrom, replaceinto, finalver)

                    # basically, if the thing we are trying to put in starts with a number, we assume it's a quantity
                    # replacement and look for replacefrom exactly in the sentence
                    try:
                        float(replaceinto.split()[0])
                        is_float = True
                    except:
                        is_float = False
                    if is_float:
                        if replacefrom in sentence:
                            recognizelist += [(replacefrom, replaceinto)]

                    # if it's a not a measure, do the other thing
                    else:
                        recognizelist += recognize_ingredient(replacefrom, sentence,replaceinto)
                recognizelist.sort(reverse=True,key=helper2)
                # print("recognize list is", recognizelist)
                for thing,replace in recognizelist:
                    #print(thing,replace,finalver)
                    # print("thing, replace", thing,replace)
                    finalver=finalver.replace(replace,"a1b2c3asdf")
                    finalver=finalver.replace(thing,replace)
                    finalver=finalver.replace("a1b2c3asdf", replace)
                # print("finalver", finalver)
                if backup != sentence:
                    stepnew.pop(verb)
        if (transform == "veg"):
            for problem, fix in veg_replace.items():
                finalver=finalver.replace(problem,fix)
        # print(finalver)
        entire_string.append(finalver)
    #print(entire_string)
    return entire_string                

veg_replace = {'meat':'greens'}

def applylist(rlist,sentence):
    applied = []
    for thing,replace in rlist:
        if not any(thing in app for app in applied):
            
            sentence = sentence.replace(thing,replace)
            applied.append(replace)
    return sentence


#recognizies ingredient in the context of a sentence
def recognize_ingredient(ingredient, sentence,replacement):
    retlist = []
    recognize = ""
    #chloe caught bad substitutions here
    for word in range(len(sentence.split(" "))):
        if (depunctuate(sentence.split(" ")[word]) in ingredient) and (len(sentence.split(" ")[word]) > 2) and (len(sentence.split(" ")[word]) not in ignorelist):
            while word < len(sentence.split(" ")) and depunctuate(sentence.split(" ")[word]) in ingredient:
                # print("HERE>>>>>>")
                recognize=recognize+(sentence.split(" ")[word]+" ")
                word+=1
            #print(recognize)
            recognize=recognize[:-1]
            if recognize != replacement:
                retlist.append((recognize,repunctuate(recognize,replacement)))
            recognize = ''
    retlist.sort(key=lenhelp,reverse=True)
    #print(retlist)
    return retlist

def depunctuate(word):
    punctuations = '\'!()-[]\{\};:\"\/,<>.?@#$%^&*_~'
    for char in punctuations:
        if char in word:
            word=word.replace(char,"")
    return word

def repunctuate(pword, replaceword):
    punctuations = '\'!()-[]\{\};:\"\/,<>.?@#$%^&*_~'
    for char in punctuations:
        if char == pword[-1]:
            return replaceword+char
    return replaceword


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
        while len(m) >= 1 and m[-1]=="s":
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
        trimmeasure = measure[0]
        if trimmeasure[-1] == 's':
            trimmeasure = trimmeasure[:-1]
        return str(sum(quantity)).replace(".0","") +" "+ trimmeasure.capitalize()+sstring+" "

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
        if len(m) >= 1 and q != 1.0 and m[-1] != "s":
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

def render_recipe(ingredients, steps, bigsteps,transform = ""):
    newingredients = replace_back_ingredients(bigsteps,ingredients)
    newsteps = replace_back_steps(bigsteps,steps,transform)
    print("***INGREDIENTS***\n")
    for ingredient in newingredients:
        print(ingredient)
    print("** RECIPE STEPS **")
    for step in newsteps:
        print("    "+step+"\n")
    return
