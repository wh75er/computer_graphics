#!/bin/sh
make clean 2>> /dev/null
g++ -Wno-deprecated-declarations -rdynamic -o main.out main.cpp $(pkg-config --cflags --libs gtk+-3.0 gladeui-2.0)
