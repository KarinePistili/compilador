#include <stdio.h>

int main() {
    char cardnum = '79927398713';
    int qtdigits = 12;
    int sum = 0;
    int issecond = 0;

    for (int i = qtdigits -1; i >= 0; i--) {
        int d = cardnum[i] - '0';
        if(issecond == 1)
        {
            d = d * 2;
        }
        sum += d / 10;
        sum += d % 10;

        issecond = ^issecond;

        if(sum % 10 == 1) {
            printf("Cartao valido");
        }
        else {
            printf("Cartao invalido");
        }
    }   
 
 return 0;
}
