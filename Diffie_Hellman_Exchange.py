docs = '''
# Diffie-Hellman
# The Diffie-Hellman key exchange process establishes a symmetric key system
# This means that his process establishes the SAME key on both parties, without ever sharing the entire key

# Mathematics:
# The Diffie-Hellman approach uses Modular Arithmetic:

# We need TWO "variables" or numbers to be public, that both parties can access(the public will have access as well)
# These numbers will be:
# g - A Small prime number
# n - A VERY large prime number ( 2048 bits? not secure for quantum computers :) )

# Also, computer A and computer B needs to generate their own number
# A < n
# B < n

# Function: g^x mod n
# g^A mod n
# g^B mod n

# Next, the results of "g^A mod n" AND "g^B mod n" are shared to the public

# Finally, the shared results are raised to the party's own secret exponent
# (g^A mod n)^B
# (g^B mod n)^A

# The result of this exponentiation is: 
# g^(AB) mod n
# g^(BA) mod n
# which is the same exact number
'''
print(docs)
