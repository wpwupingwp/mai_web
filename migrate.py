from mai.database import db, User

u = User('test@example.com', '123456', '')
u2 = User('admin@example.com', '123456', '')
db.session.add(u)
db.session.add(u2)
db.session.commit()

