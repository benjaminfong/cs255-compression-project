import os
import sys
import time
import pandas as pd

import huffman
import LZW
import run_length

# directory with test cases
TEST_DIR = "./test_cases"


ALGORITHMS = {
    "Run-Length": run_length,
    "Huffman": huffman,
    "LZW": LZW,
}

# test compression 
def test_compress(filepath, algorithm):
    with open(filepath, "rb") as f:
        data = f.read()

    # test encoding 
    t0 = time.perf_counter()
    encoded = algorithm.encode(data)
    encoded_size = len(encoded)
    encoding_time = time.perf_counter() - t0


    # test decoding 
    t0 = time.perf_counter()
    decoded = algorithm.decode(encoded)
    decoding_time = time.perf_counter() - t0

    return encoding_time, decoding_time, encoded_size, data == decoded


# run tests on test directory
def run_tests():
    # get all files in test directory
    files = []
    for dirpath, _, filenames in os.walk(TEST_DIR):
        for fname in filenames:
            if fname.startswith("."):
                continue
            files.append(os.path.join(dirpath, fname))
    files.sort()

    if not files:
        return


    results = []
    for filepath in files:
        filename = filepath.split("/")[-1]
        original_size = os.path.getsize(filepath)

        # test each algorithm
        for algorithm_name, algorithm in ALGORITHMS.items():
            print(f"Testing {algorithm_name} on {filename}")

            # test compression and calculate size reduction
            encoding_time, decoding_time, encoded_size, success = test_compress(filepath, algorithm)
            reduction = 1 - (encoded_size / original_size)

            results.append({
                "file": filename,
                "algorithm": algorithm_name,
                "original_bytes": original_size,
                "encoded_bytes": encoded_size,
                "size_reduction": round(reduction, 2),
                "encode_ms": round(encoding_time * 1000, 2),
                "decode_ms": round(decoding_time * 1000, 2),
                "data_matches_decoded": success,
            })

    # save results
    df = pd.DataFrame(results)
    df.to_csv("results.csv", index=False)

    return df


if __name__ == "__main__":
    run_tests()
