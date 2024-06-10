from contextlib import closing
from base import Base, SessionLocal, User, engine

print("Create all tables")
Base.metadata.create_all(bind=engine)

users = [
     User(login='pavel', email='a@gmail.com'),
     User(login='yura', email='b@gmail.com')
]

print("Create users:")
with closing(SessionLocal()) as session:
    for user in users:
        if session.query(User.id).filter_by(email=user.email).first():
            print(f"- {user.email} exists")
        else:
            session.add(user)
            session.commit()
            print(f"- {user.email} added")
