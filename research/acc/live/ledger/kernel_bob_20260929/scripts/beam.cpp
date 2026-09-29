// SCRIPT: KERNEL-BEAM-01
// Beam search for AC trivialization under the official SAIR ac-r2-v1 move table
// (moves 0..13, free reduction only, exactly as verifier/core.py apply_move).
// Goal: both relators of length 1. Finishing moves to ((1,),(2,)) are added and the
// whole path is re-verified afterwards with the official Python core.
// Usage: beam r0 r1 width maxdepth maxlen seed mode
//   r0/r1: comma-separated ints (1=x,-1=X,2=y,-2=Y)
//   mode 0: score = |r0|+|r1|
//   mode 1: score = |r0|+|r1| + balance term |(|r0|-|r1|)|/2
//   mode 2: score = max(|r0|,|r1|)*2 + min
// Output: "PATH m1 m2 ..." on success, "NOPATH depth" otherwise.
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <vector>
#include <algorithm>
#include <unordered_set>
#include <random>
#include <cstdint>
using namespace std;
const int ML = 96;
struct St { int8_t a[ML], b[ML]; uint8_t la, lb; };
static int MAXLEN;
static inline bool push(int8_t *out, int &n, int8_t c) {
    if (n && out[n-1] == -c) { n--; return true; }
    if (n >= MAXLEN) return false;
    out[n++] = c; return true;
}
// apply move m to s -> t; return false if length cap exceeded
static bool apply(const St &s, int m, St &t) {
    t = s;
    int8_t buf[2*ML+4]; int n = 0;
    auto finish = [&](int which) -> bool {
        if (which == 0) { memcpy(t.a, buf, n); t.la = n; } else { memcpy(t.b, buf, n); t.lb = n; }
        return true;
    };
    const int8_t *A = s.a, *B = s.b; int la = s.la, lb = s.lb;
    if (m == 0) { for (int i = la-1; i >= 0; i--) buf[n++] = -A[i]; return finish(0); }
    if (m == 1) { for (int i = lb-1; i >= 0; i--) buf[n++] = -B[i]; return finish(1); }
    if (m >= 2 && m <= 5) {
        const int8_t *X = (m <= 3) ? A : B; int lx = (m <= 3) ? la : lb;
        const int8_t *Y = (m <= 3) ? B : A; int ly = (m <= 3) ? lb : la;
        bool inv = (m == 3 || m == 5);
        for (int i = 0; i < lx; i++) if (!push(buf, n, X[i])) return false;
        if (!inv) { for (int i = 0; i < ly; i++) if (!push(buf, n, Y[i])) return false; }
        else { for (int i = ly-1; i >= 0; i--) if (!push(buf, n, -Y[i])) return false; }
        return finish(m <= 3 ? 0 : 1);
    }
    int k = (m <= 9) ? m - 6 : m - 10;
    int8_t g = (k == 0) ? 1 : (k == 1) ? -1 : (k == 2) ? 2 : -2;
    const int8_t *X = (m <= 9) ? A : B; int lx = (m <= 9) ? la : lb;
    push(buf, n, g);
    for (int i = 0; i < lx; i++) if (!push(buf, n, X[i])) return false;
    if (!push(buf, n, -g)) return false;
    return finish(m <= 9 ? 0 : 1);
}
static uint64_t hsh(const St &s) {
    uint64_t h = 1469598103934665603ULL;
    for (int i = 0; i < s.la; i++) { h ^= (uint8_t)s.a[i]; h *= 1099511628211ULL; }
    h ^= 0xff; h *= 1099511628211ULL;
    for (int i = 0; i < s.lb; i++) { h ^= (uint8_t)s.b[i]; h *= 1099511628211ULL; }
    return h ^ (h >> 29);
}
static vector<int8_t> parse(const char *s) {
    vector<int8_t> v; char *e; const char *p = s;
    while (*p) { long x = strtol(p, &e, 10); if (e == p) break; v.push_back((int8_t)x); p = e; if (*p == ',') p++; }
    return v;
}
int main(int argc, char **argv) {
    auto r0 = parse(argv[1]), r1 = parse(argv[2]);
    size_t W = atol(argv[3]); int D = atoi(argv[4]); MAXLEN = atoi(argv[5]);
    unsigned seed = atoi(argv[6]); int mode = atoi(argv[7]);
    if (MAXLEN > ML) MAXLEN = ML;
    mt19937_64 rng(seed);
    St s0; s0.la = r0.size(); s0.lb = r1.size();
    memcpy(s0.a, r0.data(), r0.size()); memcpy(s0.b, r1.data(), r1.size());
    struct Node { St s; int parent; int8_t mv; };
    vector<vector<pair<int,int8_t>>> hist; // per depth: (parent index, move)
    vector<St> cur{ s0 };
    unordered_set<uint64_t> seen; seen.reserve(W * 40); seen.insert(hsh(s0));
    for (int d = 0; d < D; d++) {
        struct Cand { float sc; St s; int par; int8_t mv; };
        vector<Cand> cand; cand.reserve(cur.size() * 14);
        for (int i = 0; i < (int)cur.size(); i++) {
            for (int m = 0; m < 14; m++) {
                St t;
                if (!apply(cur[i], m, t)) continue;
                if (t.la == 0 || t.lb == 0) continue;
                uint64_t h = hsh(t);
                if (!seen.insert(h).second) continue;
                float L = t.la + t.lb, sc;
                if (mode == 0) sc = L;
                else if (mode == 1) sc = L + 0.5f * abs(t.la - t.lb);
                else sc = 2.0f * max(t.la, t.lb) + min(t.la, t.lb);
                sc += (rng() % 1000) * 1e-4f;
                cand.push_back({sc, t, i, (int8_t)m});
                if (t.la == 1 && t.lb == 1) {
                    // reconstruct
                    vector<int> path{ m };
                    int p = i;
                    for (int dd = d - 1; dd >= 0; dd--) { path.push_back(hist[dd][p].second); p = hist[dd][p].first; }
                    reverse(path.begin(), path.end());
                    printf("PATH");
                    for (int x : path) printf(" %d", x);
                    printf("\n"); return 0;
                }
            }
        }
        if (cand.empty()) break;
        if (cand.size() > W) {
            nth_element(cand.begin(), cand.begin() + W, cand.end(), [](const Cand &x, const Cand &y) { return x.sc < y.sc; });
            cand.resize(W);
        }
        vector<pair<int,int8_t>> h; h.reserve(cand.size());
        vector<St> nxt; nxt.reserve(cand.size());
        for (auto &c : cand) { h.push_back({c.par, c.mv}); nxt.push_back(c.s); }
        hist.push_back(move(h)); cur.swap(nxt);
        if (seen.size() > 120000000ULL) { printf("NOPATH memcap %d\n", d); return 0; }
    }
    printf("NOPATH %d\n", D);
    return 0;
}
