from pydub import AudioSegment
from pydub.silence import split_on_silence
import noisereduce as nr


def normalize_amplitude(chunk, target_dBFS):
  delta_dBFS = target_dBFS - chunk.dBFS
  return chunk.apply_gain(delta_dBFS)


def load_audio(filename):
  return AudioSegment.from_mp3(filename)


def chunk_audio(audio, min_silence_len=200, keep_silence=500, silence_thresh=-48, seek_step=2):
  chunks = split_on_silence(
    audio,
    min_silence_len=min_silence_len,
    keep_silence=keep_silence,
    silence_thresh=silence_thresh,
    seek_step=seek_step,
  )

  print(len(chunks))

  i = 0
  for chunk in chunks:
    normalized_chunk = normalize_amplitude(chunk, -24.0)
    normalized_chunk.export(f'/tmp/chunks/chunk-{i}-orig.wav', format='wav')

    reduced_noise = nr.reduce_noise(
      y=normalized_chunk.get_array_of_samples(),
      sr=normalized_chunk.frame_rate,
      prop_decrease=0.5,
    )

    new_sound = normalized_chunk._spawn(reduced_noise)
    new_sound = normalize_amplitude(new_sound, -24.0)
    new_sound.export(f'/tmp/chunks/chunk-{i}-nr.wav', format='wav')

    i += 1

    # reduced_noise.export("chunk.mp3", format="mp3")

    # yield normalized_chunk

    # print('Exporting chunk{0}.mp3.'.format(i))
    # normalized_chunk.export(
    #     './chunks/chunk{0}.mp3'.format(i),
    #     bitrate = '192k',
    #     format = 'mp3'
    # )

chunk_audio(load_audio('/tmp/KPDX3-Twr-123775-Oct-01-2021-2000Z.mp3'))
