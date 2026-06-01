#!/bin/sh
set -e
DIR="$(dirname "$0")"
gcc -Wall -Wextra -Werror -std=c11 -I"$DIR/include" -c "$DIR/src/lau_conservation.c" -o "$DIR/src/lau_conservation.o"
ar rcs "$DIR/liblau_conservation.a" "$DIR/src/lau_conservation.o"
gcc -Wall -Wextra -Werror -std=c11 -I"$DIR/include" "$DIR/tests/test_basic.c" -L"$DIR" -llau_conservation -lm -o "$DIR/tests/test_basic"
"$DIR/tests/test_basic"
