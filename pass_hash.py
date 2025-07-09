from passlib.hash import bcrypt

hashed_password = bcrypt.hash("qwerty12345")
print(hashed_password)
