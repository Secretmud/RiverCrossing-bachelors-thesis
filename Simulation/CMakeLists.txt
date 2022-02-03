cmake_minimum_required(VERSION 3.21)
project(Simulation)

set(CMAKE_CXX_STANDARD 23)

add_executable(Simulation main.cpp LibAnt/ant.cpp.h)
