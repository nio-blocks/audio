# PlayAudioFile

Plays an audio file from disk. Currently supports WAV files only.

This block plays a WAV file from disk and notifies the incoming signal once the playing has completed. It makes use of the [LimitLock mixin](https://docs.n.io/blocks/block-mixins/limit-lock.html) to ensure that only one file gets played at a time.

## Properties

 * **Audio File Location** - The location of the audio file. If a relative path is given then it is interpreted from the working directory. To ensure a path relative from the project root use the `[[PROJECT_ROOT]]` environment variable.
 * **Audio Queue Size** - The max number of audio files to queue up for playing. The block only plays one audio file at a time, this number represents the maximum number of files to queue up for playing. It is equivalent to the `max_locks` attribute of the LimitLock mixin.

## Outputs

 * The incoming signal is notified when the audio file has completed playing. If the file is not played (if it doesn't exist or the queue is full) then the signal is not notified.
