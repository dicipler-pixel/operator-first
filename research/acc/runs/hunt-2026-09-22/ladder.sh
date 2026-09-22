#!/bin/sh
row=$1; args=$(grep "^$row " rows.args | cut -d' ' -f2-)
echo "=== $row ==="
for C in 19 20 21 22 23 24 25 26; do
  if [ $C -le 22 ]; then B=5000000; elif [ $C -le 24 ]; then B=20000000; else B=50000000; fi
  out=$(./acc_close $C $B $args)
  echo "$out"
  case "$out" in *BUDGET*) break;; esac
done
