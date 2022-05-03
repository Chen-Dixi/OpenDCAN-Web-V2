docker run --gpus all --rm --name dcan-run -it \
 --mount type=bind,src=$(pwd),dst=/root/backend/ \
 chendixi/torch190_zsh:latest