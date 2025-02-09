import random
import string

def generate_code(length=4):
    caracteres = string.ascii_letters + string.digits 
    return ''.join(random.choice(caracteres) for _ in range(length))

def generate_name(length=4):
    return 'tarea-' + generate_code(length)