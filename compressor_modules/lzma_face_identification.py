import os, lzma


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
    test_compressed_str_size = len(lzma.compress(test_original_str))
    best_ncd = 5
    best_subject = ""
    for subject, reference_set in ref_dict.items():
        ncd = 0
        for reference in reference_set:
            ncd += (len(lzma.compress((b''.join([reference[1], test_original_str])))) -
                    min(test_compressed_str_size, len(lzma.compress((reference[1]))))) / \
                   (max(test_compressed_str_size, len(lzma.compress((reference[1])))))
        avg_ncd = ncd / len(reference_set)
        if best_ncd > avg_ncd:
            best_ncd = avg_ncd
            best_subject = subject
    return best_subject, best_ncd


def test_ncd_similarity(reference_values):
    source = os.path.join(os.getcwd(), "orl_faces", "subsets", "test")
    test_dict = {}
    for dirs in os.listdir(source):
        for file in os.listdir(os.path.join(source, dirs)):
            with open(os.path.join(source, dirs, file), 'rb') as original:
                original_str = original.read()
                best_subject, best_ncd = calculate_best_ncd(reference_values, original_str)
                if dirs not in test_dict:
                    test_dict[dirs] = {file: (best_subject, best_ncd)}
                else:
                    test_dict[dirs][file] = (best_subject, best_ncd)
    return test_dict


def lzma_results():
    print("\nFace Identification with LZMA")
    # dictionary containing the bytes of each file for each subject in the references subset
    reference_values = get_references_values()
    return test_ncd_similarity(reference_values)


if __name__ == '__main__':
    lzma_results()
