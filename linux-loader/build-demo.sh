#Build the loader
gcc -g -Wall -m32 -o loader.out loader.c -ldl
#build the test binary
gcc -fPIE -fPIC -DPIC -pie -m32 -fno-stack-protector -o test.out test.c

