from gzip_face_identification import gzip_results
from bzip2_face_identification import bz2_results
from zlib_face_identification import zlib_results
from lzma_face_identification import lzma_results
from lz4_face_identification import lz4_results
from brotli_face_identification import brotli_results

from sklearn.metrics import confusion_matrix

from time import time as tm
import re, os
import matplotlib.pyplot as plt


def main():
    #compressor_results = [gzip_results, bz2_results, zlib_results, lz4_results, lzma_results, brotli_results]
    compressor_results = [lz4_results]
    for results in compressor_results:
        comp_name = results.__name__
        accuracy = 0
        start = tm()
        true_case, pred_case = [], []
        for subject, test_files in results().items():
            print("Subject {}".format(re.sub("s", "", subject)))
            for test_file, result in test_files.items():
                print("\t{}: Subject {}, NCD: {}".format(test_file, re.sub("s", "", result[0]), result[1]))
                if subject == result[0]:
                    accuracy += 1
                true_case.append(subject)
                pred_case.append(result[0])
        print("Positive Results: {}, Accuracy: {}%".format(accuracy, round(accuracy / 280 * 100, 1)))
        print("Elapsed Time: {} sec.".format(round(tm() - start, 2)))
        conf_matrix = confusion_matrix(true_case, pred_case)
        print(conf_matrix)
        plt.imshow(conf_matrix, cmap='binary', interpolation='None')
        if not os.path.exists(os.path.join(os.getcwd(), "results", "conf_matrix")):
            os.makedirs(os.path.join(os.getcwd(), "results", "conf_matrix"))
        plt.savefig(os.path.join(os.getcwd(), "results", "conf_matrix", comp_name + "_confusion_matrix.png"))

if __name__ == '__main__':
    main()
