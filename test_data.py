from app import db, app
from app.models import User, Post


app_context = app.app_context()
app_context.push()
db.drop_all()
db.create_all()

u1 = User(username='john', email='john@example.com')
u2 = User(username='susan', email='susan@example.com')
u1.set_password("P@ssw0rd")
u2.set_password("P@ssw0rd")
db.session.add(u1)
db.session.add(u2)
u1.follow(u2)
u2.follow(u1)

p1 = Post(body='my first post!', author=u1)
p2 = Post(body='my first post!', author=u2)
db.session.add(p1)
db.session.add(p2)

db.session.commit()
