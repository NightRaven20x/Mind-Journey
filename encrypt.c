#include <stdio.h>
#include <string.h>

// Function to encrypt a single character
char encrypt_char(char c, int shift) {
    if (c >= 'A' && c <= 'Z') {
        return ((c - 'A' + shift) % 26) + 'A';
    }
    
    if (c >= 'a' && c <= 'z') {
        return ((c - 'a' + shift) % 26) + 'a';
    }
    
    return c;
}

int main() {
    char password[100];
    int shift = 3;  // Always shift by 3!
    
    // Get password from user
    scanf("%s", password);
    
    // Encrypt each character
    for (int i = 0; i < strlen(password); i++) {
        char encrypted = encrypt_char(password[i], shift);
        printf("%c", encrypted);
    }
    printf("\n");
    
    return 0;
}