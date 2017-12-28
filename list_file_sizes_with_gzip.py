import os, gzip, shutil, re

def get_references_values():
    source = os.path.join(os.getcwd(), "orl_faces", "subsets","reference")
    ref_dict = {}
    for dirs in os.listdir(source):
        subject = ("Subject {}:".format(re.sub("s", "", dirs)))
        for file in os.listdir(os.path.join(source, dirs)):
            f = ("File {}".format(file))
            with open(os.path.join(source, dirs, file), 'rb') as original:
                original_str = original.read()
                if subject not in ref_dict.keys():
                    ref_dict[subject] = [(f, original_str)]
                else:
                    ref_dict[subject].append((f, original_str))
    return ref_dict

def calculate_best_ncd(ref_dict, test_original_str):
    test_compressed_str_size = len(gzip.compress((test_original_str)))
    best_ncd = 5
    ncd = 0
    subject = ""
    for k, v in ref_dict.items():
        for s in v:
            ncd += (len(gzip.compress((b''.join([s[1], test_original_str])))) -
                    min(test_compressed_str_size, len(gzip.compress((s[1]))))) / \
                   (max(test_compressed_str_size, len(gzip.compress((s[1])))))
        ncd = ncd/3.0
        if(best_ncd > ncd):
            best_ncd = ncd
            subject = k
        ncd = 0
    return subject,best_ncd


def test_ncd_similarity(reference_compressed_values):
    source = os.path.join(os.getcwd(), "orl_faces", "subsets", "test")
    test_dict = {}
    for dirs in os.listdir(source):
        for file in os.listdir(os.path.join(source, dirs)):
            with open(os.path.join(source, dirs, file), 'rb') as original:
                original_str = original.read()
                subject,best_ncd = calculate_best_ncd(reference_compressed_values, original_str)
                img = dirs+file
                test_dict[img] = (subject,best_ncd)
    return test_dict

if __name__ == '__main__':
    reference_compressed_values = get_references_values()    #dictionary containing the bytes of each file for each subject in the references subset
    results = test_ncd_similarity(reference_compressed_values)
    accuracy = 0
    for k,r in results.items():
        print(k+" : "+str(r))
        if k[1:3]==r[0][8:-1]:
            accuracy+=1
    print("Nr of times that got right:"+str(accuracy)+" Accuracy: "+str(accuracy/280.0))