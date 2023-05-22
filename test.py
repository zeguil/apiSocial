import random, string

characters = string.ascii_letters + string.digits
cod = ''.join(random.choice(characters) for _ in range(6))

print(cod)