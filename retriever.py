import requests
import sys
from lxml import html

def retrieve_dict():
    print("Please input a url from Recipes.com OR a search term")

    url = input()

    while True:
        try:
            if "http" not in url and not url == "":
                url = 'https://www.allrecipes.com/search/results/?wt=%s&sort=re' % (url.replace(' ', '+'))
                search_page = requests.get(url)
                search_data = html.fromstring(search_page.content)
                url = search_data.xpath('//div[@class="grid-card-image-container"]//a/@href')[0]
                break
            else:
                break
        except:
            print("Not found - please try again")
            url = input()

    #Default to a random recipe if blank, for testing
    if url=="":
        url = 'https://www.allrecipes.com/recipe/229957/slow-cooker-au-jus-pot-roast/'

    #Confirm the url is valid. Will keep asking so long as the url is not valid
    while True:
        try:
            page = requests.get(url)
            if(page.status_code != 200):
                print("url not found, please try again") 
            break
        except:
            print("url not found, please try again")
            url = input()

    
    #final data form
    data = html.fromstring(page.content)

    #Get Title
    try:
        title = data.xpath('/html/body/div[1]/div[2]/div/div[3]/section/div[1]/div/section[2]/h1')[0].text
    except: 
        title = data.xpath('/html/body/div[1]/div/main/div[1]/div[2]/div[1]/div[1]/div[1]/div/h1')[0].text
    #Gather ingredients
    ingredientlist=[]

    #Iterators
    changeu = False
    i,ul = 1,1

    while True:
        #print('/html/body/div[1]/div[2]/div/div[3]/section/section[1]/div[2]/ul[1]/li[' + str(i) + ']/label/span/text()')
        ingredient = data.xpath('/html/body/div[1]/div[2]/div/div[3]/section/section[1]/div[2]/ul['+str(ul)+']/li['+str(i)+']/label/span/text()')
        if ingredient == []:
            ul += 1
            i = 1
            if changeu:
                break
            changeu = True
            continue
        ingredientlist.append(ingredient[0])
        i+=1
        changeu = False
    ingredientlist = ingredientlist[:-1]
    #print("makes it here")
    #handle video sites
    if ingredientlist == []:
        i,ul = 1,1
        while True:
            #print('/html/body/div[1]/div[2]/div/div[3]/section/section[1]/div[2]/ul[1]/li[' + str(i) + ']/label/span/text()')
            ingredient = data.xpath('/html/body/div[1]/div/main/div[1]/div[2]/div[1]/div[2]/div[2]/div[4]/section[1]/fieldset/ul/li['+str(i)+']/label/span/span/text()')
            if ingredient == []:
                # print(i)
                ul += 1
                i = 1
                break
                if changeu:
                    break
                changeu = True
                continue
            ingredientlist.append(ingredient[0].strip().splitlines()[0])
            i+=1
            changeu = False
       

    steplist = []
    changeu = False
    i,ul = 1,1
    while True:
        #print('/html/body/div[1]/div[2]/div/div[3]/section/section[1]/div[2]/ul[1]/li[' + str(i) + ']/label/span/text()')
        step = data.xpath('/html/body/div[1]/div[2]/div/div[3]/section/section[2]/div/div[1]/ol/li['+str(i)+']/span')
        if step == []:
            break
        steplist.append(step[0].text.splitlines()[0])
        i+=1
        changeu = False

    if steplist == []:
        i,ul = 1,1
        while True:
            #print('/html/body/div[1]/div[2]/div/div[3]/section/section[1]/div[2]/ul[1]/li[' + str(i) + ']/label/span/text()')
            step = data.xpath('/html/body/div[1]/div/main/div[1]/div[2]/div[1]/div[2]/div[2]/section[1]/fieldset/ul/li['+str(i)+']/div[1]/p')
            
            if step == []:
                break
            steplist.append(step[0].text.splitlines()[0])
            i+=1
            changeu = False
    ret = {'Name':title,"Ingredients":ingredientlist,"Procedure":steplist}
    return ret