docker run --gpus all --rm --name dcan-run -it \
 --mount type=bind,src=$(pwd),dst=/root/backend/ \
 cdx_bupt/pytorch-py36-cu102:1.0 bash