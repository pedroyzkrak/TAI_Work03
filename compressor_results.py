from compressor_modules.gzip_face_identification import gzip_results
from compressor_modules.bzip2_face_identification import bz2_results
from compressor_modules.zlib_face_identification import zlib_results
from compressor_modules.lzma_face_identification import lzma_results
from compressor_modules.lz4_face_identification import lz4_results
from compressor_modules.brotli_face_identification import brotli_results

from sklearn.metrics import confusion_matrix, classification_report

from time import time as tm
import re
import os
import matplotlib.pyplot as plt
import numpy as np
import warnings

warnings.filterwarnings("ignore")


def main():
    compressor_results = [gzip_results, bz2_results, zlib_results, lz4_results, lzma_results, brotli_results]
    file_path = os.path.join(os.getcwd(), "results", "metrics", "metrics_NCD.txt")
    f = open(file_path, "w")
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

        x = range(0, 40, 1)
        metrics = classification_report(true_case, pred_case, target_names=["Subject " + str(i + 1) for i in x])
        conf_matrix = confusion_matrix(true_case, pred_case)
        conf_matrix = conf_matrix.astype('float') / conf_matrix.sum(axis=1)[:, np.newaxis]
        plt.imshow(conf_matrix, cmap='binary', interpolation='None')
        plt.colorbar()
        plt.step(x, x)
        plt.ylabel("Actual")
        plt.xlabel("Predicted")

        if not os.path.exists(os.path.join(os.getcwd(), "results", "conf_matrix")):
            os.makedirs(os.path.join(os.getcwd(), "results", "conf_matrix"))
        if not os.path.exists(os.path.join(os.getcwd(), "results", "metrics")):
            os.makedirs(os.path.join(os.getcwd(), "results", "metrics"))
        plt.savefig(os.path.join(os.getcwd(), "results", "conf_matrix", comp_name + "_confusion_matrix.png"))
        f.write("{} metrics:\n\n".format(comp_name))
        f.write(metrics)
        plt.clf()
    f.close()


if __name__ == '__main__':
    main()
