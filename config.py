import os

CURRENT_DIR = os.path.dirname(__file__)

credentials = ('admin:admin', 'foo:bar')

tasks = [
    {
        'id': 1,
        'title': 'Buy groceries',
        'description': 'Milk, Cheese, Pizza, Fruit, Tylenol',
        'status': 'False'
    },
    {
        'id': 2,
        'title': 'Learn Python',
        'description': 'Need to find a good Python tutorial on the web',
        'status': 'False'
    },
    {
        'id': 3,
        'title': 'Learn Java8',
        'description': 'Need to find a good Java tutorial on the web',
        'status': 'False'
    }
]


