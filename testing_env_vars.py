import os

a = os.environ.get("SECRET_TEST_A")
b = os.environ.get("SECRET_TEST_B")

with open(os.path.join(os.getcwd(), 'testing.txt'), 'w') as f:
    f.write(a)
    f.write('\n')
    f.write(b)
