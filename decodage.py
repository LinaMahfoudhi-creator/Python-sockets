
"""
    data_with_checksum : chaîne binaire contenant les données + le checksum
    block_size : taille des blocs (par défaut : 8 bits)

"""
from codage import checksum_calculate

def checksum_decode(data_with_checksum, block_size=3):

    initial_data= data_with_checksum[:len(data_with_checksum)-block_size]
    checksum= data_with_checksum[len(data_with_checksum)-block_size:]
    received_checksum=checksum_calculate(initial_data)
    if received_checksum == checksum:
        return (initial_data,"success")
    else:
        return (initial_data,"error")


#print("Décodage "+checksum_decode("001010011101011101000").__str__())