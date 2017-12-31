import os, brotli


def get_references_values(reference):
    source = os.path.join(os.getcwd(), "orl_faces_raw")
    ref_dict = {}
    for dirs in os.listdir(source):
        for file in os.listdir(os.path.join(source, dirs)):
            if file in reference:
                with open(os.path.join(source, dirs, file), 'rb') as original:
                    original_str = original.read()
                    if dirs not in ref_dict.keys():
                        ref_dict[dirs] = [(file, original_str)]
                    else:
                        ref_dict[dirs].append((file, original_str))
    return ref_dict


def calculate_best_ncd(ref_dict, test_original_str):
    test_compressed_str_size = len(brotli.compress(test_original_str))
    best_ncd = 5
    best_subject = ""
    for subject, reference_set in ref_dict.items():
        for reference in reference_set:
            ncd = (len(brotli.compress((b''.join([reference[1], test_original_str])))) -
                    min(test_compressed_str_size, len(brotli.compress((reference[1]))))) / \
                   (max(test_compressed_str_size, len(brotli.compress((reference[1])))))

            if best_ncd > ncd:
                best_ncd = ncd
                best_subject = subject

    return best_subject, best_ncd


def test_ncd_similarity(reference_values, reference):
    source = os.path.join(os.getcwd(), "orl_faces_raw")
    test_dict = {}
    for dirs in os.listdir(source):
        for file in os.listdir(os.path.join(source, dirs)):
            if file not in reference:
                with open(os.path.join(source, dirs, file), 'rb') as original:
                    original_str = original.read()
                    best_subject, best_ncd = calculate_best_ncd(reference_values, original_str)
                    if dirs not in test_dict:
                        test_dict[dirs] = {file: (best_subject, best_ncd)}
                    else:
                        test_dict[dirs][file] = (best_subject, best_ncd)
    return test_dict


def brotli_results(reference):
    print("\nFace Identification with Brotli")
    # dictionary containing the bytes of each file for each subject in the references subset
    reference_values = get_references_values(reference)
    return test_ncd_similarity(reference_values, reference)
