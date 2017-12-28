from gzip_face_recognition import results as gzip_results
from bzip2_face_recognition import results as bzip2_results
from zlib_face_recognition import results as zlib_results
from lzma_face_recognition import results as lzma_results
from time import time as tm
import re


def main():
    compressor_results = [gzip_results, bzip2_results, zlib_results, lzma_results]
    for results in compressor_results:
        accuracy = 0
        start = tm()
        for subject, test_files in results().items():
            print("Subject {}".format(re.sub("s", "", subject)))
            for test_file, result in test_files.items():
                print("\t{}: Subject {}, NCD: {}".format(test_file, re.sub("s", "", result[0]), result[1]))
                if subject == result[0]:
                    accuracy += 1
        print("Positive Results: {}, Accuracy: {}%".format(accuracy, round(accuracy / 280 * 100, 1)))
        print("Elapsed Time: {} sec.".format(round(tm() - start, 2)))

if __name__ == '__main__':
    main()
