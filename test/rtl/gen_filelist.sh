#!/bin/bash

find . -type f -name "*.sv" | xargs realpath > filelist.txt

