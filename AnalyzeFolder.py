'''
Created on 14.02.2024

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
import gc 
 
os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'expandable_segments:True'


coder = r"C:\Models\deepseek-coder-1.3b" # Download from https://huggingface.co/deepseek-ai/deepseek-coder-1.3b-instruct/tree/main
#coder = r"C:\Models\Deepseek-Coder-7B-Instruct" 
#coder = r"C:\Models\microsoft_phi2" 
global ToAnalyzeFolder
ToAnalyzeFolder = r"C:\Users\abdelmaw\Documents\GitHub\Wingman" # r"C:\Users\abdelmaw\Documents\Git\hyperion-ultra\Unity"#  r"C:\Users\abdelmaw\Documents\GitHub\Wingman"#  # r"C:\Users\abdelmaw\Documents\GitHub\Wingman" #r"C:\Users\abdelmaw\Documents\GitHub\ATMOS-Scenery-Generator" #  
 
global KeysList 
KeysList =[] 
 

tokenizer_coder = AutoTokenizer.from_pretrained(coder , trust_remote_code=True)
model_coder = AutoModelForCausalLM.from_pretrained(coder , trust_remote_code=True, torch_dtype=torch.bfloat16).cuda()

textchars = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)) - {0x7f})
is_binary_string = lambda bytes: bool(bytes.translate(None, textchars))
 
 
 

ignoreList =[".git" ,".gitattributes" , ".gitignore" , "ignore", ".project" , ".pydevproject" , ".settings"  ,".vs" ,"__pycache__"]

extensions =dict()
extensions[".py"] = "Python"
extensions[".bat"] = "Batch"
extensions[".cs"] = "C Sharp"
extensions[".txt"] = "Text"
extensions[".yaml"] = "Yaml"
extensions[".yml"] = "Yaml"
extensions[".json"] = "Json"
extensions[".html"] = "HTML , without including any HTML Tags in the output"
extensions[".xml"] = "XML"



def ask_coder(message):
        # Create a list of messages to be sent to the model
        messages=[{ 'role': 'user', 'content':   message}]
    
        # Apply the chat template to the messages and add a generation prompt
        inputs = tokenizer_coder.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt").to(model_coder.device)
    
        # Generate responses from the model
        outputs = model_coder.generate(inputs, max_new_tokens=1024, do_sample=True, top_k=50, top_p=0.95, num_return_sequences=1, eos_token_id=tokenizer_coder.eos_token_id)
    
        # Decode the output sequences
        outputstr= str( tokenizer_coder.decode(outputs[0][len(inputs[0]):], skip_special_tokens=True) )
        
        del inputs
        del outputs
        gc.collect()
        torch.cuda.empty_cache()
        return outputstr


translationDict = dict()

translationDict["'''"] = ["<code>" , "</code>" ]
translationDict["**"]  = ["<strong>" , "</strong>" ]
#translationDict["'"]  = ["<em>" , "</em>" ]
translationDict["`"]  = ["<em>" , "</em>"]

def to_html(d, c = 1):
 
    global KeysList 
    folders = []
    files = []    
    
    dkeys = list(d.keys())
    
    for ele in dkeys:
        
        b  = d.get(ele)
        
        if isinstance(b, str)  : 
            files.append(ele)
            
        elif  isinstance(b, dict):
            folders.append(ele)
 
 
    folders.sort()        
    files.sort()     
    
    
    dkeysmew = folders + files
    
    for a in dkeysmew:
        
        b  = d.get(a)
 
        if isinstance(b, str) :
        
        
            yield "{}<button id={} class='collapsible'>{}</button>  ".format('   '*(c +1),  '"'+a +'"'  , a    )
            
        else:
            yield "{}<h{} id={} style='background-color: #777;color: white;cursor: pointer;padding: 18px;width: 100%;border: none;text-align: left;outline: none;font-size: 15px;'>{}</h{}>".format('   '*(c +1) ,c, '"'+a +'"',   a,c    )            
            
        if isinstance(b, dict):
        
            yield '{}<ul>\n{}\n{}</ul>'.format('   '*c, "\n".join(to_html(b, c + 1)), '   '*c)
        
        else:
            
            b =  b.replace('<', '&lt')    
            b =  b.replace('>', '&gt')  
            for key in KeysList:
                
        
                
                b = b.replace(" "+key + " ", f' <a href="#{key}">{key}</a> ' )
                b = b.replace(" "+key + "'", f' <a href="#{key}">{key}</a>'+"'" )
                b = b.replace("'"+key + " ", "'"+f'<a href="#{key}">{key}</a> ' )  
                b = b.replace("'"+key + "'", "'"+f'<a href="#{key}">{key}</a>'+"'" ) 
                                
                b = b.replace(" "+key + '"', f' <a href="#{key}">{key}</a>'+'"' )
                b = b.replace('"'+key + " ", '"'+f'<a href="#{key}">{key}</a> ' )  
                b = b.replace('"'+key + '"', '"'+f'<a href="#{key}">{key}</a>'+'"')
        
                b = b.replace(" "+key + '`', f' <a href="#{key}">{key}</a>'+'`' )
                b = b.replace('`'+key + " ", '`'+f'<a href="#{key}">{key}</a> ' )  
                b = b.replace('`'+key + '`', '`'+f'<a href="#{key}">{key}</a>'+'`')
                
                
                
            for key in translationDict.keys():
                
                start = True
                if key in b:
                    while key in b :
                        index = b.find(key)
                        if start:
                            b = b[0:index] + translationDict.get(key)[0] + b[index+len(key):]
                            start = False
                        else:
                            b = b[0:index] + translationDict.get(key)[1] + b[index+len(key):]                            
                            start = True
                    
                    
            
            
            
                
                                 
            b = '<div class="content">'+b.replace('\n', '<br>') + "</div>"
        
            
            yield b
                  
        


 
# This code is a Python script that uses the Hugging Face's transformers library to load a pre-trained model for text generation and a spelling correction model. The AutoTokenizer and AutoModelForCausalLM classes are used to load the models. The pipeline function is used to create a text-to-text generation pipeline. The fix-spelling function is used to correct the spelling of a given text.
# Here's a brief explanation of the code.
#
#  - `coder = r"C:\Models\deepseek-coder-1.3b"` and `spelling = r"C:\Models\spelling-correction-multilingual-base"`: These lines are defining the paths to the pre-trained models.
#  - `tokenizer_coder = AutoTokenizer.from_pretrained(coder , trust_remote_code=True)` and `model_coder = AutoModelForCausalLM.from_pretrained(coder , trust_remote_code=True, torch_dtype=torch.bfloat16).cuda()`: These lines are loading the pre-trained models and converting them to the appropriate data types for the GPU.
#  - `fix_spelling_pipeline = pipeline("text2text-generation",model= spelling)`: This line is creating a text-to-text generation pipeline using the spelling correction model.
#
# Please note that the code is using the AutoTokenizer and AutoModelForCausalLM classes from the transformers library, which are part of the Hugging Face's transformers library. The pipeline function is a part of the transformers library, and the fix-spelling function is a custom function that uses the fix-spelling-pipeline to correct the spelling of a given text. 

 


def organizeDict(d):
    global KeysList 
    newDict = dict()
 
    dkeys = list(d.keys())
 
    for a in dkeys:
        
        if len(a) > 2 and not a in KeysList:
            KeysList.append(a)  
        
        b  = d.get(a)
        
        if isinstance(b, str)  and "skipped" in b:
            pass
 
        else:
            if isinstance(b, str) :
                
                newDict[a] = b
     
 
            elif isinstance(b, dict):
                
                b = organizeDict(b)
     
                if len(b.keys()) > 0:
                    newDict[a] = b
                            
 
    return newDict 
    
    
 
def save_res(Folder , resDict):
 
    # json file to write to
    

 
    
    
    filename = os.path.join( Folder,'CoderReport.json' ) 
    
    with open(filename, 'w') as f:
    
        json.dump(resDict, f)
    
        print(f"Data written to {filename}")
    #
 
       
    resDict = organizeDict(resDict)
    
    print("organizeDict ok")
    global KeysList 
    
    KeysList = list(set(KeysList))
 
    KeysList.sort(key=len)
    KeysList.reverse()
    
    print(KeysList)
    print("KeysList sort ok")     
    data = '\n'.join(to_html(resDict))
    
    print("HTML ok")
    
    titel = Folder.split("\\")[-1] 
    
    data = data.replace(ToAnalyzeFolder , titel)
    
    filename = os.path.join(Folder,'CoderReport.html' )  
    with open(filename, 'w' , encoding="utf-8") as f:
        
        data = """
        <!DOCTYPE html>
        <html>
        <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
        .collapsible {
          background-color: #777;
          color: white;
          cursor: pointer;
          padding: 18px;
          width: 100%;
          border: none;
          text-align: left;
          outline: none;
          font-size: 15px;
        }
        
        .active, .collapsible:hover {
          background-color: #555;
        }
        
        .content {
          padding: 0 18px;
          max-height: 0;
          overflow: hidden;
          transition: max-height 0.2s ease-out;
          background-color: #f1f1f1;
        }
        </style> 
        <title>""" + titel  +"""</title>
        </head>
        <body>  """+data+"""
        <script>
        var coll = document.getElementsByClassName("collapsible");
        var i;
        
        for (i = 0; i < coll.length; i++) {
          coll[i].addEventListener("click", function() {
            this.classList.toggle("active");
            var content = this.nextElementSibling;
            if (content.style.maxHeight){
              content.style.maxHeight = null;
            } else {
              content.style.maxHeight = content.scrollHeight + "px";
            } 
          });
        }
        </script>
        <footer>
          <p>Author: deepseek-coder-1.3b<br>
          <a href="https://huggingface.co/deepseek-ai/deepseek-coder-1.3b-instruct/tree/main">deepseek-coder</a></p>
        </footer>        
        </body>
        </html>
        """
        
        f.write(data)
        print(f"Data written to {filename}")
 

def AnalyzeFolder( Folder = None):
    global i
 
    
    returnDict = True
    
    if Folder is None:
        returnDict = False
 
        global ToAnalyzeFolder
 
        Folder = ToAnalyzeFolder
 
 
 
    resDict = dict()
        
 
        
    print(Folder)
    filename = os.path.join(Folder,'CoderReport.json' )
    if os.path.isfile(filename):
        
        with open(filename) as json_data:
        
            resDict = json.load(json_data)


            
            if returnDict:
 
                return resDict
            
            else:
 
                save_res(Folder, resDict)
                return
    if os.path.isdir(os.path.abspath(Folder) ) :
    
        #Python get a list of files and folders in directory .
    
        listFIlsdir  = os.listdir(Folder)
        
        listFIlsdir.sort()
        
        for ele in listFIlsdir:
            
            
            
            if ele not in ignoreList :
                

                
    
                fullpath = os.path.join(Folder,ele )
                
 
                print(fullpath , "is Not binary")                        
                
                
                res = None
                if os.path.isdir(fullpath):
                
                    res = AnalyzeFolder(fullpath)
                
                
                elif os.path.isfile(fullpath):
 
                    #try:
  
                    res = None
                    for key in extensions.keys():
                        if key == ele[-len(key):]:
                            fileType = extensions.get(key)   
                            
                            
                            if is_binary_string(open(fullpath, 'rb').read(1024)):
                                print(fullpath , "is  binary")
                                res = fullpath + "is  binary"
                                
                            else:                         
                            
                                data = ""
                                with open(fullpath, 'r' , encoding="utf8") as file:
                                
                                    data = file.read()
                                
                                if len(data) >0:
                                    
                                    
                                    if len(data)  <= 25*1024:
                                    
 
                                        message = f"Explain this {fileType} in details , What is its purpose and what does it do?\n'''\n"+data+"''' "
                                        res = ask_coder(message)
                                    
                                    else:
                                        
                                        res= ""
                                        for i in range(0 ,len(data), 25*1024 ):
                                            part = data[i:i+25*1024]
                                    
                                            message = f"Explain this {fileType} in details , What is its purpose and what does it do?\n'''\n"+part+"''' "
                                            res = res + ask_coder(message)
                                        
                                    print(res) 
                                    
 
                                        
                                           
                                
                                else:
                                    #
                                    # message = f"what this {fileType} with file name {ele} ,  say about the file"
                                    # res = ask_coder(message)
                                    
                                    res = f"File is empty  "  
                                
                            break
                     
                    if res is None:
                        # message = f"what this  file name {ele} ,  say about the file? and what is this file for?"
                        # res = ask_coder(message)
                        
                        res =  fullpath + " is  skipped    "  
 
                
                    # except:
                    #     res =  ele + "  is not Readable"
                
                
                # if resDict.get(ele) is not None:
                #     res_old = resDict.get(ele)
                #     message = f"combine the information  in these two segments {fileType}  "+res_old+"''' \n and " + res
                #     res = ask_coder(message) 
                #     resDict[ele] = res                   
 
                if ele not in KeysList:
                    KeysList.append(ele) 
           
                resDict[ele] = res
    if returnDict:
        save_res(Folder , resDict)
        return resDict
    
    else:
        
        save_res(Folder , resDict)
            
        
     
if __name__ == '__main__':
    
    AnalyzeFolder()
    
    

 

 
 