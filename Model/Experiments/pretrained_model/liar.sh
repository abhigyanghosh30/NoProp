#!/bin/bash

#SBATCH --job-name=liar_pretrain
#SBATCH -A research
#SBATCH -p long
#SBATCH -c 20
#SBATCH -t 4-00:00:00
#SBATCH --gres=gpu:4
#SBATCH --ntasks 1
#SBATCH --mem-per-cpu=3G
#SBATCH --output liar_pretrain_out
#SBATCH --mail-type=END
#SBATCH --mail-user=sravani.boinepelli@research.iiit.ac.in


## The following sends a SIGHUP signal 900 seconds before the job
## gets sent a kill signal on TimeOut. We can thus premptively clean
## up and export any data saved automatically.

## It is possible to use SIGUSR1, SIGUSR2 as well.

#SBATCH --signal=B:HUP@900

env | grep GPU
echo $CUDA_VISIBLE_DEVICES

# conda install pytorch torchvision cudatoolkit=10.2 -c pytorch

module load cuda/10.1
# module load cudnn/7.6.5-cuda-10.1
# pip install git+https://github.com/huggingface/transformers
# pip list | grep -E 'transformers|tokenizers'

#pip install -U tranformers==2.8
#pip install -U torch==1.6.0
echo "load done"

# should contain pretrain output folder, .csv and .py files
scp -r sravaniboinepelli@ada.iiit.ac.in:/share1/sravaniboinepelli/liar /scratch
echo "transfer done"
cd /scratch/liar

USER="sravaniboinepelli"
REMOTE_DIR="/home/sravaniboinepelli/tout_logs"
echo $User
echo $REMOTE_DIR

## We trap the SIGHUP signal and register a handler, which saves computed checkpoint
## In my case.
function _export {
    echo "export called"
    scp -r results_train_sc2 sravaniboinepelli@ada.iiit.ac.in:/share1/sravaniboinepelli/liar

    # ssh $USER@ada "mkdir -p $REMOTE_DIR/"
    # rsync -rz pretrain3_rsdd_train_out ada:$REMOTE_DIR/

}
trap "_export" SIGHUP

echo "running script"
python liar_sc_train_v5.py n &
wait
scp -r results_train_sc2 sravaniboinepelli@ada.iiit.ac.in:/share1/sravaniboinepelli/liar
