#!/bin/bash
#SBATCH -c 1                               # Use a CPU
#SBATCH --partition gpu_quad               # Use a quad GPU
#SBATCH --gres=gpu:rtx8000:1               # Number to use
#SBATCH --time=4-00:00                     # Runtime in D-HH:MM format
#SBATCH --mem=100GB                        # Memory total (for all cores)
#SBATCH -o jobs/deepcad_%j.out             # File to which STDOUT will be written, including job ID (%j)
#SBATCH -e jobs/deepcad_%j.err             # File to which STDERR will be written, including job ID (%j)

start=`date +%s`

module load gcc/6.2.0 
module load cuda/10.2 
module load miniconda3/4.10.3 
module load python/3.6.0

cd DeepCAD_pytorch
source activate deepcad
python script.py train
echo "deepcad train complete"
python script.py test
echo "deepcad test complete"

end=`date +%s`
runtime=$((end-start))
echo "script completed in: "
echo $runtime
