#!/bin/bash

for file in results/*.log;do
    gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dSAFER -sOutputFile=results/tmp.pdf "${file}".*.ps
    convert -size 700x850 -alpha deactivate -delay 30 -loop 0 results/tmp.pdf "gifs/$(basename ${file}).gif"
    rm results/tmp.pdf
done
