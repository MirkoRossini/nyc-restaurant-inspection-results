cmake_minimum_required(VERSION 3.8)

project(crow-app)

#include(/vcpkg/scripts/buildsystems/vcpkg.cmake)

find_package(Crow CONFIG REQUIRED)

add_executable(main "main.cpp")

target_link_libraries(main PUBLIC Crow::Crow)
