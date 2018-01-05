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

# gets valid bass lines (single key signature and single time signature)
def get_workable_bass():

    valid = 0
    dir_name = "data/"

    file_names = os.listdir(dir_name)
    cap = len(file_names)

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


def shift_and_write():
    dir_name = "data/"
    with open("bass_consistent_time_and_key.txt", "r") as f:
        file_names = f.readlines()
        file_names = [file_name.strip() for file_name in file_names]

    cap = 10 # len(file_names)

    for i in tqdm(range(cap)):
        try:
            b = Bass(dir_name + file_names[i])
        except:
            print("Exception with " + file_names[i])
            continue

        b.auto_transpose()
        b.write("bass_line_%d.mid" % i)




if __name__ == "__main__":
    shift_and_write()

































