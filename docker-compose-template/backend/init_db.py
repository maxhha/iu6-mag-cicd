from contextlib import closing
from base import Base, SessionLocal, User, engine

Base.metadata.create_all(bind=engine)

users = [
     User(login='pavel', email='a@gmail.com'),
     User(login='yura', email='b@gmail.com')
]

with closing(SessionLocal()) as session:
    for user in users:
        if session.query(User.id).filter_by(email=user.email).first():
            session.add(user)
            session.commit()
