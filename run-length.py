import sys
import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
import tensorflow as tf

def encode(data):
    if len(data) == 0:
        return b""

    encoded_data = bytearray()
    count = 1
    cur_byte = data[0]

    for i in range(1, len(data)):
        # increase count if repeating byte (255 limit since 1 byte can only hold up to 255)
        if data[i] == cur_byte and count < 255:
            count += 1

        # otherwise append to file and reset count
        else:
            encoded_data.append(cur_byte)
            encoded_data.append(count)
            cur_byte = data[i]
            count = 1
    
    # append final character
    encoded_data.append(cur_byte)
    encoded_data.append(count)

    return encoded_data


def decode(data):
    if len(data) == 0:
        return b""
    
    decoded_data = bytearray()

    # traverse through each byte
    for i in range(0, len(data), 2):

        # append the byte the amount of times encoded
        for j in range(0, data[i + 1]):
            decoded_data.append(data[i])

    return decoded_data


def main():
    # get command line arguments
    if len(sys.argv) != 4 or (sys.argv[3] != "-e" and sys.argv[3] != "-d"):
        print("Please provide the proper command line arguments.")
        print("Usage: python run-length.py <input-file> <output-file> <-e for encode or -d for decode>")
        exit()
    operation = sys.argv[3]
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # read in data as bytes
    with open(input_file, "rb") as f:
        data = f.read()

    # encode/decode data
    if operation == "-e":
        result = encode(data)
    elif operation == "-d":
        result = decode(data)


    with open(output_file, "wb") as f:
        f.write(result)


if (__name__ == "__main__"):
    main()