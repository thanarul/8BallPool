CC = clang
CFLAGS = -std=c99 -Wall -pedantic
LDFLAGS=-shared

all: _phylib.so phylib.py

clean:
	rm -f *.o *.so phylib.py phylib_wrap.c

phylib_wrap.o: phylib_wrap.c
	$(CC) $(CFLAGS) -fPIC -c phylib_wrap.c -I/usr/include/python3.11/ -o phylib_wrap.o

phylib_wrap.c: phylib.i
	swig -python phylib.i

libphylib.so: phylib.o 
	$(CC) $(LDFLAGS) phylib.o -o libphylib.so -lm

phylib.o: phylib.c phylib.h
	$(CC) $(CFLAGS) -fPIC -c phylib.c -o phylib.o

_phylib.so: phylib_wrap.o libphylib.so
	$(CC) $(LDFLAGS) phylib_wrap.o -L. -L/usr/lib/python3.11 -lpython3.11 -lphylib -o _phylib.so
