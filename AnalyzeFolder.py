'''
Created on 08.02.2024

@author: abdelmawla saeed Rizk
'''

 

import keyboard 
import pyperclip
import inspect
import time , os
import json 
from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import pipeline
import torch
from builtins import isinstance
 

coder = r"C:\Models\deepseek-coder-1.3b" # Download from https://huggingface.co/deepseek-ai/deepseek-coder-1.3b-instruct/tree/main
#coder = r"C:\Models\Deepseek-Coder-7B-Instruct" 
#coder = r"C:\Models\microsoft_phi2" 


tokenizer_coder = AutoTokenizer.from_pretrained(coder , trust_remote_code=True)
model_coder = AutoModelForCausalLM.from_pretrained(coder , trust_remote_code=True, torch_dtype=torch.bfloat16).cuda()

textchars = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)) - {0x7f})
is_binary_string = lambda bytes: bool(bytes.translate(None, textchars))
 
 
global ToAnalyzeFolder
ToAnalyzeFolder =  r"C:\Users\abdelmaw\Documents\Git\hyperion-ultra\Unity" #r"C:\Users\abdelmaw\Documents\GitHub\Wingman" #
 
ignoreList =[".git" ,".gitattributes" , ".gitignore" , ".project" , ".pydevproject" , ".settings"  ,".vs"]

extensions =dict()
extensions[".py"] = "Python"
extensions[".bat"] = "Batch"
extensions[".unity"] = "Unity"
extensions[".cs"] = "C Sharp"
extensions[".txt"] = "Text"
extensions[".yaml"] = "Yaml"
extensions[".yml"] = "Yaml"
extensions[".json"] = "Json"
extensions[".html"] = "HTML , without including any HTML Tags in the output"


Keys =[]

def ask_coder(message):
        # Create a list of messages to be sent to the model
        messages=[{ 'role': 'user', 'content':   message}]
    
        # Apply the chat template to the messages and add a generation prompt
        inputs = tokenizer_coder.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt").to(model_coder.device)
    
        # Generate responses from the model
        outputs = model_coder.generate(inputs, max_new_tokens=1024, do_sample=True, top_k=50, top_p=0.95, num_return_sequences=1, eos_token_id=tokenizer_coder.eos_token_id)
    
        # Decode the output sequences
        outputstr= str( tokenizer_coder.decode(outputs[0][len(inputs[0]):], skip_special_tokens=True) )
        
        
        return outputstr

def to_html(d, c = 1):
    for a, b in d.items():
        
 
 
        yield "{}<h{} id={} style='color: Navy '>{}</h{}>".format('   '*(c +1),c, '"'+a +'"' ,   a,c    )
        if isinstance(b, dict):
 
            yield '{}<ul>\n{}\n{}</ul>'.format('   '*c, "\n".join(to_html(b, c + 1)), '   '*c)
    
        else:
            
            for key in Keys:
                b = b.replace(key, f'<a href="#{key}">{key}</a>')
            
            yield b.replace('\n', '<br>')
              
        


 
# This code is a Python script that uses the Hugging Face's transformers library to load a pre-trained model for text generation and a spelling correction model. The AutoTokenizer and AutoModelForCausalLM classes are used to load the models. The pipeline function is used to create a text-to-text generation pipeline. The fix-spelling function is used to correct the spelling of a given text.
# Here's a brief explanation of the code.
#
#  - `coder = r"C:\Models\deepseek-coder-1.3b"` and `spelling = r"C:\Models\spelling-correction-multilingual-base"`: These lines are defining the paths to the pre-trained models.
#  - `tokenizer_coder = AutoTokenizer.from_pretrained(coder , trust_remote_code=True)` and `model_coder = AutoModelForCausalLM.from_pretrained(coder , trust_remote_code=True, torch_dtype=torch.bfloat16).cuda()`: These lines are loading the pre-trained models and converting them to the appropriate data types for the GPU.
#  - `fix_spelling_pipeline = pipeline("text2text-generation",model= spelling)`: This line is creating a text-to-text generation pipeline using the spelling correction model.
#
# Please note that the code is using the AutoTokenizer and AutoModelForCausalLM classes from the transformers library, which are part of the Hugging Face's transformers library. The pipeline function is a part of the transformers library, and the fix-spelling function is a custom function that uses the fix-spelling-pipeline to correct the spelling of a given text. 

 
 
 

def AnalyzeFolder( Folder = None):
    
    
    
    returnDict = True
    
    if Folder is None:
        returnDict = False
 
        global ToAnalyzeFolder
        ToAnalyzeFolder

        Folder = ToAnalyzeFolder
    
    
    print(Folder)
    
    
    resDict = dict()
    
    filename = os.path.join(Folder,'Report.json' )
    if os.path.isfile(filename):
        
        with open(filename) as json_data:
        
            resDict = json.load(json_data)
        
        
        
    if os.path.isdir(os.path.abspath(Folder) ) :
    
        #Python get a list of files and folders in directory .
    
        listFIlsdir  = os.listdir(Folder)
        
        listFIlsdir.sort()
        
        for ele in listFIlsdir:
            
            
            
            if ele not in ignoreList :
                
                if ele not in Keys:
                    Keys.append(ele)
                
    
                fullpath = os.path.join(Folder,ele )
                
 
                print(fullpath , "is Not binary")                        
                
                
                res = None
                if os.path.isdir(fullpath):
                
                    res = AnalyzeFolder(fullpath)
                
                
                elif os.path.isfile(fullpath):
 
                    try:
  
                        res = None
                        for key in extensions.keys():
                            if key in ele:
                                fileType = extensions.get(key)   
                                
                                
                                if is_binary_string(open(fullpath, 'rb').read(1024)):
                                    print(fullpath , "is  binary")
                                    res = fullpath + "is  binary"
                                    
                                else:                         
                                
                                    data = ""
                                    with open(fullpath, 'r') as file:
                                    
                                        data = file.read()
                                    
                                    if len(data) >0:
                            
                                       message = f"Explain this {fileType} in details , What is its purpose and what does it do?\n'''\n"+data+"'''\n"
                                       res = ask_coder(message)
                                    
                                    
                                    else:
                                        res = "File is empty"
                                    
                                break
                         
                        if res is None:
                            res =  fullpath + " is  skipped"
 
                
                    except:
                        res =  ele + "  is not Readable"
                
                
                if resDict.get(ele) is not None:
                    res_old = resDict.get(ele)
                    message = f"combine the information  in these two segments {fileType}  "+res_old+"''' \n and " + res
                    res = ask_coder(message) 
                    resDict[ele] = res                   
                    
                else:            
                    resDict[ele] = res
    if returnDict:
        return resDict
    
    else:

        # json file to write to
        
        data = '\n'.join(to_html(resDict))
        
        filename = os.path.join(Folder,'CoderReport.json' ) 
        
        with open(filename, 'w') as f:
        
            json.dump(resDict, f)
        
            print(f"Data written to {filename}")
        #

        filename = os.path.join(Folder,'CoderReport.html' )  
        with open(filename, 'w' , encoding="utf-8") as f:
            
            f.write(data)
            print(f"Data written to {filename}")
            
        
     
if __name__ == '__main__':
    
    AnalyzeFolder()
    
    

 

 
 