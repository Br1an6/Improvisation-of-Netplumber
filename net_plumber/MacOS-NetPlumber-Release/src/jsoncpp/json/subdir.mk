################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
CC_SRCS += \
../src/jsoncpp/json/dummy.cc 

OBJS += \
./src/jsoncpp/json/dummy.o 

CC_DEPS += \
./src/jsoncpp/json/dummy.d 


# Each subdirectory must supply rules for building sources it contributes
src/jsoncpp/json/%.o: ../src/jsoncpp/json/%.cc
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -DJSON_IS_AMALGAMATION -I/usr/local/include/ -O3 -Wall -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


