CC = gcc
CFLAGS = -Wall -Wextra -std=c11 -D_GNU_SOURCE -Iinclude
SRCDIR = src
TESTDIR = tests

SOURCES = $(SRCDIR)/lattice.c $(SRCDIR)/funnel.c $(SRCDIR)/holonomy.c $(SRCDIR)/rigidity.c $(SRCDIR)/consensus.c

.PHONY: all clean test

all: libconstraintsubstrate.a

libconstraintsubstrate.a: $(SOURCES)
	$(CC) $(CFLAGS) -c $(SOURCES)
	ar rcs $@ *.o
	rm -f *.o

test: libconstraintsubstrate.a $(TESTDIR)/test_main.c
	$(CC) $(CFLAGS) -o test_runner $(TESTDIR)/test_main.c -L. -lconstraintsubstrate -lm
	./test_runner

clean:
	rm -f libconstraintsubstrate.a test_runner *.o
