#!/bin/bash
#SBATCH --partition gpu_quad               # Use a quad GPU
#SBATCH --gres=gpu:rtx8000:1               # Number to use
#SBATCH --time=4-00:00                     # Runtime in D-HH:MM format
#SBATCH --mem=100GB                        # Memory total (for all cores)
#SBATCH -o jobs/deepcad_train_%j.out             # File to which STDOUT will be written, including job ID (%j)
#SBATCH -e jobs/deepcad_train_%j.err             # File to which STDERR will be written, including job ID (%j)

start=`date +%s`

module load gcc/6.2.0 
module load cuda/10.2 
module load miniconda3/4.10.3 
module load python/3.6.0

cd DeepCAD_pytorch
echo "activate deepcad"
source activate deepcad
echo "deepcad train initiated"
python train.py --train_datasets_size 6000 --output_dir '/n/data1/hms/neurobio/wilson/DeepCAD_datasets/20230811-1_EK021_7f_infinite_bar_methyl_salicylate/train' \
               --datasets_folder 'time_slices_ch1_trial_001' --datasets_path '/n/data1/hms/neurobio/wilson/DeepCAD_datasets/20230811-1_EK021_7f_infinite_bar_methyl_salicylate/'\
               --pth_path '/n/data1/hms/neurobio/wilson/DeepCAD_datasets/20230811-1_EK021_7f_infinite_bar_methyl_salicylate/pth/' \
               --img_h 30 --img_w 30 --img_s 30 --gap_h 18 --gap_w 18 --gap_s 18 
echo "deepcad train complete"

end=`date +%s`
runtime=$((end-start))
echo "script completed in: "
echo $runtime