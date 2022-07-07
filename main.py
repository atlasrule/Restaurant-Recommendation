#!/usr/bin/env python
# coding: utf-8


from similar_restaurants import similar_restaurants
import platform
from os import system
from string import capwords


user_criteria = ['?','?','?','?','?','?','?']
n_restaurants = 1

with open('restaurants.csv') as f:
    criteria = f.readline()[:-1]

criteria = criteria.replace('_', ' ')
criteria = criteria.split(',')
criteria = criteria[1:]
criteria = [capwords(c) for c in criteria]
print(criteria)


while True:
    restart = False

    if platform.system() == 'Windows':
        system('cls')
    else:
        system('clear')

    print("\n  Restaurant Recommendations\n\nEnter your criteria (0-10),\nput question mark for don't cares,\nrestart to reset input loop, exit to end program.\n" )

    n_restaurants = int(input('How many restaurants should be listed? (k): '))

    for index, c in enumerate(criteria):
        inp = input(c+':')

        if inp == 'restart':
            restart = True
            break

        if inp == 'exit':
            exit()

        try:
            if inp != '?':
                inp = int(inp)

        except ValueError:
            restart = True
            break

        user_criteria[index] = inp

    if not restart:
        break


cosine_similars = similar_restaurants(n_restaurants=n_restaurants, input_columns=user_criteria, similarity_metric='cosine')

pearson_similars = similar_restaurants(n_restaurants=n_restaurants, input_columns=user_criteria, similarity_metric='pearson')

print('\n', '_'*64, '\n', sep='')
for cosine_similar, pearson_similar in zip(cosine_similars, pearson_similars):
    print('{}         {}'.format(cosine_similar, pearson_similar))
print('\n\n')