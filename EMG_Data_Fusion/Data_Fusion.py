import os
import sys
import fnmatch
import time

data_path = f".{os.sep}data{os.sep}Test"
pattern = "??.??.????_??.??.??_EMGAufzeichnung_Lable_?.txt"

def main():
    print("Fusion...")
    os.chdir(data_path)

    date = time.strftime("%d.%m.%Y_%H.%M.%S")
    output_name = date + "_EMGAufzeichnung_Complete.csv"
    output_file = open(output_name, "a+")
    
    files = fnmatch.filter(os.listdir(os.getcwd()), pattern)
    print(f"File 0/{len(files)}")
    for file in files:
        print(f"File {files.index(file)+1}/{len(files)}")
        f = open(file, "r")
        output_file.write((f.read() + "\n").replace(',', ';'))
        f.close()
    output_file.close()
    print("Done!")