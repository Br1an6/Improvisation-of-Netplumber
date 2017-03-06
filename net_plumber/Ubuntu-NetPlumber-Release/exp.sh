#!/bin/bash
hdrs=( xxxxxxxx,xxxxxxxx,xxxxxxxx,xxxxxxxx,xxxxxxxx,xxxxxxxx,xxxxxxxx,xxxxxxxx,xxxxxxxx,xxxxxxxx,xxxxxxxx 
xxxxxxxx,xxxxxxxx,xxxxxxxx,00001010,11110011,111xxxxx,xxxxxxxx,xxxxxxxx,xxxxxxxx,xxxxxxxx,xxxxxxxx 
xxxxxxxx,xxxxxxxx,xxxxxxxx,00001010,11110011,110xxxxx,xxxxxxxx,xxxxxxxx,xxxxxxxx,xxxxxxxx,xxxxxxxx 
xxxxxxxx,xxxxxxxx,xxxxxxxx,00001010,11110011,1110xxxx,xxxxxxxx,xxxxxxxx,xxxxxxxx,xxxxxxxx,xxxxxxxx 
xxxxxxxx,xxxxxxxx,xxxxxxxx,00001010,11110011,1111xxxx,xxxxxxxx,xxxxxxxx,xxxxxxxx,xxxxxxxx,xxxxxxxx 
xxxxxxxx,xxxxxxxx,xxxxxxxx,00001010,11110011,11110xxx,xxxxxxxx,xxxxxxxx,xxxxxxxx,xxxxxxxx,xxxxxxxx 
xxxxxxxx,xxxxxxxx,xxxxxxxx,00001010,11110011,11111xxx,xxxxxxxx,xxxxxxxx,xxxxxxxx,xxxxxxxx,xxxxxxxx 
xxxxxxxx,xxxxxxxx,xxxxxxxx,00001010,11110011,111100xx,xxxxxxxx,xxxxxxxx,xxxxxxxx,xxxxxxxx,xxxxxxxx 
xxxxxxxx,xxxxxxxx,xxxxxxxx,00001010,11110011,111101xx,xxxxxxxx,xxxxxxxx,xxxxxxxx,xxxxxxxx,xxxxxxxx 
xxxxxxxx,xxxxxxxx,xxxxxxxx,00001010,11110011,111110xx,xxxxxxxx,xxxxxxxx,xxxxxxxx,xxxxxxxx,xxxxxxxx 
xxxxxxxx,xxxxxxxx,xxxxxxxx,00001010,11110011,111111xx,xxxxxxxx,xxxxxxxx,xxxxxxxx,xxxxxxxx,xxxxxxxx 
xxxxxxxx,xxxxxxxx,xxxxxxxx,00001010,11110011,1111000x,xxxxxxxx,xxxxxxxx,xxxxxxxx,xxxxxxxx,xxxxxxxx 
xxxxxxxx,xxxxxxxx,xxxxxxxx,00001010,11110011,1111001x,xxxxxxxx,xxxxxxxx,xxxxxxxx,xxxxxxxx,xxxxxxxx 
xxxxxxxx,xxxxxxxx,xxxxxxxx,00001010,11110011,11110010,xxxxxxxx,xxxxxxxx,xxxxxxxx,xxxxxxxx,xxxxxxxx 
xxxxxxxx,xxxxxxxx,xxxxxxxx,00001010,11110011,11110011,xxxxxxxx,xxxxxxxx,xxxxxxxx,xxxxxxxx,xxxxxxxx )
for hdr in "${hdrs[@]}" 
do
	./net_plumber --load /home/peymank/workspace/open-source/hassel/hsa-python/examples/google/google_sdn_tfs --policy /home/peymank//workspace/open-source/hassel/hsa-python/examples/google/policy.json --hdr-len 11 --filter $hdr
done
