/* Read-only score probe: includes the production implementation, no beam run. */
#define main unused_production_beam_main
#include "../../acc_beam.c"
#undef main

int main(void) {
    St s;
    unsigned n, v;
    P2M = 2;
    while (scanf("%u", &n) == 1) {
        if (n > MAXW) return 2;
        s.l[0] = n;
        for (unsigned i=0; i<n; i++) {
            if (scanf("%u", &v) != 1 || v > 3) return 3;
            s.w[0][i] = v;
        }
        if (scanf("%u", &n) != 1 || n > MAXW) return 4;
        s.l[1] = n;
        for (unsigned i=0; i<n; i++) {
            if (scanf("%u", &v) != 1 || v > 3) return 5;
            s.w[1][i] = v;
        }
        printf("%u %u\n", p2_of(&s), hprio(&s));
    }
    return ferror(stdin) ? 6 : 0;
}
