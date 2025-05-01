
"""
    data_with_checksum : chaîne binaire contenant les données + le checksum
    block_size : taille des blocs (par défaut : 8 bits)

"""
from codage import checksum_calculate


def checksum_decode(data_with_checksum, block_size=3):

    initial_data= data_with_checksum[:len(data_with_checksum)-block_size]
    #print(initial_data)
    checksum= data_with_checksum[len(data_with_checksum)-block_size:]
    #print(checksum)
    received_checksum=checksum_calculate(initial_data)
    if received_checksum == checksum:
        #print("Checksum valide")
        return initial_data
    else:
        return "error"


print(checksum_decode("010010011101011101001"))
