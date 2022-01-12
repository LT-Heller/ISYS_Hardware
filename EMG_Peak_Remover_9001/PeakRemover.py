import os
import sys, getopt
import fnmatch

def main(argv):
    pattern = "??.??.????_??.??.??_EMGAufzeichnung_Lable_?.txt"
    max_offset = 100
    try:
        opts, args = getopt.getopt(argv,"hp:o:",["pattern=", "max_offset="])
    except getopt.GetoptError:
        print("peakremover.py [-p <pattern>] [-o <max_offset>]")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h' or len(argv) == 0:
            print("peakremover.py [-p <pattern>] [-o <max_offset>]")
            sys.exit()
        elif opt in ("-p", "--pattern"):
            pattern = arg
        elif opt in ("-o", "--offset"):
            if type(arg) != int:
                print("Filtersize must be an integer!")
                sys.exit()
            max_offset = abs(int(arg))

    # create output dir
    print("Ceating output directory...")
    path = os.cwd
    try:
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)

    # Test & Read Inputile
    print("Reading inputfile...")
    channel_value = list([] for _ in range(0,4))
    lables = list()
    try:
        with open(inputfile, 'r') as input:
            for values in open(inputfile, 'r').readlines():
                channel_value[0].append(int(values.split(';')[0]))
                channel_value[1].append(int(values.split(';')[1]))
                channel_value[2].append(int(values.split(';')[2]))
                channel_value[3].append(int(values.split(';')[3]))
                lables.append(int(values.split(';')[4]))
    except IOError:
        print("Inputfile error! Does it exist?")
        sys.exit()

    # detect indices for each spike value
    print("Detecting peaks...")
    rows_to_delete = list()
    for channel in channel_value:
        max = get_max(channel, filter_size)
        for value, index in max:
            rows_to_delete.append(index)
        min = get_min(channel, filter_size)
        for value, index in min:
            rows_to_delete.append(index)

    rows_to_delete = list(set(rows_to_delete))   # entferne Duplikate
    rows_to_delete.sort(reverse=True)            # sotiere absteigend

    # delete rows out of input
    print("Removing peaks...")
    for index in rows_to_delete:
        for channel in list(range(0, 4)):
            del channel_value[channel][index]
    
    # write new outputfile
    print("Writing Outputfile...")
    output.truncate()
    for row in range(len(channel_value[0])):
        output.write(f"{channel_value[0][row]};{channel_value[1][row]};{channel_value[2][row]};{channel_value[3][row]};{lables[row]}\n")
    output.close()

    print("Done!")

if __name__ == "__main__":
   main(sys.argv[1:])