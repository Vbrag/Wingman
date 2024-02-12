conda create -n pytorch python=3.10  
conda activate pytorch 
conda env update --file environment.yml --prune
python -c "import torch; print(torch.cuda.is_available())"

 


 
 