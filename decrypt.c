#include <stdio.h>
#include <string.h>

// Function to decrypt a single character (shift backwards)
char decrypt_char(char c, int shift) {
    // For uppercase letters
    if (c >= 'A' && c <= 'Z') {
        // Shift backwards and wrap around
        int pos = c - 'A';
        int new_pos = (pos - shift + 26) % 26;  // +26 to handle negative numbers
        return new_pos + 'A';
    }
    
    // For lowercase letters
    if (c >= 'a' && c <= 'z') {
        int pos = c - 'a';
        int new_pos = (pos - shift + 26) % 26;
        return new_pos + 'a';
    }
    
    // If not a letter, return unchanged
    return c;
}

int main() {
    char encrypted_password[100];
    int shift = 3;  // Same shift as encryption
    
    // Get encrypted password from input
    scanf("%s", encrypted_password);
    
    // Decrypt each character
    for (int i = 0; i < strlen(encrypted_password); i++) {
        char decrypted = decrypt_char(encrypted_password[i], shift);
        printf("%c", decrypted);
    }
    printf("\n");
    
    return 0;
}