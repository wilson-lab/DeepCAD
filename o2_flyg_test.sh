#!/bin/bash
#SBATCH --partition gpu_quad               # Use a quad GPU
#SBATCH --gres=gpu:rtx8000:1               # Number to use
#SBATCH --time=4-00:00                     # Runtime in D-HH:MM format
#SBATCH --mem=100GB                        # Memory total (for all cores)
#SBATCH -o jobs/deepcad_test_%j.out             # File to which STDOUT will be written, including job ID (%j)
#SBATCH -e jobs/deepcad_test_%j.err             # File to which STDERR will be written, including job ID (%j)

start=`date +%s`

module load gcc/6.2.0 
module load cuda/10.2 
module load miniconda3/4.10.3 
module load python/3.6.0

/n/cluster/bin/job_gpu_monitor.sh &

cd DeepCAD_pytorch
echo "activate deepcad"
source activate deepcad
echo "deepcad test initiated"
python test.py --denoise_model 'ModelForPytorch'\
               --datasets_folder 'time_slices_ch1_trial_001' --datasets_path '/n/data1/hms/neurobio/wilson/DeepCAD_datasets/20230811-1_EK021_7f_infinite_bar_methyl_salicylate/'\
               --pth_path '/n/data1/hms/neurobio/wilson/DeepCAD_datasets/pth/' --output_dir '/n/data1/hms/neurobio/wilson/DeepCAD_datasets/20230811-1_EK021_7f_infinite_bar_methyl_salicylate/'\
               --test_datasize 10000000 \
               --img_h 25 --img_w 25 --img_s 25 --gap_h 15 --gap_w 15 --gap_s 15 
echo "deepcad test complete"

end=`date +%s`
runtime=$((end-start))
echo "script completed in: "
echo $runtime