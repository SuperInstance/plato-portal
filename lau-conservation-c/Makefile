CC      = gcc
CFLAGS  = -Wall -Wextra -Werror -std=c11
INC     = -Iinclude
LIB     = liblau_conservation.a
OBJ     = src/lau_conservation.o

all: $(LIB) tests/test_basic

$(OBJ): src/lau_conservation.c include/lau_conservation.h
	$(CC) $(CFLAGS) $(INC) -c $< -o $@

$(LIB): $(OBJ)
	ar rcs $@ $^

tests/test_basic: tests/test_basic.c $(LIB)
	$(CC) $(CFLAGS) $(INC) $< -L. -llau_conservation -lm -o $@

clean:
	rm -f $(OBJ) $(LIB) tests/test_basic

.PHONY: all clean
