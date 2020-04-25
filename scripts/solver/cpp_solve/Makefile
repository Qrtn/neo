CC=clang++
CFLAGS=-std=c++11

DEPS = lightsout.h

OBJ = lightsout.o solve.o 

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

solve: $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS)

.PHONY: clean

clean:
	rm -f *.o *~ core
