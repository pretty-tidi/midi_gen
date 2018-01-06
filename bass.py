import pretty_midi
import sys, re
import tensorflow

# creates a PrettyMIDI and gets the bass line from it. Marks as either valid or invalid bass object
# reasons it could be invalid:
#   no bass line/instrument with bass in the name
#   key signature changes around (hard to work with)
#   time signature changes around (hard to work with)
#   time signature is not 4 beats per measure
#
# has a generator function for generating the vector for each time step (for the lstm)

class Bass(object):

    def __init__(self, file_name=None, already_bass=False):

        # will be useful for generating new midis from whatever lstm generates
        if file_name == None:
            self._empty_initiate()
            return

        midi = pretty_midi.PrettyMIDI(file_name)

        bass_inst = self._get_bass(midi)
        if bass_inst == None:
            self.valid = False
            self.invalid_reason = "No instrument with 'bass/Bass' in name"
            return
        elif len(midi.key_signature_changes) != 1 and not already_bass:
            self.valid = False
            self.invalid_reason = "Key signature change amount is %d. Weird to use" % len(midi.key_signature_changes)
            return
        elif len(midi.time_signature_changes) != 1:
            self.valid = False
            self.invalid_reason = "Time signature change amount is %d. Weird to use" % len(midi.time_signature_changes)
            return
        elif midi.time_signature_changes[0].numerator != 4:
            self.valid = False
            self.invalid_reason = "Only doing 4/x time sig right now"
            return
        else:
            self.valid = True
            self.invalid_reason = "Not invalid"

        # pretty midi maps major keys to 0-11 and minor keys to 12-23
        if midi.key_signature_changes[0].key_number < 12:
            self.major = True
        else:
            self.major =  False

        self.key = midi.key_signature_changes[0].key_number
        self.beats_per_measure = midi.time_signature_changes[0].numerator
        self.gets_the_beat = midi.time_signature_changes[0].denominator
        self.tempo = midi.estimate_tempo()
        self.length = midi.get_end_time() # should return length of midi file in seconds
        self.beats = midi.get_beats()
        self.notes = bass_inst.notes


    # find if there is a bass line instrument, return it if there iss
    def _get_bass(self, midi):
        for inst in midi.instruments:
            if re.match(".*(bass|Bass).*", inst.name):
                return inst
        return None

    # transpose to c major
    # pretty_midi maps shit in terms of half steps, 0-11 being c major, c# major, d major, etc
    def to_c_major(self):
        if self.key == 0:
            return

        # shift them all up to nearest c octave. up cause bass notes tend to be low, don't wanna overflow
        shift_amt = 12 - self.key
        for note in self.notes:
            note.pitch += shift_amt

    # transpose to a minor
    # pretty_midi maps shit in terms of half steps, 12-23 being c minor, c# minor, d minor etc
    def to_a_minor(self):
        if self.key == 21:
            return

        # shift them to a minor. most will be shifted up, some down though
        shift_amt = 21 - self.key
        for note in self.notes:
            note.pitch += shift_amt

    def auto_transpose(self):
        if not self.valid:
            print("not transposing on invalid Bass object", file=sys.stderr)
            return
        if self.major:
            self.to_c_major()
        else:
            self.to_a_minor()

    # generator of the one-hot note vectors for the rnn
    # vector specs:
    #   0-87 are corresponding notes on the piano (88 keys)
    #   88 is for the lack of a note (rest)
    #   89 is for continuation of the previous note
    def time_step_vector_gen(self):
        note_change = False
        index_in_notes = 0
        for beat_sec in self._get_half_beats():  # beat is an increment in seconds
            if self.notes[index_in_notes].end <= beat_sec:
                note_change = True
                index_in_notes += 1
            if self.notes[index_in_notes].start >= beat_sec:
                if not note_change:
                    yield Bass._vectorize(89) # continuation of previous note
                else:
                    yield Bass._vectorize(self.notes[index_in_notes].pitch)
            else:
                note_change = False # i think i want this here
                yield Bass._vectorize(88) # rest/lack of pitch

        return

    # this doesn't always work right for some reason. it'll write it properly to play but
    # prettyMIDI has errors re-reading those written files
    # copy pasta from documentation
    def write(self, file_name): # TODO
        # Create a PrettyMIDI object
        bass_line = pretty_midi.PrettyMIDI()
        # Create an Instrument instance for a cello instrument
        bass_program = pretty_midi.instrument_name_to_program('Cello')
        bass = pretty_midi.Instrument(program=bass_program)
        bass.notes = self.notes
        bass.name = "bassline"
        # Add the cello instrument to the PrettyMIDI object
        bass_line.instruments.append(bass)
        # Write out the MIDI data
        bass_line.write(file_name)

    # will be useful for generating new midis from whatever lstm generates
    def _empty_initiate(self):
        print("Nothing happening", file=sys.stderr)
        return

    # generator
    def _get_half_beats(self):
        for i in range(len(self.beats) - 1):
            yield self.beats[i]
            yield (self.beats[i+1] + self.beats[i]) / 2
        yield self.beats[len(self.beats)-1]
        return

    # i have no idea how to use tensorflow or numpy arrays
    @staticmethod
    def _vectorize(pitch):
        # v = tensorflow.Variable(tensorflow.zeros(90))
        # v[pitch] = 0
        # return v
        v = [0] * 90
        v[pitch] = 1
        return v
















