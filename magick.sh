#!/bin/bash

for file in results/*.log;do
    convert -verbose -delay 100 "${file}"*.ps "${file}".gif 2>&1 | grep -oP '(?<=\.)[^.]*\.[^.]*\.ps'
done
