# Wingman
 A simple Copilot-like assistant to run on a local LLM
 This explanation is Ai generated, so it might not be 100% accurate. 

 Wingman is a simple, lightweight, and extensible Copilot-like assistant that runs on a local Large Language Model (LLM). It's designed to provide a user-friendly interface for interacting with the LLM, and to extend its functionality by adding customizable features.
 
 Here's a more detailed explanation:
 
 1. **User-Friendly Interface:** not very much put it helps
 
 2. **Customizable Features:** Wingman allows users to customize its functionality by adding customizable features. This includes the ability to add commands, change the context of the assistant, and even create custom prompts.
 
 3. **Extensibility:** Wingman is designed to be extensible. This means that it can be easily extended to add new features or capabilities. This is done by adding new Python modules to the Wingman package, and then adding those modules to the PATH of the Python interpreter.
 
 4. **LLM Integration:** Wingman can be integrated with any LLM, With a focus on running the model locally, if you have GPU.
 
 5. **Security and Privacy:** running the model locally 
 
 In summary, Wingman is a powerful tool for anyone looking to create a Copilot-like assistant on a local LLM. It's designed to be simple, extensible, and secure, making it a great tool for anyone looking to create a conversational AI assistant for coding.
 
 
#Basically, it loads a deepseek-coder model and spelling-correction model and sends input to them through the Clipboard .



# hotkey 'ctrl+x' 
cut send to clipboard
# hotkey 'ctrl+c' 
copy  send to clipboard
# hotkeys 'ctrl+shift+alt+W' 
 Write Response  from clipboard to deepseek-coder  to keyboard
# hotkeys 'ctrl+shift+alt+V'
Paste Response from clipboard to deepseek-coder  to clipboard
# hotkeys 'ctrl+shift+alt+S' 
Fix Spelling from clipboard to spelling-correction model to keyboard
# hotkeys 'ctrl+shift+alt+N' 
Intialize
 
# Download Models

Download  from `https://huggingface.co/deepseek-ai/deepseek-coder-1.3b-instruct/tree/main` ==>    `C:\Models\deepseek-coder-1.3b`
 
Download  from  `https://huggingface.co/oliverguhr/spelling-correction-multilingual-base/tree/main`   ==>    `C:\Models\spelling-correction-multilingual-base`  



#Install anaconda.
To install Anaconda, you can follow these steps:

1. Visit the Anaconda website (https://www.anaconda.com/products/distribution) and download the appropriate installer for your operating system.

2. Run the installer and follow the prompts to install Anaconda.

3. After installation, you can verify the installation by opening a new terminal window and typing `conda --version`. This should display the version of Anaconda installed.

4. If you want to use Python 3, you can set the default Python version in Anaconda by running `conda config --set default_python_version 3`.

5. To install additional packages, you can use the `conda install` command followed by the name of the package. For example, to install the NumPy package, you would run `conda install numpy`.Remember, Anaconda is a distribution of the Python and R programming languages for scientific computing, that aims to simplify package management and deployment.

6. After installation, open the Anaconda Prompt by searching it in the start menu.

7. run Setup.bat

8. conda activate pytorch 

9. run.bat

 

 

 