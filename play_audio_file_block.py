from os.path import isfile
from nio import Block
from nio.block.mixins import LimitLock
from nio.properties import FileProperty, IntProperty, VersionProperty
import simpleaudio


class PlayAudioFile(LimitLock, Block):

    version = VersionProperty('0.1.0')
    audio_file = FileProperty(title='Audio File Location', default='audio.wav')
    max_locks = IntProperty(title='Audio Queue Size', default=5, advanced=True)

    def process_signal(self, signal, input_id=None):
        file_loc = self.audio_file(signal).value
        if not isfile(file_loc):
            self.logger.error(
                "{} is not a valid file location".format(file_loc))
            return
        obj = simpleaudio.WaveObject.from_wave_file(file_loc)
        self.execute_with_lock(
            self._play_simpleaudio, self.max_locks(signal), obj)
        # Notify the incoming signal once the audio has completed playing
        return signal

    def _play_simpleaudio(self, audio_obj):
        """ Plays a simpleaudio object and waits for it to complete """
        self.logger.info("Playing simpleaudio obj {}".format(audio_obj))
        play = audio_obj.play()
        play.wait_done()

    def stop(self):
        simpleaudio.stop_all()
        super().stop()
