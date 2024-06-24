import random
import time

max_int=3000000# max int 9223372036854775807

start=time.time()
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def modinv(a, p):
    """Находит обратное по модулю p число для a, используя расширенный алгоритм Евклида"""
    if gcd(a, p) != 1:
        return None  # Обратного элемента не существует, если a и p не взаимно просты

    # Расширенный алгоритм Евклида
    t, new_t = 0, 1
    r, new_r = p, a

    while new_r != 0:
        quotient = r // new_r
        t, new_t = new_t, t - quotient * new_t
        r, new_r = new_r, r - quotient * new_r

    if t < 0:
        t = t + p

    return t

def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def order(a, m):
    order = 1
    result = a
    while result != 1:
        result = (result * a) % m
        order += 1
        if result == a:  # Цикл
            return None
    return order

def generate_keys():
    # Выбор простого числа p
    p = random.randint(1000, max_int)
    while not is_prime(p):
        p = random.randint(1000, max_int)

    g = random.randint(2, p - 2)
    if not is_prime(order(g,p)):
        g = random.randint(2, p - 2)

    # Выбор закрытого ключа x
    x = random.randint(1, p - 2)

    # Вычисление открытого ключа y
    y = pow(g, x, p)

    return (p, g, y), x

def encrypt(public_key, message):
    p, g, y = public_key

    # Выбор случайного k
    k = random.randint(1, p - 2)
    while gcd(k, p - 1) != 1:
        k = random.randint(1, p - 2)

    # Вычисление компонента c1
    c1 = pow(g, k, p)

    # Вычисление компонента c2
    c2 = (message * pow(y, k, p)) % p

    return c1, c2

def decrypt(private_key, public_key,ciphertext):
    p, g, y = public_key
    c1, c2 = ciphertext
    x = private_key

    # Вычисление m
    s = pow(c1, x, p)
    s_inv = modinv(s, p)
    m = (c2 * s_inv) % p

    return m

# Пример использования
public_key, private_key = generate_keys()
message = random.randint(1,public_key[0])  # Исходное сообщение

print("Public Key:", public_key)
print("Private Key:", private_key)
print("Original Message:", message)

ciphertext = encrypt(public_key, message)
print("Encrypted Message:", ciphertext)

decrypted_message = decrypt(private_key, public_key, ciphertext)
print("Decrypted Message:", decrypted_message)
stop=time.time()

print('Время работы в секундах: ',stop-start)
