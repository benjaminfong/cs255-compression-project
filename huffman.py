import os
import sys
import heapq
import json
import struct

class HuffmanNode:
    def __init__(self, byte = None, freq = None, left = None, right = None):
        self.is_leaf = byte is not None
        self.byte = byte
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

    def __le__(self, other):
        return self.freq <= other.freq

    def __gt__(self, other):
        return self.freq > other.freq


def encode(data):

    # get byte frequencies
    frequency = {}
    for byte in data:
        frequency[byte] = frequency.get(byte, 0) + 1

    # create frequency priority queue
    heap = [HuffmanNode(byte, count) for byte, count in frequency.items()]
    heapq.heapify(heap)

    # build huffman tree
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        parent = HuffmanNode(None, left.freq + right.freq, left, right)

        heapq.heappush(heap, parent)

    # create huffman tree and get codes
    huffman_codes = {}
    def get_huffman_codes(node, code):
        if node.is_leaf:
            huffman_codes[node.byte] = code
        else:
            get_huffman_codes(node.left, code + "0")
            get_huffman_codes(node.right, code + "1")
            
 
    get_huffman_codes(heap[0], "")
    
    # create decoder
    decoder = {value: key for key, value in huffman_codes.items()}

    # encode file contents with codes
    bit_string = ""
    for byte in data:
        bit_string += huffman_codes[byte]

    # determine padding needed and add to bit string
    padding = (8 - len(bit_string) % 8) % 8
    bit_string += "0" * padding

    # convert bit string to bytes
    encoded_bytes = bytearray()
    for i in range(0, len(bit_string), 8):
        encoded_bytes.append(int(bit_string[i:i+8], 2))

    # serialize decoder dict to bytes via JSON
    decoder_bytes = json.dumps(decoder).encode("utf-8")

    # return decoder length, decoder, padding length, encoded data
    return struct.pack(">I", len(decoder_bytes)) + decoder_bytes + bytes([padding]) + bytes(encoded_bytes)
    
    
    
def decode(data):
    decoder_len = struct.unpack(">I", data[:4])[0]
    decoder = json.loads(data[4:4 + decoder_len].decode("utf-8"))
    padding = data[4 + decoder_len]
    encoded_bytes = data[5 + decoder_len:]

    # convert encoded bytes to bit string
    bit_string = ""
    for i, byte in enumerate(encoded_bytes):
        bits = format(byte, "08b")
        if i == len(encoded_bytes) - 1 and padding > 0:
            bits = bits[:8 - padding]
        bit_string += bits

    # iterate through the bit string and match against huffman codes
    decoded_data = bytearray()
    current_code = ""
    for bit in bit_string:
        current_code += bit
        if current_code in decoder:
            decoded_data.append(decoder[current_code])
            current_code = ""

    return bytes(decoded_data)

def main():
        # get command line arguments
    if len(sys.argv) != 4 or (sys.argv[3] != "-e" and sys.argv[3] != "-d"):
        print("Please provide the proper command line arguments.")
        print("Usage: python huffman.py <input-file> <output-file> <-e for encode or -d for decode>")
        exit()
    operation = sys.argv[3]
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file, "rb") as file:
        data = file.read()

    if operation == "-e":
        result = encode(data)
    elif operation == "-d":
        result = decode(data)
    else:
        print("Invalid mode")

    with open(output_file, "wb") as file:
        file.write(result)
        
if __name__ == "__main__":
    main()