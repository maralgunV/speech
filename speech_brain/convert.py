import torchaudio
import speechbrain as sb
from speechbrain.dataio.dataio import read_audio
from IPython.display import Audio

from speechbrain.inference.separation import SepformerSeparation as separator
model = separator.from_hparams(source="speechbrain/sepformer-whamr-enhancement", savedir='pretrained_models/sepformer-whamr-enhancement')

print("TEST")
# enhanced_speech = model.separate_file(path='maralgun.wav')

# file = Audio(enhanced_speech[:, :].detach().cpu().squeeze(), rate=8000)

def enhancement(file_path):
    enhanced_speech = model.separate_file(path=file_path)
    return Audio(enhanced_speech[:, :].detach().cpu().squeeze(), rate=8000)

def send_audio(enhanced_audio):
    output = BytesIO()
    torchaudio.save(output, enhanced_audio[0], enhanced_audio[1], format="wav")
    output.seek(0)
    return send_file(output, mimetype="audio/wav")