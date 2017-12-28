from gzip_face_recognition import results as gzip_results
from bzip2_face_recognition import results as bzip2_results
from zlib_face_recognition import results as zlib_results
from lzma_face_recognition import results as lzma_results
from time import time as tm


def main():
    compressor_results = [gzip_results, bzip2_results, zlib_results, lzma_results]
    for results in compressor_results:
        start = tm()
        results()
        print("Elapsed Time: {} sec.".format(round(tm() - start, 2)))

if __name__ == '__main__':
    main()
