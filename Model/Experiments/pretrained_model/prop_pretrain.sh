#!/bin/bash

#SBATCH --job-name=prop_pretrain
#SBATCH -A research
#SBATCH -p long
#SBATCH -c 20
#SBATCH -t 4-00:00:00
#SBATCH --gres=gpu:4
#SBATCH --ntasks 1
#SBATCH --mem-per-cpu=4G
#SBATCH --output prop_pretrain
#SBATCH --mail-type=END
#SBATCH --mail-user=sravani.boinepelli@research.iiit.ac.in


## The following sends a SIGHUP signal 900 seconds before the job
## gets sent a kill signal on TimeOut. We can thus premptively clean
## up and export any data saved automatically.

## It is possible to use SIGUSR1, SIGUSR2 as well.

#SBATCH --signal=B:HUP@900

env | grep GPU
echo $CUDA_VISIBLE_DEVICES

module load cuda/10.1


echo "load done"


cd /scratch

scp -r sravaniboinepelli@ada.iiit.ac.in:/share1/sravaniboinepelli/prop_pretrain /scratch

echo "transfer done"
cd /scratch/prop_pretrain


USER="sravaniboinepelli"

echo $User
echo $REMOTE_DIR

## We trap the SIGHUP signal and register a handler, which saves computed checkpoint
## In my case.
function _export {
    echo " timeout and export  function called"  
    scp -r prop_v0 sravaniboinepelli@ada.iiit.ac.in:/share1/sravaniboinepelli/prop_pretrain
    scp -r prop_new_v0 sravaniboinepelli@ada.iiit.ac.in:/share1/sravaniboinepelli/prop_pretrain
    #scp tmp2_pre_train_file.csv sravaniboinepelli@ada.iiit.ac.in:/share1/sravaniboinepelli/prop_pretrain


}
trap "_export" SIGHUP

echo "running script"
# python get_prop_pretrain.py training.csv&
python prop_pretrain.py &


wait
# scp log_bert_server sravaniboinepelli@ada.iiit.ac.in:/home/sravaniboinepelli
 scp -r prop_new_v0 sravaniboinepelli@ada.iiit.ac.in:/share1/sravaniboinepelli/prop_pretrain
 scp -r prop_v0 sravaniboinepelli@ada.iiit.ac.in:/share1/sravaniboinepelli/prop_pretrain
 #scp tmp2_pre_train_file.csv sravaniboinepelli@ada.iiit.ac.in:/share1/sravaniboinepelli/prop_pretrain
