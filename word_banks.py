import requests
from lxml import html
import re
import nltk
from nltk.corpus import wordnet
# nltk.download('wordnet')

# all word banks used in the project

pasta = ['spaghetti', 'penne', 'fettucine', 'angel hair', 'linguine', 'orzo', 'lasagn', 'macaroni', 'rigatoni',
         'ravioli', 'cannelloni', 'tagliatette', 'tortellini', 'pappardelle', 'fusilli', 'bucatini', 'orecchiette',
         'farfalle', 'fregula', 'taglierini', 'manicotti', 'cavatappi', 'cavatelli', 'capellin', 'ziti', 'rotini']
meat = ['chicken', 'beef', 'pork', 'steak', 'fish', 'salmon', 'bass',
        'egg', 'tuna', 'turkey', 'halibut', 'bacon', 'veal', 'duck', 'lamb', 'cod', 'trout',
        'sausage', 'salami']
cheese = ['mozzarella', 'parmesan', 'gorgonzola', 'ricotta', 'ovalini', 'cheddar']

# used in ing_parser.py
measurement_bank = ['teaspoon', 'tablespoon', 'cup', 'lb', 'package', 'pinch', 'sprinkle', 'ounce', 'oz', 'stalk',
                    'whole', 'sprig', 'leaf', 'bottle', 'liter', 'pound', 'can', 'clove', 'head', 'slice', 'medium',"cube","dash","splash","packet","package"]
prep_words = ['chop', 'peel', 'core', 'slice', 'mince', 'crush', 'rinse', 'grate', 'wash', 'beaten', 'dice']


# used in ing_sorter.py
proteins = ['tofu', 'tempeh','lentil', 'chickpea', 'legume','seitan', 'mushroom']
proteins.extend(meat)
# veggies found here: https://www.halfyourplate.ca/fruits-and-veggies/veggies-a-z/
veggies = ['amaranth leaves', 'arrowroot', 'artichoke', 'arugula', 'asparagus', 'bamboo shoots', 'beans', 'beets',
           'belgian endive', 'bitter melon', 'bok choy', 'broadbeans', 'broccoli', 'broccoli rabe', 'brussel sprout',
           'cabbage', 'carrot', 'cassava', 'yuca', 'cauliflower', 'celeriac', 'celery', 'chayote', 'chicory',
           'collards', 'corn', 'crookneck', 'cucumber', 'daikon', 'dandelion', 'edamame', 'soybean', 'eggplant',
           'fennel', 'fiddlehead', 'ginger', 'horseradish', 'jicama', 'kale', 'kohlrabi', 'leeks', 'lettuce',
           'mushroom', 'mustard', 'okra', 'onion', 'parsnip', 'peas', 'green pepper', 'red pepper', 'potato', 'pumpkin',
           'radicchio', 'radish', 'rutabaga', 'salsify', 'oysterplant', 'shallot', 'snow peas', 'sorrel', 'dock',
           'squash', 'spinach', 'chard', 'tomatillo', 'tomato', 'turnip', 'watercress', 'yam', 'zucchini']
# fruits found here: https://www.halfyourplate.ca/fruits-and-veggies/fruits-a-z/
fruits = ['pineapple', 'acerola', 'apple', 'apricots', 'avocado', 'banana', 'blackcurrant', 'cantaloupe', 'carambola', 'cherimoya',
          'cherry', 'cherries', 'clementine', 'coconut', 'date', 'durian', 'feijoa', 'fig', 'grape', 'guava', 'melon',
          'kiwi', 'kumquat', 'lemon', 'lime', 'longan', 'loquat', 'lychee', 'mandarin', 'mango', 'mangosteen',
          'nectarine', 'olive', 'orange', 'papaya', 'peach', 'pear', 'persimmon', 'pitaya', 'pineapple', 'pitanga',
          'plantain', 'plum', 'pomegranate', 'prickly pear', 'prune', 'pummelo', 'quince', 'rhubarb', 'sapodilla',
          'sapote', 'soursop', 'tamarind', 'tangerine', 'fruit', 'berry', 'berries']
# spices found here: https://www.spicejungle.com/list-of-spices
seasonings = ['adobo', 'chile powder', 'chiles', 'paprika', 'allspice', 'flavoring',
              'chile peppers', 'anise', 'annatto', 'arrowroot', 'assam', 'spice blend', 'basil',
              'bay leaves, ground', 'seasoning', 'extract', 'berbere', 'chili', 'chili powder',
              'black fungus', 'cloud ear', 'garlic', 'black pepper', 'peppercorn', 'salt',
              'pekoe', 'mushroom powder', 'rooibos',
              'brown sugar', 'cajun seasoning', 'steak seasoning', 'cane sugar', 'sugar cubes', 'cane syrup',
              'cape cod seasoning', 'caraway',
              'cardamom', 'carom', 'cassia bark', 'cinnamon', 'caster sugar', 'cayenne',
              'celery seed', 'tea', 'chai', 'chervil', 'chiltepin pepper', 'chimichurri',
              'chipotle', 'chive', 'cilantro', 'ceylon', 'ginger', 'clove', 'cocoa', 'coconut chips',
              'coconut sugar', 'spice rub', 'coriander', 'corn husks', 'cream of tartar',
              'cubeb pepper', 'cumin', 'radish seeds', 'dill', 'mushroom blend',
              'fajita seasoning', 'fennel', 'fenugreek', 'mélange', 'melange', 'five spice', 'fleur de sel',
              'herb blend', 'galangal', 'garam masala', 'garlic',
              'grains of paradise', 'melegueta', 'serrano', 'guajillo', 'gumbo', 'habanero', 'harissa',
              'herbes de provence', 'hibiscus', 'hickory', 'honey powder', 'honey', 'horseradish powder',
              'curry powder', 'jasmine pearls', 'jerk seasoning', 'juniper', 'kabsa', 'lime leaves', 'kaffir', 'kukicha',
              'lavender', 'lemon extract', 'lemon juice powder', 'lemon peel', 'lemon zest', 'lemongrass',
              'lime juice powder', 'lime peel', 'lime zest', 'long pepper',
              'mace', 'maple sugar', 'marjoram', 'molasses powder', 'mulling spices', 'mustard powder',
              'mustard seed', 'nameko', 'nigella seeds', 'nutmeg', 'onion powder', 'onion powder', 'oolong', 'orange peel',
              'oregano', 'paella seasoning', 'five-spice', 'parsley',
              'pasilla', 'poppy seeds', 'porcini powder',
              'poultry seasoning', 'pumpkin pie spice', 'quatre épices', 'ras el hanout', 'raspberry powder',
              'chili flakes', 'crystal sugar', 'rosemary', 'rum flavoring',
              'saffron', 'sage', 'salsa verde seasoning', 'sassafras', 'sesame seed', 'togarashi',
              'soy sauce powder', 'sumac', 'vanilla beans', 'tamarind powder', 'tandoori spice',
              'tarragon', 'thyme', 'tomato powder', 'turmeric', 'vadouvan spice',
              'vindaloo curry powder', 'vinegar powder', 'malt', 'wasabi',
              'worcestershire sauce powder', 'zaatar spice', 'sugar', 'mint', 'caper']
media = ['wine', 'oil', 'vinegar', 'butter', 'margarine', 'broth', 'juice', 'sauce', 'marinara']
# grains found here: https://wholegrainscouncil.org/whole-grains-101/whole-grains-z
grains = ['amaranth', 'barley', 'buckwheat', 'bulgur', 'corn', 'einkorn', 'farro', 'emmer', 'fonio', 'freekeh',
          'kamut', 'kañiwa', 'millet', 'oats', 'quinoa', 'rice', 'rye', 'sorghum', 'milo', 'spelt', 'teﬀ', 'triticale',
          'wheat', 'wild rice', 'flour', 'couscous']
dairy = ['milk', 'butter', 'yogurt', 'yoghurt', 'cream', 'whey', 'casein', 'mayonnaise', 'gelato'] + cheese
carbs = ['rice', 'bread', 'couscous', 'cereal', 'pasta', 'ramen', 'udon', 'soba'] + pasta
toppings = ['sauce', 'sprinkle', 'garnish', 'marinara']

not_protein = ['bouillon', 'broth', 'noodle', 'seasoning']
not_seasoning = ['butter']
not_veg = ['sauce','paste', 'oil', 'vinegar', 'cider', 'broth', 'juice']
not_fruit = ['sauce', 'oil', 'vinegar', 'cider', 'juice']
not_carbs = ['sauce', 'seasoning']
not_med = ['milk']

# used in step_parser
toollist = ['dipper', 'brasero', 'fillet knife', 'skillet', 'cheesemelter', 'range', 'processor', 'oven', 'thermometer',
            'opener', ' boiler', 'tamis', 'reamer', 'kyoto box', 'lame', 'tongs', 'pestle and mortar', 'stove',
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

# used in vegetarianify
not_vegetarian = meat

# used in unvegetarianify
replace_with_meat = {'tofu': 'chicken',
                     'tempeh': 'chicken',
                     'lentil': 'chicken',
                     'chickpea': 'chicken',
                     'seitan': 'steak',
                     'mushroom': 'steak'}

# used for cuisine changes.
# if you add something to 'italian' you must also add it to 'sorted_italian in the proper place
cuisines = {
    'sorted_italian': {
        'protein': ['beef', 'prosciutto', 'chicken', 'salami', 'sausage', 'eggplant', 'ground beef'],
        'vegetable': ['tomato', 'zucchini', 'cucumber', 'mushroom', 'broccolini', 'rabe', 'arugula', 'squash', 'potato',
                      'carrot', 'spinach'],
        'seasoning': ['garlic', 'parsley', 'basil', 'rosemary', 'oregano', 'caper', 'sugar', 'lime', 'lemon',
                      'bay leaf', 'salt'],
        'dairy': cheese + ['cream', 'gelato'],
        'media': ['olive oil', 'balsamic vinegar', 'butter', 'marinara'],
        'carb': ['orzo', 'couscous'] + pasta,
        'topping': ['tomato sauce', 'marinara'],
        'fruit': ['grape', 'apple', 'olive', 'peach', 'orange', 'nectarine']
    }
}

for key in cuisines['sorted_italian'].keys():
    cuisines.setdefault('italian', []).extend(cuisines['sorted_italian'][key])

#
# spicy_seas = []
# pungent_seas = []
# sweet_seas = []
#
# for item in seasonings:
#     syns = wordnet.synsets(item)
#     try:
#         meaning = ' '.join([syns[i].definition() for i in range(len(syns))])
#     except:
#         continue
#     print(item,":", meaning)
#     if 'hot' in meaning:
#         spicy_seas.append(item)
#     if 'pungent' in meaning:
#         pungent_seas.append(item)
#     if 'sweet' in meaning:
#         sweet_seas.append(item)
#
# print(spicy_seas)
# print(pungent_seas)
# print(sweet_seas)


# basic food/method descriptions
descriptor_thing = {
    'healthy_method': ['boil', 'steam', 'grill'],
    'unhealthy_methods': ['saute', 'fry', 'roast'],
    'healthy_food': ['chicken'] + veggies,
    'unhealthy_food': ['butter', 'bacon', 'cheese', 'sugar'],
    'light_protein': ['chicken', 'tofu', 'tempeh', 'lentil', 'chickpea'],
    'heavy_protein': ['beef', 'bacon', 'pork', 'steak', 'seitan', 'sausage', 'salami',
                      'turkey'],
    'leafy_veg': ['arugula', 'amaranth leaves', 'artichoke', 'cabbage', 'celery', 'chicory', 'collards', 'dandelion', 'fennel',
                  'kale', 'leeks', 'lettuce', 'mustard', 'radicchio', 'sorrel', 'spinach', 'chard', 'rabe'],
    'root_veg': ['arrowroot', 'beets', 'carrot', 'cassava', 'celeriac', 'chicory', 'daikon', 'dandelion', 'ginger',
                 'horseradish', 'parsnip', 'radish', 'rutabaga', 'salsify', 'sorrel', 'dock', 'chard', 'turnip', 'yam'],
    'spicy_seas': ['chiles', 'chili', 'carom', 'cayenne', 'togarashi', 'peppercorn'],
    'pungent_seas': ['peppercorn', 'cayenne', 'ginger', 'marjoram', 'oregano', 'rosemary', 'saffron', 'caper', 'garlic',
                     'lemon', 'seasoning'],
    'sweet_seas': ['honey', 'sugar'],
    'oil_med': ['olive oil', 'vegetable oil', 'oil', 'butter', 'margarine'],
    'acidic_med': ['marinara', 'wine', 'vinegar', 'balsamic vinegar', 'sauce'],
    'pasta': pasta + ['ramen', 'udon', 'soba'],
    'grain': ['rice', 'barley', 'orzo', 'couscous'],
    'solid_dairy': cheese,
    'cream_dairy': ['milk', 'yogurt', 'yoghurt', 'cream', 'whey', 'casein', 'mayonnaise', 'gelato',
                    'buttermilk', 'butter'],
    'soft_fruit': ['banana', 'peach', 'pear', 'watermelon'],
    'sweet_fruit': ['apple', 'coconut', 'grape'],
    'citrus_fruit': ['pineapple', 'orange', 'nectarine']
}

thing_descriptor = {}
for desc, list in descriptor_thing.items():
    for item in list:
        thing_descriptor.setdefault(item, []).append(desc)
# print("DESCRIPTOR_THING:", descriptor_thing)
# print("THING_DESCRIPTOR", thing_descriptor)


# print([item.lower() for item in fruits])

# url = 'https://wholegrainscouncil.org/whole-grains-101/whole-grains-z'
# search_page = requests.get(url)
# search_data = html.fromstring(search_page.content)
# items = search_data.xpath('//h2[@class="xpandable"]/text()')
# print([re.sub(r'\([^)]*\)', '', item).lower() for item in items])
