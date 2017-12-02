from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections import defaultdict
import json
import time


class Recipe:
    def __init__(self):
        self.id = None
        self.tags = []
        self.ingredients = []
        self.instructions = []
        self.prep = None
        self.cook = None
        self.ready = None

    def __str__(self):
        string = '{\n'
        # string += '\tid: ' + str(self.id) + '\n'
        string += '\ttags: ' + str(self.tags) + '\n'
        string += '\tingredients: ' + str(self.ingredients) + '\n'
        string += '\tinstructions: ' + str(self.instructions) + '\n'
        string += '\tprep: ' + str(self.prep) + '\n'
        string += '\tcook: ' + str(self.cook) + '\n'
        string += '\tready: ' + str(self.ready) + '\n' + '}'
        return string

    def to_dict(self):
        r = dict()
        r['id'] = self.id
        r['tags'] = self.tags
        r['ingredients'] = self.ingredients
        r['instructions'] = self.instructions
        r['ready'] = self.ready
        return r


def main():
    URLS = open("Recipe_urls.txt").read().splitlines()
    output = open("Recipes.json", 'w')
    recipes = defaultdict(dict)

    for line in URLS:
        r = Recipe()

        # Make soup for this recipe
        line = line.split()
        url = line[0]
        time.sleep(0)
        bytes = urlopen(url).read()
        soup = BeautifulSoup(bytes, 'lxml')

        # Get ID
        id = ''.join(ch for ch in url if ch.isdigit())
        r.id = id

        # Get Tags
        for tag in line[1:]:
            r.tags.append(tag)

        # Get ingredients
        all_ingredients = soup.find_all('ul', 'dropdownwrapper')
        for ingredients in all_ingredients:
            for ingredient in ingredients.find_all('span', 'recipe-ingred_txt added'):
                r.ingredients.append(ingredient.string)

        # Get Instructions
        instructions = soup.find('ol', 'list-numbers recipe-directions__list')
        for instruction in instructions.find_all('span', 'recipe-directions__list--item'):
            r.instructions.append(instruction.string)

        # Get Ready In Time
        times = soup.find_all('li', 'prepTime__item')
        for time_option in times:
            time_type = time_option.find('p', 'prepTime__item--type')
            if time_type and time_type.string == 'Ready In':
                T = time_option.find('time')['datetime'][2:]
                minutes = 0
                if 'D' in T:
                    days = T.partition('Day')
                    minutes += 3600 * int(days[0])
                    T = days[2]
                if 'H' in T:
                    hours = T.partition('H')
                    minutes += 60 * int(hours[0])
                    T = hours[2]
                if 'M' in T:
                    minutes += int(T.partition('M')[0])
                r.ready = minutes
        print(r.to_dict())
        recipes[id] = r.to_dict()

    output.write(json.dumps(recipes, sort_keys=True, indent=3))

if __name__ == '__main__':
    main()