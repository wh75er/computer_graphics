#!/bin/sh
rm *.out 2>> /dev/null
g++ -g -Wno-deprecated-declarations -rdynamic -o main.out main.cpp $(pkg-config --cflags --libs gtk+-3.0 gladeui-2.0)
./main.out 2>> /dev/null
rm *.out 2>> /dev/null
