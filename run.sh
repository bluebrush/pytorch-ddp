set -x
echo "Testing.. test1-b256.py"
python test1-b256.py

echo "Testing.. test2-b10240.py"
python -m torch.distributed.launch --nproc_per_node=4 test2-b10240.py

echo "Testing.. test3-20480.py"
python -m torch.distributed.launch --nproc_per_node=8 test3-20480.py
