cmake_minimum_required(VERSION 3.5)

project(Task6)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${Task6_SOURCE_DIR}/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${Task6_SOURCE_DIR}/lib)

add_subdirectory(B)
add_subdirectory(C)

