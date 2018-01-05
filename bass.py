import pretty_midi
import sys, re

class Bass(object):

    def __init__(self, midi_file_name):

        try:
            midi = pretty_midi.PrettyMIDI(midi_file_name)
        except:
            raise Exception("class Bass: Error reading" + midi_file_name)

        self.bass_inst = self._get_bass(midi)
        if self.bass_inst == None:
            self.valid = False
            self.invalid_reason = "No instrument with 'bass/Bass' in name"
            return
        elif len(midi.key_signature_changes) != 1:
            self.valid = False
            self.invalid_reason = "Key signature change amount is not 1. Weird to use"
            return
        elif len(midi.time_signature_changes) != 1:
            self.valid = False
            self.invalid_reason = "Time signature change amount is not 1. Weird to use"
            return
        else:
            self.valid = True
            self.invalid_reason = "Not invalid"

        # pretty midi maps major keys to 0-11 and minor keys to 12-23
        self.major = True if midi.key_signature_changes[0].key_number < 12 else False
        self.key = midi.key_signature_changes[0]

    # find if there is a bass line instrument, return it if there iss
    def _get_bass(self, midi):
        for inst in midi.instruments:
            if re.match(".*(bass|Bass).*", inst.name):
                return inst
        return None

    # transpose to c major
    def to_c_major(self):
        if not self.valid:
            print("to_c_major on invalid Bass object", file=sys.stderr)
            return
        if not self.major:
            print("Transposing minor key bass line to C major...", file=sys.stderr)



        return "This dick"

    # transpose to a minor
    def to_a_minor(self):
        if not self.valid:
            print("to_c_major on invalid Bass object", file=sys.stderr)
            return
        if self.major:
            print("Transposing major key bass line to A minor..", file=sys.stderr)


        return "This dick"


    # generator of the one-hot note vectors for the rnn
    def note_vector_gen(self):
        yield "this dick"

    # write the bass instrument with the file name file_name
    # use pretty_midi to do this
    # make the file called whatever, but make sure it has the single instrument called bass or something,
    # so that this object can be used not only during preprocessing, but then to re-read these written
    # midi bass lines and use this for the note_vector_gen with training
    def write(self, file_name):
        print("write does nothing", file=sys.stderr)
        return


