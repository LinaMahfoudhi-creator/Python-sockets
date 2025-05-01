
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

    #print("Le block ")
    #print(blocks)

    # Additionner les blocs en base 2
    total = 0
    for block in blocks:
        total += int(block, 2) # convertion en binaire
    total= str(bin(total))[2:]
    #print("total avec overflow "+total)

    # determination de l'overflow
    overflowbits = len(total)%block_size
    #print("nombre de bits overflow " + str(overflowbits))
    overflowbit=total[:overflowbits]

    # reduction du total
    total = total[overflowbits:]
    #print("total sans overflow ")
    #print(total)

    # logical shift right de l'overflow
    #print("le overflow bit "+overflowbit)
    while len(overflowbit)!=block_size:
        overflowbit = '0' + overflowbit
    #print(overflowbit)

    #ajout du bit d'overflow
    resultat = int(overflowbit,2) + int(total,2)
    resultat = str(bin(resultat))[2:]
    #print("resultat final "+resultat)

    checksum = ''.join('0' if bit == '1' else '1' for bit in resultat)
    #print("checksum final "+checksum)
    return checksum

def checksum_encode(data, block_size=3):

    # Compléter à un multiple de block_size
    while len(data) % block_size != 0:
        data = '0' + data

    #print(data)
    checksum=checksum_calculate(data)
    #print(data+checksum)
    return data+checksum

print(checksum_encode("10010011101011101"))
