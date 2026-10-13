import json
import random


class DatabaseHelper:
    def __init__(self, db_name):
        self.db_name = db_name
        self.db = json.load(open(self.db_name, encoding="utf-8"))

    def rand_pick(self, query_food_type, rand_seed) -> dict:
        ret = {
            'food_type': None,
            'food_name': None,
            'food_price': None,
        }
        if query_food_type == '都可':
            random.seed(rand_seed)
            choice = random.choice(self.db['rest_menu'])
            ret['food_type'] = choice['food_type_name']
            choice = random.choice(choice['food_type_menu'])
            ret['food_name'] = choice['food_name']
            ret['food_price'] = choice['food_price']

            return ret

        else:
            query_result: dict = self.query(query_food_type)
            random.seed(rand_seed)
            choice = random.choice(query_result['food_type_menu'])
            ret['food_type'] = query_food_type
            ret['food_name'] = choice['food_name']
            ret['food_price'] = choice['food_price']

            return ret

    def query(self, query_food_type=None) -> dict:
        if query_food_type:
            food_type_menu = []
            for food_type in self.db['rest_menu']:
                if food_type['food_type_name'] == query_food_type:
                    for food in food_type['food_type_menu']:
                        food_type_menu.append(food)
                    return {
                        'food_type_name': query_food_type,
                        'food_type_menu': food_type_menu
                    }

        elif query_food_type is None:
            food_type_menu = []
            for food_type in self.db['rest_menu']:
                for food in food_type['food_type_menu']:
                    food_type_menu.append(food)
            return {
                'food_type_name': 'all',
                'food_type_menu': food_type_menu
            }

        else:
            return {'error': 'No query parameters provided'}
