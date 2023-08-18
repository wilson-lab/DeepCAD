#!/bin/bash
#SBATCH -c 4                               # Request cores
#SBATCH -p gpu_quad                        # Use a quad GPU
#SBATCH --gres=gpu:1                       # Number to use
#SBATCH -t 2-00:00                         # Runtime in D-HH:MM format
#SBATCH --mem=50GB                         # Memory total in MiB (for all cores)
#SBATCH -o jobs/deepcad_%j.out               # File to which STDOUT will be written, including job ID (%j)
#SBATCH -e jobs/deepcad_%j.err               # File to which STDERR will be written, including job ID (%j)

module load gcc/6.2.0 cuda/10.2 miniconda3/4.10.3 python/3.6.0

/n/cluster/bin/job_gpu_monitor.sh &        # collect information about the actual GPU utilization

conda init bash
conda activate deepcad
python DeepCAD_pytorch /script.py train
echo "deepcad train complete"
python DeepCAD_pytorch /script.py test
echo "deepcad test complete"