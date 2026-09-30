// SCRIPT: BOB-SPLICE3-01
// Reach-3 block splice: bridges state_i -> state_k made of two forward steps meeting one
// backward (inverted) step, each step = one library block or a 1-2 move primitive string.
// Official ac-r2-v1 move semantics (verifier/core.py apply_move, free reduction only).
// Prints the best saving found as: "BEST saving i k m1 m2 ..." (bridge moves), or "NONE".
// Every candidate is re-verified by the Python caller with the official core.
// Input on stdin: line1 r0, line2 r1 (space-separated ints), line3 path, then steps (one per line).
#include <cstdio>
#include <cstring>
#include <vector>
#include <string>
#include <unordered_map>
#include <iostream>
#include <sstream>
#include <cstdint>
using namespace std;
typedef vector<int8_t> W;
struct St { W a, b; };
static void pushc(W &o, int8_t c) { if (!o.empty() && o.back() == -c) o.pop_back(); else o.push_back(c); }
static St ap(const St &s, int m) {
    St t = s;
    if (m == 0) { W o; for (int i = s.a.size() - 1; i >= 0; i--) o.push_back(-s.a[i]); t.a = o; return t; }
    if (m == 1) { W o; for (int i = s.b.size() - 1; i >= 0; i--) o.push_back(-s.b[i]); t.b = o; return t; }
    if (m >= 2 && m <= 5) {
        const W &X = (m <= 3) ? s.a : s.b; const W &Y = (m <= 3) ? s.b : s.a;
        W o; for (auto c : X) pushc(o, c);
        if (m == 2 || m == 4) { for (auto c : Y) pushc(o, c); }
        else { for (int i = Y.size() - 1; i >= 0; i--) pushc(o, -Y[i]); }
        if (m <= 3) t.a = o; else t.b = o; return t;
    }
    int k = (m <= 9) ? m - 6 : m - 10;
    int8_t g = (k == 0) ? 1 : (k == 1) ? -1 : (k == 2) ? 2 : -2;
    const W &X = (m <= 9) ? s.a : s.b;
    W o; pushc(o, g); for (auto c : X) pushc(o, c); pushc(o, -g);
    if (m <= 9) t.a = o; else t.b = o; return t;
}
static const int INV[14] = {0, 1, 3, 2, 5, 4, 7, 6, 9, 8, 11, 10, 13, 12};
static St run(St s, const vector<int> &q) { for (int m : q) s = ap(s, m); return s; }
static uint64_t H(const St &s) {
    uint64_t h = 1469598103934665603ULL;
    for (auto c : s.a) { h ^= (uint8_t)c; h *= 1099511628211ULL; }
    h ^= 0x77; h *= 1099511628211ULL;
    for (auto c : s.b) { h ^= (uint8_t)c; h *= 1099511628211ULL; }
    return h;
}
static vector<int> readints(const string &line) { vector<int> v; stringstream ss(line); int x; while (ss >> x) v.push_back(x); return v; }
int main(int argc, char **argv) {
    int slack = argc > 1 ? atoi(argv[1]) : 4;
    string l; getline(cin, l); auto r0 = readints(l); getline(cin, l); auto r1 = readints(l);
    getline(cin, l); auto path = readints(l);
    vector<vector<int>> steps; while (getline(cin, l)) { auto v = readints(l); if (!v.empty()) steps.push_back(v); }
    St s0; for (int c : r0) s0.a.push_back(c); for (int c : r1) s0.b.push_back(c);
    vector<St> S{ s0 }; for (int m : path) S.push_back(ap(S.back(), m));
    int L = path.size(); size_t maxlen = 0;
    for (auto &s : S) maxlen = max(maxlen, s.a.size() + s.b.size());
    size_t cap = maxlen + slack;
    // backward: T --step--> S[k]; keep entry maximizing k - cost
    struct B { int k, c, st; };
    unordered_map<uint64_t, B> back; back.reserve((L + 1) * steps.size() * 2);
    unordered_map<uint64_t, int> idx;
    for (int k = 0; k <= L; k++) idx[H(S[k])] = k;
    for (int k = 0; k <= L; k++)
        for (int j = 0; j < (int)steps.size(); j++) {
            vector<int> iv; for (int t = steps[j].size() - 1; t >= 0; t--) iv.push_back(INV[steps[j][t]]);
            St T = run(S[k], iv);
            if (T.a.size() + T.b.size() > cap) continue;
            uint64_t h = H(T); int c = steps[j].size();
            auto it = back.find(h);
            if (it == back.end() || k - c > it->second.k - it->second.c) back[h] = {k, c, j};
        }
    int best = 0, bi = -1, bk = -1; vector<int> bb;
    auto consider = [&](int i, const St &T, int cost, const vector<int> &pre) {
        uint64_t h = H(T);
        auto d = idx.find(h);
        if (d != idx.end() && d->second > i) {
            int sav = (d->second - i) - cost;
            if (sav > best) { best = sav; bi = i; bk = d->second; bb = pre; }
        }
        auto it = back.find(h);
        if (it != back.end() && it->second.k > i) {
            int sav = (it->second.k - i) - cost - it->second.c;
            if (sav > best) { best = sav; bi = i; bk = it->second.k; bb = pre; for (int m : steps[it->second.st]) bb.push_back(m); }
        }
    };
    for (int i = 0; i < L; i++) {
        for (int a = 0; a < (int)steps.size(); a++) {
            St T1 = run(S[i], steps[a]);
            if (T1.a.size() + T1.b.size() > cap || T1.a.empty() || T1.b.empty()) continue;
            int c1 = steps[a].size();
            consider(i, T1, c1, steps[a]);
            if (c1 + 1 >= L - i) continue;
            for (int b = 0; b < (int)steps.size(); b++) {
                int c2 = c1 + steps[b].size();
                if (c2 >= L - i) continue;
                St T2 = run(T1, steps[b]);
                if (T2.a.size() + T2.b.size() > cap || T2.a.empty() || T2.b.empty()) continue;
                vector<int> pre = steps[a]; pre.insert(pre.end(), steps[b].begin(), steps[b].end());
                consider(i, T2, c2, pre);
            }
        }
    }
    if (best <= 0) { printf("NONE\n"); return 0; }
    printf("BEST %d %d %d", best, bi, bk); for (int m : bb) printf(" %d", m); printf("\n");
    return 0;
}
