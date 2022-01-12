import os, sys
from shutil import copyfile
from getopt import getopt, GetoptError
from fnmatch import filter as fnmatch
from time import strftime
from statistics import median, mean
import matplotlib.pyplot as plot
from PIL.Image import open as OpenImage

help_string = "peakremover.py [-p <pattern>] [-o <max_offset> / -u <upper_offset> -l <lower_offset>]\n"

programm_description = f"""
{100*'*'}
The PeakRemover9001 filters all files with the matching PATTERN for values exceding the median of
all values by UPPER_OFFSET or descends by LOWER_OFFSET.

 - If you want to enter UPPER_OFFSET == LOWER_OFFSET you can use MAX_OFFSET instead.
 - The PATTERN can be changed as parameter

After scanning it will add all files accepted by the filter to a folder with the current date and
time. At the end a graph will be created and displayed to identify possible "leftover" peaks to
further tune the offsets.
{100*'*'}
"""

def main(argv):
    pattern = "??.??.????_??.??.??_EMGAufzeichnung_Lable_?.txt"
    max_offset = 1000
    upper_offset = -1 
    lower_offset = -1
    try:
        opts, args = getopt(argv,"hp:o:u:l:",["pattern=", "max_offset=", "upper_offset=", "lower_offset="])
    except GetoptError:
        print(help_string)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h' or len(argv) == 0:
            print(programm_description)
            print(help_string)
            sys.exit()
        elif opt in ("-p", "--pattern"):
            pattern = arg
        elif opt in ("-o", "--offset"):
            max_offset = abs(int(arg))
        elif opt in ("-u", "--upper"):
            upper_offset = abs(int(arg))
        elif opt in ("-l", "--lower"):
            lower_offset = abs(int(arg))
    if upper_offset == -1 and lower_offset == -1:
        upper_offset = max_offset
        lower_offset = max_offset
    elif upper_offset == -1 or lower_offset == -1:
        print("You need to enter upper_offset AND lower_offset OR the max_offset")
        print(help_string)
        sys.exit()
    
    # check for files to filter
    files = fnmatch(os.listdir(os.getcwd()), pattern)
    if not files:
        print(f"Not Files with matching pattern found!\ncurrent Pattern: {pattern}")
        sys.exit()

    # create output dir
    print("Creating output directory... ", end="")
    path = os.path.join(os.getcwd(), strftime("%d.%m.%Y_%H.%M.%S") + f"---offsets_{lower_offset}_{upper_offset}")
    try:
        os.mkdir(path)
    except OSError:
        print(f"failed!\nPath: {path}")
        sys.exit()
    print("done!\n")

    # calculating median
    channel_values = list([] for _ in range(0,4))
    for file in files:
        print(f"\rCalculating median... File {files.index(file)+1}/{len(files)}", end="")
        f = open(file, "r")
        for values in f.readlines():
                channel_values[0].append(int(values.split(',')[0]))
                channel_values[1].append(int(values.split(',')[1]))
                channel_values[2].append(int(values.split(',')[2]))
                channel_values[3].append(int(values.split(',')[3]))
        f.close()
    channel_median = [median(channel_values[0]),median(channel_values[1]), median(channel_values[2]), median(channel_values[3])]
    print("\rCalculating median... done!" + 10*" ")
    print(f"\nMedian: {channel_median}")

    # filter files
    print("\nFiltering...")
    for file in files:
        print(f"File {files.index(file)+1}/{len(files)}", end=" - ")
        try:
            f = open(file, "r")
            for line in f.readlines():
                values = line.split(',')[:-1]
                for channel_number, value in enumerate(values):
                    if int(value) > channel_median[channel_number] + upper_offset or int(value) < channel_median[channel_number] - lower_offset:
                        raise ValueError
            f.close()
            print("ok!", end=" - ")
            copyfile(file, os.path.join(path, file))
            print("Moved!")
        except ValueError:
            f.close()
            print(f"bad! {file}")
            pass

    # print graph
    print("\nGenerating graph plot... ", end="")

    filtered_files = fnmatch(os.listdir(path), pattern) # Read all newly filtered files
    channel_values = list([] for _ in range(0,4))
    for file in filtered_files:
        f = open(file, "r")
        for values in f.readlines():
                channel_values[0].append(int(values.split(',')[0]))
                channel_values[1].append(int(values.split(',')[1]))
                channel_values[2].append(int(values.split(',')[2]))
                channel_values[3].append(int(values.split(',')[3]))
        f.close()
    
    fig_quad, axs = plot.subplots(2, 2, sharex=True, sharey=True) # Create 2x2 subplots (one for each channel)
    fig_quad.suptitle(f"Offsets: [{lower_offset},{upper_offset}]    Number of files: {len(filtered_files)}/{len(files)}")
    axs[0,0].set_ylim([mean(channel_median)-lower_offset if mean(channel_median)-lower_offset > 0 else 0, mean(channel_median)+upper_offset if mean(channel_median)+upper_offset < 1024 else 1024])
    channel_plotcolor = ["-r", "-g", "-b", "-m"]
    for channel in range(4): # plot channels in subplots
        print(f"Channel {channel}... ", end="")
        axs[int(channel/2), channel%2].plot(range(len(channel_values[channel])), channel_values[channel], channel_plotcolor[channel])
        axs[int(channel/2), channel%2].set_title(f"Channel {channel}")
        axs[int(channel/2), channel%2].grid(which='major', axis='y', linestyle='-')
        axs[int(channel/2), channel%2].minorticks_on()
        axs[int(channel/2), channel%2].grid(which='minor', axis='y', linestyle='--')
    print("done!")

    print("\nSaving plot as image... ", end="")
    fig_quad.savefig(os.path.join(path, "Channelview"), dpi=600) # export graph as image
    OpenImage(os.path.join(path, "Channelview.png")).show() # display the exported image
    print("done!")

    print(f"\nCompleted successfuly!")

if __name__ == "__main__":
   main(sys.argv[1:])