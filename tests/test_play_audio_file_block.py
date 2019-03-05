from nio import Signal
from nio.testing.block_test_case import NIOBlockTestCase
from unittest.mock import patch
from ..play_audio_file_block import PlayAudioFile


class TestPlayAudioFile(NIOBlockTestCase):

    @patch(PlayAudioFile.__module__ + '.simpleaudio')
    def test_plays_file(self, patch_audio):
        blk = PlayAudioFile()
        self.configure_block(blk, {
            'audio_file': 'myfile.wav',
        })
        with patch(PlayAudioFile.__module__ + '.isfile') as isfile:
            isfile.return_value = True
            blk.process_signals([Signal({})])
        isfile.assert_called_once_with('myfile.wav')
        # We should load the wav file and then play it
        wav_loader = patch_audio.WaveObject.from_wave_file
        wav_loader.assert_called_once_with('myfile.wav')
        wav_loader.return_value.play.assert_called_once_with()

    @patch(PlayAudioFile.__module__ + '.simpleaudio')
    def test_skips_missing_file(self, patch_audio):
        blk = PlayAudioFile()
        self.configure_block(blk, {
            'audio_file': 'badfile.wav',
        })
        with patch(PlayAudioFile.__module__ + '.isfile') as isfile:
            isfile.return_value = False
            blk.process_signals([Signal({})])
        isfile.assert_called_once_with('badfile.wav')
        wav_loader = patch_audio.WaveObject.from_wave_file
        # Make sure we don't try to create the audio object
        self.assertEqual(wav_loader.call_count, 0)
