import os
import fnmatch
import time

pattern = "??.??.????_??.??.??_EMGAufzeichnung_Lable_?.txt"

def main():
    print("Fusion...")
    
    files = fnmatch.filter(os.listdir(os.getcwd()), pattern)

    if(len(files) == 0):
        print("ERROR! No matching files found!")
        print("Pattern: " + pattern)
        input("Press Enter to continue...")
        return

    date = time.strftime("%d.%m.%Y_%H.%M.%S")
    output_name = date + "_EMGAufzeichnung_Complete.csv"
    output_file = open(output_name, "a+")

    print(f"File 0/{len(files)}")
    for file in files:
        print(f"File {files.index(file)+1}/{len(files)}")
        f = open(file, "r")
        output_file.write((f.read()).replace(',', ';'))
        f.close()
    output_file.close()
    input("Done! Press Enter to continue...")

main()