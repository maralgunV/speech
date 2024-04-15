import torchaudio
import speechbrain as sb
from speechbrain.dataio.dataio import read_audio
from IPython.display import Audio
from io import BytesIO

from speechbrain.inference.separation import SepformerSeparation as separator

models = [
    Separator.from_hparams(source="speechbrain/sepformer-wham-enhancement", savedir='pretrained_models/sepformer-wham-enhancement'),
    Separator.from_hparams(source="speechbrain/sepformer-wham16k-enhancement", savedir='pretrained_models/sepformer-wham16k-enhancement'),
    Separator.from_hparams(source="speechbrain/sepformer-whamr-enhancement", savedir='pretrained_models/sepformer-whamr-enhancement'),
    Separator.from_hparams(source="speechbrain/sepformer-dns4-16k-enhancement", savedir='pretrained_models/sepformer-dns4-16k-enhancement')
]
import io
from scipy.io.wavfile import write

def enhancement(file_path, modelId):
    enhanced_speech = models[modelId].separate_file(path=file_path)

    enhanced_audio_data = enhanced_speech[:, :].detach().cpu().squeeze().numpy()

    file = io.BytesIO()

    write(file, 8000, enhanced_audio_data)

    file.seek(0)

    return file

