#!/bin/bash

find ./*/rtl -type f -name "*.sv" | xargs realpath > filelist.txt

