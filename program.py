from compressor_results import full_test
import re

def print_info(reference):
    print("\nFull testing: Tests all 6 available compression algorithms with 10 different reference subsets.\n"
          "\tMay take around 12 - 13 hours to finish all tests.\n\n"
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


def test_compression_algorithm_option():
    print("Choose a compression algorithm.")
    algorithms = "1 - BROTLI.\n" \
          "2 - BZIP2.\n" \
          "3 - GZIP.\n" \
          "4 - LZ4.\n" \
          "5 - LZMA.\n" \
          "6 - ZLIB.\n"

    op = ""
    while op not in ("1", "2", "3", "4", "5", "6"):
        print(algorithms)
        op = input("Option: ")
        if op.lower() not in ("1", "2", "3", "4", "5", "6"):
            print("\tInvalid Option.\n")

    return op


def test_reference_subset_option(reference):
    print("Choose a reference subset.")
    i = 0
    choose = ""
    for ref_set in reference:
        i += 1
        ref = ""
        for image in ref_set:
            ref += " " + re.sub(".pgm", " ", image)
        choose += "{} -{} subset\n".format(i, ref)
    op = ""
    while op not in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10"):
        print(choose)
        op = input("Option: ")
        if op.lower() not in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10"):
            print("\tInvalid Option.\n")

    return reference[int(op) - 1]


def test_compression_algorithm_individually_option(reference):
    algorithm = test_compression_algorithm_option()
    ref = test_reference_subset_option(reference)

    return algorithm, ref



def main():
    print("Face identification using compression algorithms.")
    menu = "Choose what test to run.\n" \
           "1 - Full testing.\n" \
           "2 - Testing by compression algorithm.\n" \
           "3 - Testing by reference subset.\n" \
           "4 - Test a compression algorithm individually.\n" \
           "\ninfo - display information about the tests, compression algorithms available and reference subsets used.\n"

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
        #full_test()
        pass
    elif op == "2":
        algorithm_option = test_compression_algorithm_option()
        # test_compression_algorithm(reference, algorithm_option)
    elif op == "3":
        reference = test_reference_subset_option(reference_subsets)
        #test_reference_subset(reference)
    elif op == "4":
        algorithm_option, reference = test_compression_algorithm_individually_option(reference_subsets)
        #test_compression_algorithm_individually_option(algorithm_option, reference)



if __name__ == '__main__':
    main()
