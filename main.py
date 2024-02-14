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
spelling = r"C:\Models\spelling-correction-multilingual-base" # Download https://huggingface.co/oliverguhr/spelling-correction-multilingual-base/tree/main


tokenizer_coder = AutoTokenizer.from_pretrained(coder , trust_remote_code=True)
model_coder = AutoModelForCausalLM.from_pretrained(coder , trust_remote_code=True, torch_dtype=torch.bfloat16).cuda()

 
 

fix_spelling_pipeline = pipeline("text2text-generation",model= spelling)


def fix_spelling(text, max_length = 256):
    return fix_spelling_pipeline("fix:"+text,max_length = max_length)



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
 
        yield "{}<h{}  style='color: Navy '>{}</h{}>".format('   '*(c +1),c,   a,c    )
        if isinstance(b, dict):
            yield '{}<ul>\n{}\n{}</ul>'.format('   '*c, "\n".join(to_html(b, c + 1)), '   '*c)
    
        else:
            yield b.replace('\n', '<br>')
              
        


 
# This code is a Python script that uses the Hugging Face's transformers library to load a pre-trained model for text generation and a spelling correction model. The AutoTokenizer and AutoModelForCausalLM classes are used to load the models. The pipeline function is used to create a text-to-text generation pipeline. The fix-spelling function is used to correct the spelling of a given text.
# Here's a brief explanation of the code.
#
#  - `coder = r"C:\Models\deepseek-coder-1.3b"` and `spelling = r"C:\Models\spelling-correction-multilingual-base"`: These lines are defining the paths to the pre-trained models.
#  - `tokenizer_coder = AutoTokenizer.from_pretrained(coder , trust_remote_code=True)` and `model_coder = AutoModelForCausalLM.from_pretrained(coder , trust_remote_code=True, torch_dtype=torch.bfloat16).cuda()`: These lines are loading the pre-trained models and converting them to the appropriate data types for the GPU.
#  - `fix_spelling_pipeline = pipeline("text2text-generation",model= spelling)`: This line is creating a text-to-text generation pipeline using the spelling correction model.
#
# Please note that the code is using the AutoTokenizer and AutoModelForCausalLM classes from the transformers library, which are part of the Hugging Face's transformers library. The pipeline function is a part of the transformers library, and the fix-spelling function is a custom function that uses the fix-spelling-pipeline to correct the spelling of a given text. 

 
# Define the Wingman class
#This code defines a class `Wingman` with methods to Initialize, add a message to the history, and get the content from the system's clipboard. The `Initialize` method is used to clear the current message and set the new content. The `add2messageHistory` method is used to add a message to the history. The `getCutclipboard` and `getclipboard` methods are used to get the content from the system's clipboard and clear the current message, respectively.
 
class Wingman:
    # Initialize the class
    def __init__(self):
        self.Initialize()

    # Method to Initialize the class
    def Initialize(self):
        # Initialize an empty list to store the history of messages
        self.messageHistory = []

        # Initialize an empty string to store the current message
        self.message = ""
        self.response = ""

    # Method to add a message to the history
    def add2messageHistory(self, message):
        # Check if the message is not already in the history
        if message not in self.messageHistory:
            # Append the message to the history
            self.messageHistory.append(message)

    # Method to get the content from the system's clipboard
    def getCutclipboard(self):
        print("Cut")
        # Get the content from the system's clipboard
        paste = pyperclip.paste()
        print(paste)

        # Clear the current message and set the new content
        self.Initialize()
        self.message = paste

    # Method to get the content from the system's clipboard
    def getclipboard(self):
        print("Copy")
        # Get the content from the system's clipboard
        paste = pyperclip.paste()
        print(paste)

        # Clear the current message and set the new content
        self.Initialize()
        self.message = paste
 
 
    # This function sends the response to the clipboard
    def send2clipboard(self):
        print("send2clipboard")
        # Assign the response to a variable
        response = self.response
        # Copy the response to the clipboard
        pyperclip.copy(response)
        
        
    
    
    #This code is a function that takes a message from the clipboard, applies a template to it, generates a response from the model, and then sends the response to the clipboard. The function is named `PasteResponse`.
    def PasteResponse(self):
        self.getclipboard() # Get the message from the clipboard

        # Create a list of messages. Each message is a dictionary with 'role' and 'content' keys.
        # 'role' is the role of the user, and 'content' is the message content.

 
        outputstr= ask_coder(self.message)
        
        #Rewrite this code with comments describing its behavior. 
        self.Response = outputstr   # Assign the output string to self.response 
        self.send2clipboard()# Call the method to send the content of self.response to the clipboard
        keyboard.press_and_release('ctrl+v') 



        
 

 
    # Define the function FixSpelling
    def FixSpelling(self , max_length = 512 ): 
        """This function `FixSpelling` is designed to correct the spelling in a given message. It first gets the clipboard content, then it calls the `fix_spelling_pipeline` function with the message as an argument. The result is stored in the `response` variable. The corrected text is then extracted from the first element of the `response` and written to the keyboard."""
        # Get the clipboard content
        self.getclipboard()
    
        # Call the function fix_spelling with self.message as argument
        # The result is stored in the variable response
        response =  fix_spelling_pipeline("fix:"+self.message,max_length = max_length)# fix_spelling(self.message) 
    
        # Get the 'generated_text' from the first element of the response
        # This is the corrected text
        self.response = response[0].get('generated_text')  
    
        # Write the corrected text to the keyboard
        keyboard.write(str(self.response))
 



   
 
 
    # Define the function WriteResponse
    def WriteResponse(self): 
        """This function is designed to take a user message, apply a chat template to it, generate a response from the model, decode the output, and then write the response to the clipboard."""
    
        # Get the clipboard content
        self.getclipboard()
 
        # Set the response
        self.response = ask_coder(self.message)
    
        # Get the response
        response = self.response 
    
        # Write the response to the clipboard
        keyboard.write( str(response)  )
    
        # Send the response to the clipboard
        self.send2clipboard()
 

    def AnalyzeFolder(self, Folder = None):
        
        ignoreList =[".git" ,".gitattributes" , ".gitignore" , ".project" , ".pydevproject" , ".settings"  ,".vs"]
        
        returnDict = True
        
        if Folder is None:
            returnDict = False
            self.getclipboard()
            Folder = self.message
        
        
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
        
                    fullpath = os.path.join(Folder,ele )
            
                    res = None
                    if os.path.isdir(fullpath):
            
                        res = self.AnalyzeFolder(fullpath)
            
            
                    elif os.path.isfile(fullpath):
                        try:
                            pass
            
                            data = ""
                            with open(fullpath, 'r') as file:
            
                                data = file.read()
            
                            if len(data) >0:
            
                                message = "Explain this '''"+data+"'''"
                                res = ask_coder(message)
                                
                                
                                
     
                            else:
            
                                res = "File is empty."
            
            
                        except:
                            res =  ele + "  is not Readable"
            
                    resDict[ele] = res
        if returnDict:
            return resDict
        
        else:
 
            # json file to write to
            
            data = '\n'.join(to_html(resDict))
            
            filename = os.path.join(Folder,'Report.json' ) 
            
            with open(filename, 'w') as f:
            
                json.dump(resDict, f)
            
                print(f"Data written to {filename}")
            #

            filename = os.path.join(Folder,'Report.html' )  
            with open(filename, 'w' , encoding="utf-8") as f:
                
                f.write(data)
                print(f"Data written to {filename}")
            
        
     
        
    def start(self):
        
 
        # This code is adding hotkeys to the keyboard that will trigger certain actions when they are pressed.
        # The actions are defined in the methods: getCutclipboard, getclipboard, WriteResponse, PasteResponse, FixSpelling, and Initialize.
        
        # Add the hotkey 'ctrl+x' to the keyboard that will trigger the getCutclipboard method
        keyboard.add_hotkey('ctrl+x', self.getCutclipboard)
        
        # Add the hotkey 'ctrl+c' to the keyboard that will trigger the getclipboard method
        keyboard.add_hotkey('ctrl+c', self.getclipboard)
        
        # Add the hotkeys 'ctrl+shift+alt+W', 'ctrl+shift+alt+V', 'ctrl+shift+alt+S', and 'ctrl+shift+alt+N' to the keyboard
        # that will trigger the corresponding methods: WriteResponse, PasteResponse, FixSpelling, and Initialize respectively
        keyboard.add_hotkey('ctrl+shift+alt+W', self.WriteResponse)
        keyboard.add_hotkey('ctrl+shift+alt+V', self.PasteResponse)
        keyboard.add_hotkey('ctrl+shift+alt+S', self.FixSpelling)
        keyboard.add_hotkey('ctrl+shift+alt+N', self.Initialize)
        keyboard.add_hotkey('ctrl+shift+alt+F', self.AnalyzeFolder)        
        # Print a message indicating that the program has started
        print("Started KeyWingman.")
        
        # Wait for a keypress, and then exit the program
        keyboard.wait()
 
 
 
# Check if this script is being run directly, not being imported as a module
if __name__ == '__main__':

    # Create an instance of the Wingman class
    Wingman = Wingman()

    # Start the interface
    Wingman.start()


 
 