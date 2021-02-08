import os

a = os.environ.get("SECRET_TEST_A")
b = os.environ.get("SECRET_TEST_B")

print(a.split())
print(b.split())
