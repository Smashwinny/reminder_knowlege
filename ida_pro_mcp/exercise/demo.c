#include <stdio.h>
#include <stdlib.h>

/* 自己编写的最小程序：只用于本地静态分析实验。 */
static int mix(int value) {
    return (value * 3) ^ 0x5a;
}

static int check(int value) {
    return mix(value) > 20;
}

int authorize(int value) {
    if (!check(value)) {
        return 0;
    }
    return mix(value + 1);
}

int main(int argc, char **argv) {
    int input = argc > 1 ? atoi(argv[1]) : 7;
    int token = authorize(input);
    int decision = token != 0;
    printf("input=%d decision=%d token=%d\n", input, decision, token);
    return decision ? 0 : 2;
}
