import os, gzip, shutil

# compress file
with open(os.path.join(os.getcwd(), "orl_faces", "s01", "01.pgm"), 'rb') as f_in:
    with gzip.open(os.path.join(os.getcwd(), "orl_faces", "s01", "01.pgm.gz"), 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
        # uncompressed file size
        print(os.fstat(f_in.fileno()).st_size)

# compressed file size 
compresed = gzip.open(os.path.join(os.getcwd(), "orl_faces", "s01", "01.pgm.gz"), 'rb')
print(os.fstat(compresed.fileno()).st_size)