################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
CC_SRCS += \
../src/net_plumber/conditions.cc \
../src/net_plumber/main.cc \
../src/net_plumber/main_processes.cc \
../src/net_plumber/net_plumber.cc \
../src/net_plumber/net_plumber_utils.cc \
../src/net_plumber/node.cc \
../src/net_plumber/rpc_handler.cc \
../src/net_plumber/rule_node.cc \
../src/net_plumber/source_node.cc \
../src/net_plumber/source_probe_node.cc 

OBJS += \
./src/net_plumber/conditions.o \
./src/net_plumber/main.o \
./src/net_plumber/main_processes.o \
./src/net_plumber/net_plumber.o \
./src/net_plumber/net_plumber_utils.o \
./src/net_plumber/node.o \
./src/net_plumber/rpc_handler.o \
./src/net_plumber/rule_node.o \
./src/net_plumber/source_node.o \
./src/net_plumber/source_probe_node.o 

CC_DEPS += \
./src/net_plumber/conditions.d \
./src/net_plumber/main.d \
./src/net_plumber/main_processes.d \
./src/net_plumber/net_plumber.d \
./src/net_plumber/net_plumber_utils.d \
./src/net_plumber/node.d \
./src/net_plumber/rpc_handler.d \
./src/net_plumber/rule_node.d \
./src/net_plumber/source_node.d \
./src/net_plumber/source_probe_node.d 


# Each subdirectory must supply rules for building sources it contributes
src/net_plumber/%.o: ../src/net_plumber/%.cc
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -DJSON_IS_AMALGAMATION -I/usr/include/ -O3 -Wall -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


