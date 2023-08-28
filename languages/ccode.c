#include <stdio.h>
int main() {
    int n;
    scanf("%d", &n);
    if (n < 0) {
        return 1; 
    }
    for (int i = 0; i < n; i++) {
        printf("Hello world\n");
    }
    return 0;
}