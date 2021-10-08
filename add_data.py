from mai.database import db, User, Goods

try:
    db.create_all()
except:
    pass
if User.query.filter_by(username='admin@example.com').first() is None:
    u = User('admin@example.com', '123456', '')
    db.session.add(u)
    db.session.commit()

from faker import Faker

fake = Faker(locale='zh_CN')

for i in range(10):
    user = User(username=fake.ascii_email(), password=fake.postcode(),
                address=fake.address())
    db.session.add(user)
db.session.commit()

for i in range(20):
    goods = Goods()
    goods.name = fake.word()
    goods.address = fake.address()
    goods.no_bid = True
    goods.description = fake.paragraph()
    goods.original_price = fake.random_int()
    goods.lowest_price = goods.original_price * 0.1
    goods.highest_price = goods.original_price * 0.8
    goods.expired_date = fake.future_date()
    goods.pub_date = fake.future_datetime()
    goods.photo1 = goods.photo2 = goods.photo3 = ''
    goods.user_id = fake.random_digit()
    db.session.add(goods)
db.session.commit()
