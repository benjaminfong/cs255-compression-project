import sys
MAX_CODE = 65535 

def encode(data):
    if len(data) == 0:
        print("input file is empty")
        return

    # create initial dictionary with 0x00 - 0xff as keys (bytes) and 0 - 256 (corresponding codes) as values
    dictionary = {}
    for i in range(256):
        dictionary[bytes([i])] = i

    next_code = 256
    cur_sequence = bytes([data[0]])
    codes = []

    # iterate through each byte of data
    for i in range(1, len(data)):
        cur_byte = bytes([data[i]])

        # if the current sequence concated with the current byte is in dictionary already, add the next character and loop again
        if cur_sequence + cur_byte in dictionary:
            cur_sequence += cur_byte
            continue
        # if its not in the dictionary, then output the code of the current sequence, and create new entry in dictionary of cur_sequence + cur_byte
        else:
            codes.append(dictionary[cur_sequence])

            # only keep adding new entries if less than MAX_CODE
            if next_code <= MAX_CODE:
                dictionary[cur_sequence + cur_byte] = next_code
                next_code += 1
            
            cur_sequence = cur_byte
    
    # add the last code
    codes.append(dictionary[cur_sequence])

    #print(codes)

    encoded_bytes = b"".join(code.to_bytes(2, "big") for code in codes)
    return encoded_bytes
    

def decode(data):
    if len(data) == 0:
        print("input file is empty")
        return

    # each code is 2 bytes, so input length must be even
    if len(data) % 2 != 0:
        print("Compressed data length is invalid for 2-byte codes.")
        exit()

    # convert each code from 2 bytes to int
    codes = []
    for i in range(0, len(data), 2):
        code = int.from_bytes(data[i:i+2], "big")
        codes.append(code)
    
    #print(codes)

    # same dictionary intially as encode with keys and values swapped
    dictionary = {}
    for i in range(256):
        dictionary[i] = bytes([i])

    next_code = 256
    prev = dictionary[codes[0]]
    decoded = [prev]

    # traverse through codes
    for i in range(1, len(codes)):
        # if the code is found then just decode it (get value from dictionary)
        if codes[i] in dictionary:
            entry = dictionary[codes[i]]
        # if it isn't found, then append first character of previous code to current
        else:
            entry = prev + prev[:1]
        
        # append to decoded result
        decoded.append(entry)

        if next_code <= MAX_CODE:
            # add new dictionary entry previous string + first char of entry
            dictionary[next_code] = prev + entry[:1]
            next_code += 1

        # update previous to be the current entry
        prev = entry
    
    return b"".join(decoded)



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