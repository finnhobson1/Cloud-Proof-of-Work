# Python program that finds golden nonces to complete Blockchain Proof-of-Work

import hashlib
import time
import sys


def proof_of_work(data_block, difficulty_bits, number_of_workers, worker_id):

    # max number with D leading zeros (binary)
    target = 2 ** (256-difficulty_bits)
    
    max_nonce = 2 ** 32

    # convert input data block (e.g. "COMSM0010cloud") into binary
    binary_block = ''.join('{0:08b}'.format(ord(x), 'b') for x in data_block)

    for nonce in range(max_nonce):

        # each worker tries different nonces 
        worker_nonce = (nonce * number_of_workers) + worker_id

        # convert nonce to binary
        binary_nonce = '{0:b}'.format(worker_nonce)

        # append nonce to data block
        block_and_nonce = binary_block + binary_nonce

        # hash block-and-nonce, then hash the result (SHA256-Squared)
        hash_result_1 = hashlib.sha256(block_and_nonce.encode('utf-8')).hexdigest()
        hash_result_2 = hashlib.sha256(hash_result_1.encode('utf-8')).hexdigest()

        # check for D leading zeros, complete if found
        if int(hash_result_2, 16) < target:
            print()
            print("Golden Nonce Found!")
            print(f"Golden Nonce = {worker_nonce} (Binary = {binary_nonce})")
            print(f"SHA256-Squared Result (Hex) = {hash_result_2}")
            return


if __name__ == '__main__':
	
    if len(sys.argv) != 5:
        print("ERROR: Invalid Number of Arguments")
    else:
        # assign and format input parameters
        data_block = sys.argv[1]
        difficulty_bits = int(sys.argv[2])
        number_of_workers = int(sys.argv[3])
        worker_id = int(sys.argv[4])

        print(f"This is Worker {worker_id}")

        start_time = time.time()

        proof_of_work(data_block, difficulty_bits, number_of_workers, worker_id)

        end_time = time.time()

        elapsed_time = end_time - start_time

        print(f"Local Discovery Time = {elapsed_time:.3f}s")
        print()