import random
import string

from django.contrib.auth.models import User

USER_AMOUNT = 30
PASSWORD_LENGTH = 5

username_stem = 'participant'
users = []


def random_string(n):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))


def create_user():
    password = random_string(PASSWORD_LENGTH)
    username = username_stem + str(i)
    User.objects.create(
        username=username,
        password=password
    )
    print("Created user: " + username + ".")
    users.append({
        'username': username,
        'password': password
    })


for i in range(1, USER_AMOUNT + 1, 1):
    create_user()

with open('./user_list.txt', 'w') as outfile:
    for user in users:
        outfile.write(user['username'] + ', ' + user['password'] + '\n')
        print(user['username'], user['password'])
