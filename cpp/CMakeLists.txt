cmake_minimum_required(VERSION 3.15)
project(cpp_module LANGUAGES CXX)

set(pybind11_DIR C:/Python311/Lib/site-packages/pybind11/share/cmake/pybind11)
find_package(pybind11 REQUIRED)

pybind11_add_module(cpp_module cpp_module.cpp)