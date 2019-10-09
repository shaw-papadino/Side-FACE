#!/bin/bash

ROOT_PATH=$1
IMAGE_LENGTH=`wc ${ROOT_PATH}/positive.dat`
BG_LENGTH=`wc ${ROOT_PATH}/negative.dat`

opencv_createsamples -info ${ROOT_PATH}/positive.dat -vec ${ROOT_PATH}/positive.vec -num ${IMAGE_LENGTH} -w 45 -h 45
wait $!
mkdir ${ROOT_PATH}/cascade
wait $!
nohup opencv_traincascade -data ${ROOT_PATH}/cascade/ -vec ${ROOT_PATH}/positive.vec -bg negative.dat -numPos ${IMAGE_LENGTH} -numNeg ${BG_LENGTH} -w 45 -h 45 -featureType LBP -minHitRate 0.997 &

