import os, lz4.frame


def get_references_values():
    source = os.path.join(os.getcwd(), "orl_faces", "subsets", "reference")
    ref_dict = {}
    for dirs in os.listdir(source):
        for file in os.listdir(os.path.join(source, dirs)):
            with open(os.path.join(source, dirs, file), 'rb') as original:
                original_str = original.read()
                if dirs not in ref_dict.keys():
                    ref_dict[dirs] = [(file, original_str)]
                else:
                    ref_dict[dirs].append((file, original_str))
    return ref_dict


def calculate_best_ncd(ref_dict, test_original_str):
    test_compressed_str_size = len(lz4.frame.compress(test_original_str, compression_level=lz4.frame.COMPRESSIONLEVEL_MAX))
    best_ncd = 5
    best_subject = ""
    for subject, reference_set in ref_dict.items():
        ncd = 0
        for reference in reference_set:
            ncd += (len(lz4.frame.compress((b''.join([reference[1], test_original_str])), compression_level=lz4.frame.COMPRESSIONLEVEL_MAX)) -
                    min(test_compressed_str_size, len(lz4.frame.compress((reference[1]), compression_level=lz4.frame.COMPRESSIONLEVEL_MAX)))) / \
                   (max(test_compressed_str_size, len(lz4.frame.compress((reference[1]), compression_level=lz4.frame.COMPRESSIONLEVEL_MAX))))
        ncd = ncd / 3.0
        if best_ncd > ncd:
            best_ncd = ncd
            best_subject = subject
    return best_subject, best_ncd


def test_ncd_similarity(reference_values):
    source = os.path.join(os.getcwd(), "orl_faces", "subsets", "test")
    test_dict = {}
    for dirs in os.listdir(source):
        for file in os.listdir(os.path.join(source, dirs)):
            with open(os.path.join(source, dirs, file), 'rb') as original:
                original_str = original.read()
                subject, best_ncd = calculate_best_ncd(reference_values, original_str)
                if dirs not in test_dict:
                    test_dict[dirs] = {file: (subject, best_ncd)}
                else:
                    test_dict[dirs][file] = (subject, best_ncd)
    return test_dict


def results():
    print("\nFace Recognition with LZ4")
    # dictionary containing the bytes of each file for each subject in the references subset
    reference_values = get_references_values()
    return test_ncd_similarity(reference_values)


if __name__ == '__main__':
    results()