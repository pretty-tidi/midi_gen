# bunch of functions that were used somewhere in the pre processing stage
# kept as an archive of how to use pretty_midi
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
    out_dir_name = "data/transposed/"
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
        b.write(out_dir_name + "bass_line_%d.mid" % i)


def check_beats_per_measure():
    dir_name = "data/"
    out_dir_name = "data/transposed/"
    with open("bass_consistent_time_and_key.txt", "r") as f:
        file_names = f.readlines()
        file_names = [file_name.strip() for file_name in file_names]

    cap = 1000  # len(file_names)

    time_sigs = {}

    for i in tqdm(range(cap)):
        try:
            b = Bass(dir_name + file_names[i])
        except:
            print("Exception with " + file_names[i])
            continue

        beats = b.beats_per_measure
        if beats in time_sigs:
            time_sigs[beats] += 1
        else:
            time_sigs[beats] = 1

    for key in time_sigs:
        print("Beats per measure:", key, " | Amount:", time_sigs[key])
    print("Total:", cap)


def check_time_and_gen():
    dir_name_out = "data/transposed/"
    dir_name_in = "data/"

    with open("bass_consistent_time_and_key.txt", "r") as f:
        bass_midis = f.readlines()
        bass_midis = [name.strip() for name in bass_midis]

    cap = len(bass_midis)
    amt = 0
    for i in tqdm(range(cap)):
        try:
            b = Bass(file_name=dir_name_in + bass_midis[i])
        except:
            print("Error reading" + bass_midis[i], file=sys.stderr)
            continue
        if b.valid:
            print(bass_midis[i])
            b.auto_transpose()
            b.write(dir_name_out + "bass_line_time4_%d.mid" % amt)
            amt += 1
    print("Amount:", amt, file=sys.stderr)


def check_bass_keys():
    bass_files = os.listdir("data/transposed")
    cap = 1000 # len(bass_files)
    dir = "data/transposed/"

    keys = {}

    for i in tqdm(range(cap)):
        try:
            b = Bass(file_name=dir + bass_files[i], already_bass=True)
        except:
            print("Error with", dir + bass_files[i])
            print(sys.exc_info()[0])
            continue
        if not b.valid:
            print("What the fuck?", b.invalid_reason)
            continue
        if b.key in keys:
            keys[b.key] += 1
        else:
            keys[b.key] = 1
    print("Printing stats...")
    for key in keys:
        print("Key signature:", key, "--Amount:", keys[key])

def test_vector_gen():
    try:
        b = Bass(file_name="data/fff537c7ec012eb3d95245eb79f84adb.mid")
    except:
        print("Error opening file")
        sys.exit(1)

    if not b.valid:
        print("invalid")
        sys.exit(1)

    for v in b.time_step_vector_gen():
        print(v)




if __name__ == "__main__":
    test_vector_gen()






























