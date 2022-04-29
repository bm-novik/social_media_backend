# the following 4 lines setup and initialize Django app with your default app settings
# after calling these lines you can actually access DB using Django Models

import os
from datetime import datetime
from pprint import pprint

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

import django

django.setup()

from post.models import ImagePost

# 31 words
lis = ['warm', 'first', 'lewd', 'sweet', 'ruthless', 'flawless', 'loud', 'efficacious', 'weak', 'romantic', 'damaging',
       'sore', 'certain', 'subdued', 'juicy', 'mighty', 'grandiose', 'attractive', 'bad', 'elderly', 'aquatic', 'funny',
       'absorbed', 'green', 'penitent', 'vigorous', 'telling', 'simplistic', 'unique', 'hallowed', 'snobbish', ]

# 31 words
lis2 = ['underarm', 'grandstand', 'turnaround', 'blacktop', 'foremost', 'comeback', 'upside', 'ballroom', 'peppermint',
        'starfish', 'sheepskin', 'timeshare', 'teaspoon', 'butterball', 'tapeworm', 'crosswalk', 'itself', 'textbook',
        'uplink', 'throwback', 'background', 'headache', 'comeback', 'dishcloth', 'cardboard', 'railway', 'uptime',
        'candlelight', 'whitefish', 'upland', 'upstart', ]

# 31 words
list3 = ['sympathy', 'volume', 'mixture', 'conclusion', 'bathroom', 'wedding', 'power', 'examination', 'family',
         'studio', 'platform', 'customer', 'attitude', 'buyer', 'payment', 'year', 'version', 'temperature', 'instance',
         'historian', 'medicine', 'excitement', 'people', 'inspector', 'ratio', 'shirt', 'communication', 'college',
         'moment', 'direction', 'recording']

# 35 words
list4 = ['growth', 'night', 'revolution', 'opportunity', 'city', 'bonus', 'inspection', 'recipe', 'area', 'tea', 'loss',
         'owner', 'decision', 'variety', 'employee', 'percentage', 'meal', 'uncle', 'way', 'indication', 'article',
         'cabinet', 'tongue', 'interaction', 'wealth', 'affair', 'championship', 'sympathy', 'instruction', 'success',
         'energy']

# 34 words
list5 = ['storage', 'truth', 'inspection', 'reputation', 'preference', 'theory', 'cookie', 'nation', 'efficiency',
         'highway', 'requirement', 'competition', 'intention', 'student', 'way', 'signature', 'perception', 'context',
         'wife', 'analysis', 'media', 'depression', 'piano', 'clothes', 'assignment', 'historian', 'singer',
         'recording', 'aspect', 'selection', 'union', 'committee', 'marketing', 'proposal'
         ]

# 33 words
list6 = ['resource', 'speech', 'variety', 'criticism', 'cancer', 'competition', 'science', 'tradition', 'setting',
         'conclusion', 'oven', 'improvement', 'guitar', 'resolution', 'passenger', 'owner', 'goal', 'grocery',
         'customer', 'entertainment', 'solution', 'agreement', 'fortune', 'guest', 'audience', 'mud', 'historian',
         'statement', 'skill', 'device', 'understanding', 'effort', 'population'
         ]

os.chdir(r'C:\Users\buzzn\OneDrive\Desktop\pic\b')

pprint(os.getcwd())

for i, f in enumerate(os.listdir()):
    # print(f)
    ImagePost(content=f'{list3[i]}',
              image=f'posts/2022-04-28/{f}',
              like_count=0,
              comment_count=0,
              author_id=7,
              date_created=datetime.now(),
              is_active=True,
              updated_at=datetime.now()
              ).save()
