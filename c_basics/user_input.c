#include <stdio.h>

int main(){

    int age;
    printf("Enter your age: ");
    scanf("%d", &age);
    #include <stdio.h>

    // Float input
    float height;
    printf("Enter your height (in meters): ");
    scanf("%f", &height);

    // Character input
    char initial;
    printf("Enter your first initial: ");
    scanf(" %c", &initial);

    // String input
    char name[50];
    printf("Enter your full name: ");
    scanf(" %[^\n]", name);

    // Printing input values
    printf("\n--- Your Information ---\n");
    printf("Age: %d years\n", age);
    printf("Height: %.2f meters\n", height);
    printf("Initial: %c\n", initial);
    printf("Name: %s\n", name);

    return 0;
}