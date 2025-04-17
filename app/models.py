
from datetime import datetime, timedelta, timezone
from hashlib import md5
from app import app, db, login
import jwt

from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash


followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def __repr__(self) -> str:
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode("utf-8")).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Post.query.join(
            followers, followers.c.followed_id == Post.user_id
        ).filter(followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({"reset_password": self.id,
                           "exp": datetime.now(tz=timezone.utc) + timedelta(seconds=expires_in)},
                          app.config["SECRET_KEY"], algorithm="HS256")

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config["SECRET_KEY"], algorithms="HS256")[
                "reset_password"]
        except:           
            return None
        return User.query.get(id)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self) -> str:
        return f'<Post {self.body}>'

class Mobile_c(db.Model):  #table:流動通訊#
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(50))

class Voice_c(db.Model):   #table:語音電話#
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(50))
class Health_care(db.Model):  #table:醫療保健#
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(50))


class Insurance(db.Model):#保險#
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(120))
    

    def __repr__(self) -> str:
        return f'<Insurance {self.GInsurance}>'

class network(db.Model):#網絡安全#
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(120))
    media = db.Column(db.String(120))
    

    def __repr__(self) -> str:
        return f'<network {self.network}>'

class entertainment(db.Model):#娛樂#
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(120))
    

    def __repr__(self) -> str:
        return f'<entertainment {self.entertainment}>'
#jackwkw#
class Gaming(db.Model):#電競#
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(120))
    price = db.Column(db.String(120))

    def __repr__(self) -> str:
        return f'<Gaming {self.Gaming}>'

class travel(db.Model):#外遊#
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(120))
    price = db.Column(db.String(120))

    def __repr__(self) -> str:
        return f'<travel {self.travel}>'

class protucts(db.Model):#server#
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(120))
    price = db.Column(db.String(120))
    store = db.Column(db.String(120))

    def __repr__(self) -> str:
        return f'<protucts {self.protucts}>'
    
class login2(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(120))
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

class sporrt(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(120))
    phone_number = db.Column(db.String(15))

class Courtesy(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(120))
    Courtesy_name = db.Column(db.String(120))
    start_date = db.Column(db.DateTime)  # 使用标准时间类型
    End_date = db.Column(db.DateTime)