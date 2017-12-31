from compressor_modules.gzip_face_identification import gzip_results
from compressor_modules.bzip2_face_identification import bz2_results
from compressor_modules.lz4_face_identification import lz4_results
from compressor_modules.zlib_face_identification import zlib_results
from compressor_modules.lzma_face_identification import lzma_results
from compressor_modules.brotli_face_identification import brotli_results

from compressor_results import perform_testing

import re


def print_info(reference):
    print("\nFull testing: Tests all 6 available compression algorithms with 10 different reference subsets.\n"
          "\tMay take around 11 hours to finish all tests.\n\n"
          "Testing by compression algorithm: Choose a compression algorithm and test it for all 8 reference subsets.\n"
          "\tRunning time depends on the compression algorithm.\n\n"
          "Testing by reference subset: Choose a reference subset and test it for all available compression algorithms.\n"
          "\tMay take a little more than 1h 15 minutes.\n\n"
          "Test a compression algorithm individually: Allows to choose a compression algorithm and a reference subset individually.\n"
          "\tRunning time depends on the compression algorithm.\n\n"
          "Available compression algorithms:\n"
          "\tBROTLI - Takes around 50 minutes to finish a reference subset test.\n"
          "\tBZIP2  - Takes around 3-4 minutes.\n"
          "\tGZIP   - Takes around 40 seconds.\n"
          "\tLZ4    - Takes around 20 seconds.\n"
          "\tLZMA   - Takes around 20 minutes.\n"
          "\tZLIB   - Takes around 35 seconds.\n\n"
          "Available reference subsets:\n")
    for ref_set in reference:
        ref = ""
        for image in ref_set:
            ref += " " + re.sub(".pgm", " ", image)
        print("\tImages {}".format(ref))
    print()


def test_compression_algorithm_option(reference, individual=False):
    print("Choose a compression algorithm.")
    algorithms = "1 - BROTLI.\n" \
                 "2 - BZIP2.\n" \
                 "3 - GZIP.\n" \
                 "4 - LZ4.\n" \
                 "5 - LZMA.\n" \
                 "6 - ZLIB.\n"

    algorithm = ""
    while algorithm not in ("1", "2", "3", "4", "5", "6"):
        print(algorithms)
        algorithm = input("Option: ")
        if algorithm.lower() not in ("1", "2", "3", "4", "5", "6"):
            print("\tInvalid Option.\n")

    compression_algorithm = []

    if algorithm == "1":
        compression_algorithm = [brotli_results]
        print("(May take around 50 minutes to finish testing for a reference subset)\n")
    elif algorithm == "2":
        compression_algorithm = [bz2_results]
        print("(May take around 3-4 minutes to finish testing for a reference subset)\n")
    elif algorithm == "3":
        compression_algorithm = [gzip_results]
        print("(May take around 40 seconds to finish testing for a reference subset)\n")
    elif algorithm == "4":
        compression_algorithm = [lz4_results]
        print("(May take around 20 seconds to finish testing for a reference subset)\n")
    elif algorithm == "5":
        compression_algorithm = [lzma_results]
        print("(May take around 20 minutes to finish testing for a reference subset)\n")
    elif algorithm == "6":
        compression_algorithm = [zlib_results]
        print("(May take around 35 seconds to finish testing for a reference subset)\n")

    if individual:
        return compression_algorithm

    perform_testing(compression_algorithm, reference)


def test_reference_subset_option(compressors, reference, individual=False):
    print("Choose a reference subset.")
    i = 0
    choose = ""
    for ref_set in reference:
        i += 1
        ref = ""
        for image in ref_set:
            ref += " " + re.sub(".pgm", " ", image)
        choose += "{} -{} subset\n".format(i, ref)
    choose += "{} - Choose your own subset (3 images).\n".format(i + 1)
    op = ""
    while op not in ("1", "2", "3", "4", "5", "6", "7", "8", "9"):
        print(choose)
        op = input("Option: ")
        if op.lower() not in ("1", "2", "3", "4", "5", "6", "7", "8", "9"):
            print("\tInvalid Option.\n")

    if op == "9":
        if individual:
            return choose_own_subset(compressors, individual)
        choose_own_subset(compressors, individual)
    else:
        if individual:
            return [reference[int(op) - 1]]
        perform_testing(compressors, [reference[int(op) - 1]])


def choose_own_subset(compressors, individual=False):
    images = ["01.pgm", "02.pgm", "03.pgm", "04.pgm", "05.pgm", "06.pgm", "07.pgm", "08.pgm", "09.pgm", "10.pgm"]
    subset = []
    options = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    while len(subset) < 3:
        print("\nChoose image to add to reference subset.")
        i = 0
        for img in images:
            i += 1
            print("\t{} - {}".format(i, img))
        op = input("Option: ")
        if op.lower() not in options:
            print("\tInvalid Option.")
        else:
            subset.append(images[int(op) - 1])
            images.remove(images[int(op) - 1])
            options.remove(options[len(options) - 1])

    subset = [tuple(sorted(subset))]
    print("Chosen subset: {}\n".format(subset))

    if individual:
        return subset
    else:
        perform_testing(compressors, subset)


def test_compression_algorithm_individually_option(compressors, reference):
    algorithm = test_compression_algorithm_option(reference, True)
    ref = test_reference_subset_option(compressors, reference, True)
    print(ref)

    perform_testing(algorithm, ref)


def main():
    print("Face identification using compression algorithms.")
    menu = "Choose what test to run.\n" \
           "1 - Full testing.\n" \
           "2 - Testing by compression algorithm.\n" \
           "3 - Testing by reference subset.\n" \
           "4 - Test a compression algorithm individually.\n" \
           "\ninfo - display information about the tests, compression algorithms available and reference subsets used.\n"

    compressors = [gzip_results, bz2_results, zlib_results, lz4_results, lzma_results, brotli_results]
    reference_subsets = [("01.pgm", "02.pgm", "03.pgm"), ("04.pgm", "05.pgm", "06.pgm"), ("07.pgm", "08.pgm", "09.pgm"),
                         ("02.pgm", "04.pgm", "10.pgm"), ("06.pgm", "08.pgm", "10.pgm"), ("01.pgm", "03.pgm", "05.pgm"),
                         ("01.pgm", "07.pgm", "09.pgm"), ("02.pgm", "05.pgm", "07.pgm")]
    op = ""

    while op.lower() not in ("1", "2", "3", "4"):
        print(menu)
        op = input("Option: ")
        if op.lower() not in ("1", "2", "3", "4", "info"):
            print("\tInvalid Option.\n")
        if op.lower() == "info":
            print_info(reference_subsets)

    if op == "1":
        print("Performing Full testing.\n(May take around 11 hours to finish all tests)\n")
        perform_testing(compressors, reference_subsets)
    elif op == "2":
        print("Performing testing by compression algorithm.")
        test_compression_algorithm_option(reference_subsets)
    elif op == "3":
        print("Performing testing by reference subset.")
        test_reference_subset_option(compressors, reference_subsets)
    elif op == "4":
        print("Performing testing for a compression algorithm individually.")
        test_compression_algorithm_individually_option(compressors, reference_subsets)


if __name__ == '__main__':
    main()
