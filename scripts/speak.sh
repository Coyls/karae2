#!/bin/bash
pico2wave -l fr-FR -w ./tmp/speak.wav "$1"
aplay -q ./tmp/speak.wav
rm ./tmp/speak.wav