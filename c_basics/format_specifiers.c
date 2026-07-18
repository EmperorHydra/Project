#include <stdio.h>

int main() {

    int age = 25;
    printf("Integer (decimal): %d\n", age);
    printf("Integer (hexadecimal): %x\n", age);
    printf("Integer(octal): %o\n", age);

    float temperature = 98.6;
    printf("Float (default): %f\n", temperature);
    printf("Float (2 decimal places): %.2f\n",temperature);
    printf("Float (scientific notation): %e\n", temperature);

    char grade = 'A';
    char name[] = "John Doe";
    printf("Character: %c\n", grade);
    printf("String: %s\n", name);

    printf("Right-aligned integer (width 5): %5d\n", age);
    printf("Left-aligned string (width 10): %-10s\n", name);

    return 0;
}
