from sklearn.metrics import confusion_matrix, classification_report

from time import time as tm
import re
import os
import matplotlib.pyplot as plt
import numpy as np
import warnings

warnings.filterwarnings("ignore")


def reference_images(reference):
    name = ""
    for ref in reference:
        name += re.sub(".pgm", "", ref) + "_"
    return name


def perform_testing(compressors, reference_subsets):
    f = open(os.path.join(os.getcwd(), "results", "metrics", "metrics_NCD.txt"), "w")
    for reference in reference_subsets:
        subset = reference_images(reference)
        print("Using images {}as reference set.\n".format(re.sub("_", ".pgm ", subset)))
        for results in compressors:
            comp_name = results.__name__
            accuracy = 0
            start = tm()
            true_case, pred_case = [], []
            for subject, test_files in results(reference).items():
                for test_file, result in test_files.items():
                    if subject == result[0]:
                        accuracy += 1
                    true_case.append(subject)
                    pred_case.append(result[0])
            print("\tSuccessful identifications: {}, Accuracy: {}%".format(accuracy, round(accuracy / 280 * 100, 1)))
            print("\tElapsed Time: {} sec.\n".format(round(tm() - start, 2)))

            x = range(0, 40, 1)
            metrics = classification_report(true_case, pred_case, target_names=["Subject " + str(i + 1) for i in x])
            conf_matrix = confusion_matrix(true_case, pred_case)
            conf_matrix = conf_matrix.astype('float') / conf_matrix.sum(axis=1)[:, np.newaxis]
            plt.imshow(conf_matrix, cmap='binary', interpolation='None')
            plt.colorbar()
            plt.step(x, x)
            plt.ylabel("Actual")
            plt.xlabel("Predicted")

            if not os.path.exists(os.path.join(os.getcwd(), "results", "conf_matrix", subset + "results")):
                os.makedirs(os.path.join(os.getcwd(), "results", "conf_matrix", subset + "results"))
            if not os.path.exists(os.path.join(os.getcwd(), "results", "metrics")):
                os.makedirs(os.path.join(os.getcwd(), "results", "metrics"))

            plt.savefig(os.path.join(os.getcwd(), "results", "conf_matrix", subset + "results",
                                     comp_name + "_" + subset + "confusion_matrix.png"))
            f.write("\n{} metrics {}:\n\n".format(comp_name, "with images {}as reference set".format(
                re.sub("_", ".pgm ", subset))))
            f.write(metrics)
            plt.clf()
    f.close()
    print("Confusion matrices can be found under {} folder.".format(os.path.join(os.getcwd(), "results", "conf_matrix")))
    print("All metrics can be found in metrics_NCD.txt under {}".format(os.path.join(os.getcwd(), "results", "metrics")))
