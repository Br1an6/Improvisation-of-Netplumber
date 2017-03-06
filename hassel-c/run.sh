#!/bin/bash
set -e

NET=$1
if [[ ! "$1" ]]; then
  echo "Usage: $0 <network>"
  exit 0
fi

cd `dirname $0`
if [[ ! -d res ]]; then
  mkdir res
fi
if [[ ! -x $NET ]]; then
  echo "No executable $NET. You might need to run make."
  exit 1
fi

mkdir res/$NET
cd res/$NET

exec 3<../../ports/$NET
while read -u 3 p; do
  echo $p && ../../$NET $p &>$p
done

