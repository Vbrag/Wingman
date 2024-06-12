'''
Created on 14.02.2024

@author: abdelmawla saeed Rizk
'''

 
from transformers import WhisperProcessor, WhisperForConditionalGeneration
#from pydub import AudioSegment
#from pydub.utils import mediainfo
import librosa
import soundfile as sf 
import os



# load model and processor

# processor = WhisperProcessor.from_pretrained(r"C:\Models\whisper-large-v2")
# model = WhisperForConditionalGeneration.from_pretrained(r"C:\Models\whisper-large-v2")
# processor = WhisperProcessor.from_pretrained(r"C:\Models\whisper-medium")
# model = WhisperForConditionalGeneration.from_pretrained(r"C:\Models\whisper-medium")

processor = WhisperProcessor.from_pretrained(r"C:\Models\whisper-small.en")
model = WhisperForConditionalGeneration.from_pretrained(r"C:\Models\whisper-small.en")
model.config.forced_decoder_ids = None
    
    
 


 
 
base = r"C:\Users\abdelmaw\Documents\GitHub\downloadYoutube"#os.path.dirname(os.path.abspath(__file__))

def MP3ToTxt(mp3, txt):
    
    try:
        speech, rate = sf.read(mp3 )
        #print(rate)
        
        print(speech.shape)
        speech = librosa.resample(speech.T, orig_sr= rate, target_sr=16000)
        speech = speech[0] + speech[1]
        #speech = speech[0:int( len(speech)/75 )]
        step = 400000
        length = int( len(speech)/step ) +1
    
    
    except:
        speech, rate = sf.read(mp3 )
        #print(rate)
        
        print(speech.shape)
        speech = librosa.resample(speech.T, orig_sr= rate, target_sr=16000)  
        #speech = speech[0:int( len(speech)/75 )]
        step = 400000
        length = int( len(speech)/step ) +1    
    
    lines = []
    
    
    
    for i in range(0,length ):
        subspeech = speech[i*step:(i+1)*step]
        input_features = processor(subspeech , sampling_rate=16000, return_tensors="pt"  , truncation = False).input_features 
        #print(input_features.shape)
        # generate token ids
        predicted_ids = model.generate(input_features)
        # decode token ids to text
        #transcription = processor.batch_decode(predicted_ids, skip_special_tokens=False)
        #print(transcription)
        transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)
        print(transcription[0])
        lines.append(transcription[0])
        
    
    with open(txt, 'w' ,   encoding="utf-8") as the_file:
        
        for line in lines:
            the_file.write(line + "\n")
 
    
 
if __name__ == '__main__':
    for root, dirs, files in os.walk(base):
        for file in files:
            if file.endswith(".mp3"):
                mp3 = os.path.join(root, file)
                
                txt = mp3.replace(".mp3", ".txt")
                
                print(mp3)
                #if not os.path.isfile(txt) and os.stat(mp3).st_size > 0 :              
                    
                MP3ToTxt(mp3, txt)
                os.remove(mp3)

 
 