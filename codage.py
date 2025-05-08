
"""
    data : chaîne binaire (ex: "110101100111...")
    block_size : taille des blocs à additionner (par défaut : 8 bits)
    
"""

def checksum_calculate(data, block_size=3):
    # Diviser en blocs avec une boucle
    blocks = []
    i = 0
    while i < len(data):
        block = data[i:i+block_size]
        blocks.append(block)
        i += block_size

    # Additionner les blocs en base 2
    total = 0
    for block in blocks:
        total += int(block, 2) # convertion en binaire
    total= str(bin(total))[2:]

    # determination de l'overflow
    overflowbits = len(total)%block_size
    overflowbit=total[:overflowbits]

    # total sans overflow
    total = total[overflowbits:]
    # logical shift right de l'overflow
    while len(overflowbit)!=block_size:
        overflowbit = '0' + overflowbit

    #ajout du bit d'overflow
    resultat = int(overflowbit,2) + int(total,2)
    resultat = str(bin(resultat))[2:]

    checksum = ''.join('0' if bit == '1' else '1' for bit in resultat)
    return checksum

def checksum_encode(data, block_size=3):

    # Compléter à un multiple de block_size
    while len(data) % block_size != 0:
        data = "0" + data

    checksum=checksum_calculate(data)
    return data+checksum

#print("résultat final "+checksum_encode("11010011101011101"))
