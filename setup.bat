conda create -n pytorch python=3.10 -f environment.yml
conda activate pytorch 
python -c "import torch; print(torch.cuda.is_available()))"
 
 