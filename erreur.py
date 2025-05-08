import random

def flip_random_bit_with_error(binary_input, error_chance=0.1):
    if isinstance(binary_input, int):
        binary_str = bin(binary_input)[2:]
    else:
        binary_str = binary_input.strip()

    if random.random() < error_chance:
        bits = list(binary_str)
        flip_index = random.randint(0, len(bits) - 1)
        bits[flip_index] = '1' if bits[flip_index] == '0' else '0'
        return ''.join(bits)
    else:
        return binary_str


"""binary = '101101'
for _ in range(10):
    print("Result:", flip_random_bit_with_error(binary))"""
