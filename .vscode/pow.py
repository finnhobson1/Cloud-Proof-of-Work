# Python program that finds golden nonces to complete Blockchain Proof-of-Work

import hashlib
import time

max_nonce = 2 ** 32

def proof_of_work(block, difficulty_bits):

    # max number with D leading zeros (binary)
    target = 2 ** (256-difficulty_bits)

    for nonce in range(max_nonce):
        binary_nonce = '{0:b}'.format(nonce)
        block_and_nonce = block + binary_nonce
        #print(block_and_nonce)

        hash_result_1 = hashlib.sha256(block_and_nonce.encode('utf-8')).hexdigest()
        hash_result_2 = hashlib.sha256(hash_result_1.encode('utf-8')).hexdigest()

        if int(hash_result_2, 16) < target:
            print()
            print("Golden Nonce Found!")
            print(f"Golden Nonce = {nonce} (Binary = {binary_nonce})")
            print(f"SHA256-Squared Result (Hex) = {hash_result_2}")
            return


if __name__ == '__main__':
	
    difficulty_bits = int(input("Please enter number of difficulty bits: "))

    print("Hunting for Golden Nonce...")

    data_block = "COMSM0010cloud"
    binary_block = ''.join('{0:08b}'.format(ord(x), 'b') for x in data_block)

    start_time = time.time()

    proof_of_work(binary_block, difficulty_bits)
    
    end_time = time.time()

    elapsed_time = end_time - start_time

    print(f"Discovery Time = {elapsed_time:.3f}s")
    print()