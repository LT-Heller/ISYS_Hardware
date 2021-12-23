import os
import sys, getopt
import random

def get_max(data, num):
    max = list()
    index = 0
    for value in data:
        if len(max) < num:
            max.append((value, index))
            if len(max) == num:
                max.sort(key=lambda tup: tup[0])
        elif value > max[0][0]:
            max[0] = (value, index)
            max.sort(key=lambda tup: tup[0])
        index += 1
    return max

def get_min(data, num):
    min = list()
    index = 0
    for value in data:
        if len(min) < num:
            #print(min)
            min.append((value, index))
            if len(min) == num:
                min.sort(key=lambda tup: tup[0], reverse=True)
                #print(min)
        elif value < min[0][0]:
            min[0] = (value, index)
            min.sort(key=lambda tup: tup[0], reverse=True)
            #print(min)
        index += 1
    return min

def main(argv):
    inputfile = ""
    filter_size = 50
    graph = False
    try:
        opts, args = getopt.getopt(argv,"hi:f:",["input=","filter_size="])
    except getopt.GetoptError:
        print("peakremover.py -i <inputfile.csv> [-f <filter_size>]")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h' or len(argv) == 0:
            print("peakremover.py -i <inputfile.csv> [-f <filter_size>]")
            sys.exit()
        elif opt in ("-i", "--input"):
            inputfile = arg
        elif opt in ("-f", "--filter"):
            filter_size = int(arg)
    if(type(filter_size) != int or filter_size <= 0):
        print("Filtersize must be an integer > 0!")
        sys.exit()
    if(inputfile.split('.')[-1] != "csv"):
        print("Inputfiles must end with '.csv'!")
        sys.exit()

    # Test
    print("Testing outputfile...")
    outputfile = inputfile.rsplit('.',1)[-2]+"_Peaks_Removed.csv"
    try:
        output = open(outputfile, "w")
    except IOError:
        print("Outputfile error! Permission denied?")
        sys.exit()

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