################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
CPP_SRCS += \
../src/jsoncpp/jsoncpp.cpp \
../src/jsoncpp/jsonrpc_client.cpp \
../src/jsoncpp/jsonrpc_handler.cpp \
../src/jsoncpp/jsonrpc_server.cpp \
../src/jsoncpp/jsonrpc_tcpclient.cpp \
../src/jsoncpp/jsonrpc_tcpserver.cpp \
../src/jsoncpp/jsonrpc_udpclient.cpp \
../src/jsoncpp/jsonrpc_udpserver.cpp \
../src/jsoncpp/netstring.cpp \
../src/jsoncpp/networking.cpp \
../src/jsoncpp/system.cpp 

OBJS += \
./src/jsoncpp/jsoncpp.o \
./src/jsoncpp/jsonrpc_client.o \
./src/jsoncpp/jsonrpc_handler.o \
./src/jsoncpp/jsonrpc_server.o \
./src/jsoncpp/jsonrpc_tcpclient.o \
./src/jsoncpp/jsonrpc_tcpserver.o \
./src/jsoncpp/jsonrpc_udpclient.o \
./src/jsoncpp/jsonrpc_udpserver.o \
./src/jsoncpp/netstring.o \
./src/jsoncpp/networking.o \
./src/jsoncpp/system.o 

CPP_DEPS += \
./src/jsoncpp/jsoncpp.d \
./src/jsoncpp/jsonrpc_client.d \
./src/jsoncpp/jsonrpc_handler.d \
./src/jsoncpp/jsonrpc_server.d \
./src/jsoncpp/jsonrpc_tcpclient.d \
./src/jsoncpp/jsonrpc_tcpserver.d \
./src/jsoncpp/jsonrpc_udpclient.d \
./src/jsoncpp/jsonrpc_udpserver.d \
./src/jsoncpp/netstring.d \
./src/jsoncpp/networking.d \
./src/jsoncpp/system.d 


# Each subdirectory must supply rules for building sources it contributes
src/jsoncpp/%.o: ../src/jsoncpp/%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -DJSON_IS_AMALGAMATION -I/usr/include/ -O3 -Wall -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


