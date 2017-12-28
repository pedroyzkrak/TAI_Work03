import os, gzip, shutil, re

# compress file
'''
with open(os.path.join(os.getcwd(), "orl_faces", "subsets", "reference", "s01", "01.pgm"), 'rb') as f_in:
    if not os.path.exists(os.path.join(os.getcwd(), "orl_faces", "compressed", "s01")):
        os.makedirs(os.path.join(os.getcwd(), "orl_faces", "compressed", "s01"))
    with gzip.open(os.path.join(os.getcwd(), "orl_faces", "compressed", "s01", "01.pgm.gz"), 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
        # uncompressed file size
        print(os.fstat(f_in.fileno()).st_size)
    compresed = open(os.path.join(os.getcwd(), "orl_faces", "compressed", "s01", "01.pgm.gz"), 'rb')
    print(os.fstat(compresed.fileno()).st_size)
    '''


def main():
    source = os.path.join(os.getcwd(), "orl_faces", "subsets")
    comp = os.path.join(os.getcwd(), "orl_faces", "compressed")

    for subset in os.listdir(source):
        print("\nSubset {}".format(subset.capitalize()))
        for dirs in os.listdir(os.path.join(source, subset)):
            print("\tSubject {}:".format(re.sub("s", "", dirs)))
            for file in os.listdir(os.path.join(source, subset, dirs)):
                print("\t" * 2 + "File {}".format(file))
                with open(os.path.join(source, subset, dirs, file), 'rb') as original:
                    original_size = os.fstat(original.fileno()).st_size
                    path = os.path.join(comp, subset, dirs)
                    if not os.path.exists(path):
                        os.makedirs(path)
                    with gzip.open(os.path.join(path, file + ".gz"), 'wb') as compressed:
                        shutil.copyfileobj(original, compressed)
                    compressed_file = open(os.path.join(path, file + ".gz"), 'rb')
                    compressed_size = os.fstat(compressed_file.fileno()).st_size
                print("\t" * 3 + "Original: {} Bytes\n\t\t\tCompressed: {}".format(original_size, compressed_size))


if __name__ == '__main__':
    main()
