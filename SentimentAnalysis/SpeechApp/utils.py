import librosa
import numpy as np
import soundfile


def extract_feature(file_name, mfcc=True, chroma=True, mel=True):
    try:
        with soundfile.SoundFile(file_name) as sound_file:
            X = sound_file.read(dtype="float32")
            sample_rate = sound_file.samplerate

            # Compute features
            result = []
            if mfcc:
                mfccs = librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40)
                mfccs_mean = np.mean(mfccs.T, axis=0)
                result.extend(mfccs_mean)

            if chroma:
                stft = np.abs(librosa.stft(X))
                chroma = librosa.feature.chroma_stft(S=stft, sr=sample_rate)
                chroma_mean = np.mean(chroma.T, axis=0)
                result.extend(chroma_mean)

            if mel:
                mel_spectrogram = librosa.feature.melspectrogram(y=X, sr=sample_rate)
                mel_spectrogram_mean = np.mean(mel_spectrogram.T, axis=0)
                result.extend(mel_spectrogram_mean)

    except Exception as e:
        print(f"Error encountered while parsing file: {file_name}")
        return None

    return result
