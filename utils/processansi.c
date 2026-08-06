#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define WIDTH  96
#define HEIGHT 20

bool letter(char c) {
    return (c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z');
}

int main() {
    if (isatty(fileno(stdin))) return 1;
    char term[WIDTH * HEIGHT];
    memset(term, ' ', sizeof(term));
    int x = 0, y = 0;
    signed char c;
    while ((c = getchar()) != -1) {
        if (c == '\e') {
            getchar(); // [
            char number[128];
            int n = 0;
            while (!letter(c = getchar())) {
                number[n++] = c;
            }
            number[n] = 0;
            int num = atoi(number);
            switch (c) {
                case 'A':
                    y -= num;
                    if (y < 0) y = 0;
                    break;
                case 'B':
                    y += num;
                    if (y >= HEIGHT) y = HEIGHT - 1;
                    break;
                case 'C':
                    x += num;
                    if (x >= WIDTH) x = WIDTH - 1;
                    break;
                case 'D':
                    x -= num;
                    if (x < WIDTH) x = 0;
                    break;
            }
        }
        else if (c == '\r') x = 0;
        else if (c == '\n') {
            x = 0;
            y++;
            if (y == HEIGHT) y--;
        }
        else {
            term[y * WIDTH + x] = c;
            x++;
            if (x == WIDTH) {
                x = 0;
                y++;
                if (y == HEIGHT) y--;
            }
        }
    }
    for (int i = 0; i < HEIGHT; i++) {
        for (int j = 0; j < WIDTH; j++) {
            printf("%c", term[i * WIDTH + j]);
        }
        printf("\n");
    }
    return 0;
}
