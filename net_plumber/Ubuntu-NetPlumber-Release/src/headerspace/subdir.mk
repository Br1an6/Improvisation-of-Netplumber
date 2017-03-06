################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../src/headerspace/array.c \
../src/headerspace/hs.c 

OBJS += \
./src/headerspace/array.o \
./src/headerspace/hs.o 

C_DEPS += \
./src/headerspace/array.d \
./src/headerspace/hs.d 


# Each subdirectory must supply rules for building sources it contributes
src/headerspace/%.o: ../src/headerspace/%.c
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C Compiler'
	gcc -O3 -Wall -c -fmessage-length=0 -std=gnu99 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


