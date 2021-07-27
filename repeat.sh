#!/bin/bash

# if repeat-count or command are missing or if repeat-count isnt a number
if [[ "$#" -le 1 || ! "$1" =~ ^[0-9]+$ ]]
then
    echo >/dev/stderr "Usage: $0 repeat-count command [args..]"
    exit 1
fi

# take out first arg to then use "$@" to run with args
reps="$1"
shift 1

for (( i = 0; i < "$reps"; ++i ))
do
    export BLA_REPEAT="$i"
    "$@"
done
