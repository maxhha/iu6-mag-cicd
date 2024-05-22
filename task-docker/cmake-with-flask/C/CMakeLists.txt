project(C)


add_executable(C main.cpp)

target_link_libraries(C ClassLib)
target_include_directories(C PRIVATE ${Task6_SOURCE_DIR})

