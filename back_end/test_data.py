import random

from faker import Faker

from back_end.models import db, User, Post


fake = Faker()


def run():
    for i in range(10):
        user = User()
        user.name = fake.name()
        user.set_password("123456")
        user.email = fake.email()
        user.gender = random.choice(["男神", "女神", "保密"])
        db.session.add(user)
        db.session.commit()
        print(f'{user.name} 加入组织！')

    for i in range(30):
        post = Post()
        post.content = fake.text()
        post.author_id = random.randint(1, 9)
        db.session.add(post)
        db.session.commit()
        print(f'{post.author} 发了一段牢骚~')
