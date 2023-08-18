#!/bin/bash
#SBATCH -c 1                               # Request one core
#SBATCH -p gpu_quad                        # Use a quad GPU
#SBATCH --gres=gpu:1                       # Number to use
#SBATCH -t 2-00:00                         # Runtime in D-HH:MM format
#SBATCH -p medium                          # Partition to run in
#SBATCH --mem=50GB                         # Memory total in MiB (for all cores)
#SBATCH -o hostname_%j.out                 # File to which STDOUT will be written, including job ID (%j)
#SBATCH -e hostname_%j.err                 # File to which STDERR will be written, including job ID (%j)

module load gcc/6.2.0 cuda/10.2 miniconda3/4.10.3 python/3.6.0

/n/cluster/bin/job_gpu_monitor.sh &        # collect information about the actual GPU utilization

srun -c 1 cd /home/ab714/DeepCAD/DeepCAD_pytorch/
srun -c 1 conda activate deep-cad
python script.py train
srun -c 1 echo "deepcad train complete"
python script.py test
srun -c 1 echo "deepcad test complete"