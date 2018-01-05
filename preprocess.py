import pretty_midi
import os, re, sys
from tqdm import tqdm

from bass import Bass

def containsBase(name):
    return re.match(".*(bass|Bass).*", name)

def containsMelody(name):
    return re.match(".*(melody|Melody).*", name)

def get_all_base():
    dirname = "../Desktop/y_machina/Data/Midis_45k_from_echonext_1mil/"
    count = 0
    start = 112000
    i = 0
    files = None
    with open(dirname + "list.txt") as file:
        files = file.readlines()
        files = [name.strip() for name in files]

    for file in files:
        i += 1
        print(i, file=sys.stderr)
        try:
            midi = pretty_midi.PrettyMIDI(dirname+file)
        except:
            print("Some error with ", file, file=sys.stderr)
            continue
        for inst in midi.instruments:
            if containsBase(inst.name):
                print(file)
                print(file, file=sys.stderr)
                count += 1
                break

    print("Total: ", i, "Total with baseline: ", count, file=sys.stderr)

def transpose():

    valid = 0
    dir_name = "data/"

    file_names = os.listdir(dir_name)
    cap = 1000 # len(file_names)

    for i in tqdm(range(cap)):
        try:
            b = Bass(dir_name + file_names[i])
        except:
            print("Error reading " + dir_name + file_names[i], file=sys.stderr)
            continue
        if not b.valid:
            continue
        valid += 1
        print(file_names[i])

    print(valid, "valid out of", cap, file=sys.stderr)




if __name__ == "__main__":
    transpose()

































