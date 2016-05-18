#!/usr/bin/python
import ctypes
from ctypes import CDLL, c_char_p, c_void_p, memmove, cast, CFUNCTYPE
shellcode_data = (b"\xe9\x1e\x00\x00\x00\xb8\x04\x00\x00\x00\xbb\x01\x00\x00\x00"
b"\x59\xba\x0f\x00\x00\x00\xcd\x80\xb8\x01\x00\x00\x00\xbb\x00\x00\x00\x00"
b"\xcd\x80\xe8\xdd\xff\xff\xffHello wolrd!\r\n")

shellcode = shellcode_data # ctypes.c_char_p(shellcode_data)

libc = CDLL('libc.so.6')

sc = c_char_p(shellcode)
size = len(shellcode)
addr = c_void_p(libc.valloc(size))
memmove(addr, sc, size)
libc.mprotect(addr, size, 0x7)
run = cast(addr, CFUNCTYPE(c_void_p))
run()
