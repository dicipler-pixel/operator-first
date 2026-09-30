// SCRIPT: ACC_DISK (Charlie) -- disk-backed exact capped BFS for the SAIR ACC, move spec ac-r2-v1.
//
// Exactness: moves reproduce verifier/core.py apply_move bit for bit (free reduction by one
// left-fold stack, no cyclic reduction). The official move table is closed under inversion
// (INVERSE_MOVE), so the capped move graph is undirected, and frontier search is exact:
// layer d+1 = N(layer d) minus layer d minus layer d-1. Every layer lives on disk as a sorted
// file of 16-byte keys; RAM holds one sort buffer. Nothing is pruned or canonicalized.
//
// Key: 128 bits, MSB first: len0 (6 bits), len1 (6 bits), r0 letters then r1 letters,
// 2 bits each (x=0, X=1, y=2, Y=3; inverse = code^1), left aligned. Total length <= 58.
//
// Commands:
//   acc_disk bfs DIR START CAP [--mem MB] [--meet FILE] [--below T] [--maxlayer N]
//                               [--notarget] [--lean] [--minfree GB]
//   acc_disk union DIR OUTFILE           all layers of DIR into one sorted set file
//   acc_disk path DIR STATE              moves from DIR's root to STATE
//   acc_disk intersect FILE1 FILE2       first common state and the count of common states
//   acc_disk selftest STATE...           all 14 moves of each STATE (for the Python cross-check)
// STATE strings: "r0,r1" with letters x X y Y, e.g. "x,y" for the trivial.
// Results: CLOSED (component exhausted), TARGET, MEET (touched --meet set), BELOW, MAXLAYER,
// DISKFULL (clean stop before a layer that might not fit). Any failed write exits with code 3.
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <string>
#include <vector>
#include <queue>
#include <algorithm>
#include <sys/stat.h>
#include <sys/mman.h>
#include <sys/statvfs.h>
#include <fcntl.h>
#include <unistd.h>
#include <time.h>

typedef unsigned __int128 K128;
static const int MAXL = 58;
static const int INV[14] = {0,1,3,2,5,4,7,6,9,8,11,10,13,12};

struct St { int n0, n1; uint8_t a[MAXL+2], b[MAXL+2]; };

static K128 pack(const St& s) {
    K128 v = (K128)s.n0; v = (v << 6) | (K128)s.n1;
    for (int i = 0; i < s.n0; i++) v = (v << 2) | s.a[i];
    for (int i = 0; i < s.n1; i++) v = (v << 2) | s.b[i];
    v <<= 2 * (MAXL - s.n0 - s.n1);
    return v;
}
static void unpack(K128 v, St& s) {
    s.n0 = (int)(v >> 122); s.n1 = (int)((v >> 116) & 63);
    int tot = s.n0 + s.n1;
    for (int i = 0; i < tot; i++) {
        int c = (int)((v >> (114 - 2 * i)) & 3);
        if (i < s.n0) s.a[i] = c; else s.b[i - s.n0] = c;
    }
}
static int reduce_into(const uint8_t* src, int n, uint8_t* dst) {
    int k = 0;
    for (int i = 0; i < n; i++) { uint8_t c = src[i]; if (k && dst[k-1] == (c ^ 1)) k--; else dst[k++] = c; }
    return k;
}
static int invert_into(const uint8_t* w, int n, uint8_t* dst) { for (int i = 0; i < n; i++) dst[i] = w[n-1-i] ^ 1; return n; }

static bool apply_move(const St& s, int m, St& t) {
    uint8_t tmp[2*MAXL+4], out[2*MAXL+4];
    t = s;
    if (m == 0) { invert_into(s.a, s.n0, t.a); return true; }
    if (m == 1) { invert_into(s.b, s.n1, t.b); return true; }
    if (m >= 2 && m <= 5) {
        const uint8_t *x, *y; int nx, ny; uint8_t yy[MAXL+2]; bool to0 = (m <= 3), invo = (m == 3 || m == 5);
        if (to0) { x = s.a; nx = s.n0; y = s.b; ny = s.n1; } else { x = s.b; nx = s.n1; y = s.a; ny = s.n0; }
        if (invo) { invert_into(y, ny, yy); y = yy; }
        memcpy(tmp, x, nx); memcpy(tmp + nx, y, ny);
        int r = reduce_into(tmp, nx + ny, out);
        if (r > MAXL) return false;
        if (to0) { memcpy(t.a, out, r); t.n0 = r; } else { memcpy(t.b, out, r); t.n1 = r; }
        return true;
    }
    bool on0 = (m <= 9); uint8_t c = (uint8_t)(on0 ? m - 6 : m - 10); // GENS = (x, X, y, Y) -> codes 0..3
    const uint8_t* w = on0 ? s.a : s.b; int n = on0 ? s.n0 : s.n1;
    tmp[0] = c; memcpy(tmp + 1, w, n); tmp[n + 1] = c ^ 1;
    int r = reduce_into(tmp, n + 2, out);
    if (r > MAXL) return false;
    if (on0) { memcpy(t.a, out, r); t.n0 = r; } else { memcpy(t.b, out, r); t.n1 = r; }
    return true;
}
static bool parse_state(const char* str, St& s) {
    s.n0 = s.n1 = 0; int which = 0;
    for (const char* p = str; *p; p++) {
        int c;
        switch (*p) { case 'x': c = 0; break; case 'X': c = 1; break; case 'y': c = 2; break; case 'Y': c = 3; break;
                      case ',': which = 1; continue; default: return false; }
        if (which == 0) s.a[s.n0++] = c; else s.b[s.n1++] = c;
        if (s.n0 > MAXL || s.n1 > MAXL) return false;
    }
    return which == 1;
}
static std::string show(const St& s) {
    static const char L[4] = {'x','X','y','Y'}; std::string o;
    for (int i = 0; i < s.n0; i++) o += L[s.a[i]]; o += ',';
    for (int i = 0; i < s.n1; i++) o += L[s.b[i]]; return o;
}
static double now() { timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return t.tv_sec + 1e-9 * t.tv_nsec; }
static void die_io(const char* what) { perror(what); exit(3); }

struct Reader {
    FILE* f = nullptr; std::vector<K128> buf; size_t pos = 0, n = 0; K128 cur = 0; bool has = false;
    bool open(const std::string& path) { f = fopen(path.c_str(), "rb"); if (!f) { has = false; return false; } buf.resize(1 << 16); next(); return true; }
    void next() {
        if (pos >= n) { if (!f) { has = false; return; } n = fread(buf.data(), sizeof(K128), buf.size(), f); pos = 0; if (n == 0) { has = false; fclose(f); f = nullptr; return; } }
        cur = buf[pos++]; has = true;
    }
};
struct Writer {
    FILE* f; std::vector<K128> buf; size_t n = 0; uint64_t count = 0;
    Writer(const std::string& p) { f = fopen(p.c_str(), "wb"); if (!f) die_io(p.c_str()); buf.resize(1 << 16); }
    void wr() { if (fwrite(buf.data(), sizeof(K128), n, f) != n) die_io("write failed (disk full?)"); n = 0; }
    void put(K128 k) { buf[n++] = k; count++; if (n == buf.size()) wr(); }
    void close() { if (n) wr(); if (fclose(f)) die_io("close failed (disk full?)"); }
};
static std::string layer_path(const std::string& dir, int d) { char b[64]; snprintf(b, sizeof b, "/L_%04d.bin", d); return dir + b; }
static uint64_t file_count(const std::string& p) { struct stat st; if (stat(p.c_str(), &st)) return 0; return st.st_size / sizeof(K128); }

struct MFile { const K128* p = nullptr; size_t n = 0; int fd = -1;
    bool open(const std::string& path) { fd = ::open(path.c_str(), O_RDONLY); if (fd < 0) return false; struct stat st; fstat(fd, &st); n = st.st_size / sizeof(K128);
        if (n == 0) { p = nullptr; return true; } p = (const K128*)mmap(nullptr, st.st_size, PROT_READ, MAP_PRIVATE, fd, 0); return p != MAP_FAILED; }
    bool has(K128 k) const { return n && std::binary_search(p, p + n, k); }
};

static int cmd_bfs(int argc, char** argv) {
    if (argc < 5) { fprintf(stderr, "bfs DIR START CAP [--mem MB] [--meet FILE] [--below T] [--maxlayer N] [--notarget] [--lean] [--minfree GB]\n"); return 1; }
    std::string dir = argv[2]; St root; if (!parse_state(argv[3], root)) { fprintf(stderr, "bad START\n"); return 1; }
    int cap = atoi(argv[4]); if (cap > MAXL) { fprintf(stderr, "cap > %d\n", MAXL); return 1; }
    size_t memMB = 1500; std::string meet; int below = -1, maxlayer = 100000; bool notarget = false, lean = false; double minfreeGB = 0;
    for (int i = 5; i < argc; i++) {
        if (!strcmp(argv[i], "--mem")) memMB = atol(argv[++i]);
        else if (!strcmp(argv[i], "--meet")) meet = argv[++i];
        else if (!strcmp(argv[i], "--below")) below = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--maxlayer")) maxlayer = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--notarget")) notarget = true;
        else if (!strcmp(argv[i], "--lean")) lean = true;
        else if (!strcmp(argv[i], "--minfree")) minfreeGB = atof(argv[++i]);
    }
    mkdir(dir.c_str(), 0755);
    St triv; parse_state("x,y", triv); K128 target = pack(triv);
    if (root.n0 + root.n1 > cap) { fprintf(stderr, "start exceeds cap\n"); return 1; }
    { Writer w(layer_path(dir, 0)); w.put(pack(root)); w.close(); }
    FILE* log = fopen((dir + "/LOG.tsv").c_str(), "a");
    fprintf(log, "# bfs start=%s cap=%d mem=%zuMB meet=%s below=%d lean=%d\n", show(root).c_str(), cap, memMB, meet.c_str(), below, (int)lean);
    fprintf(log, "layer\tsize\tcumulative\tmin_total\tsecs\n");
    printf("start %s cap %d\n", show(root).c_str(), cap);
    uint64_t cum = 1; size_t bufN = memMB * 1024 * 1024 / sizeof(K128);
    std::vector<K128> buf(bufN);
    int status = 0; K128 hitKey = 0; int hitLayer = -1;
    if (!notarget && pack(root) == target) { status = 2; hitKey = target; hitLayer = 0; }
    for (int d = 0; status == 0; d++) {
        if (d >= maxlayer) { status = 5; break; }
        if (minfreeGB > 0) {
            struct statvfs sv; statvfs(dir.c_str(), &sv); double fg = (double)sv.f_bavail * sv.f_frsize / 1e9;
            double cur = (double)file_count(layer_path(dir, d)), prev = d > 0 ? (double)file_count(layer_path(dir, d - 1)) : 1.0;
            double grow = prev > 0 ? std::max(1.0, cur / prev) : 2.0;
            double need = cur * grow * sizeof(K128) * 3.0 / 1e9; // runs of new states (overlap across runs) + next layer
            if (fg < minfreeGB + need) { status = 6; break; }
        }
        double t0 = now();
        std::vector<std::string> runs; size_t fill = 0;
        auto flush = [&]() {
            if (!fill) return; std::sort(buf.begin(), buf.begin() + fill);
            size_t u = std::unique(buf.begin(), buf.begin() + fill) - buf.begin();
            { // drop states already in layer d or d-1 before writing (same subtraction as the final merge, done early)
              Reader A2, B2; A2.open(layer_path(dir, d)); if (d > 0) B2.open(layer_path(dir, d - 1)); size_t o = 0;
              for (size_t i = 0; i < u; i++) { K128 k = buf[i];
                  while (A2.has && A2.cur < k) A2.next(); if (A2.has && A2.cur == k) continue;
                  while (B2.has && B2.cur < k) B2.next(); if (B2.has && B2.cur == k) continue;
                  buf[o++] = k; }
              u = o; }
            char nm[64]; snprintf(nm, sizeof nm, "/run_%04zu.tmp", runs.size()); std::string rp = dir + nm;
            FILE* f = fopen(rp.c_str(), "wb");
            if (!f || fwrite(buf.data(), sizeof(K128), u, f) != u || fclose(f)) die_io("run write failed (disk full?)");
            runs.push_back(rp); fill = 0;
        };
        { Reader r; r.open(layer_path(dir, d)); St s, t;
          while (r.has) { unpack(r.cur, s);
              for (int m = 0; m < 14; m++) { if (!apply_move(s, m, t)) continue; if (t.n0 + t.n1 > cap) continue;
                  buf[fill++] = pack(t); if (fill == bufN) flush(); }
              r.next(); } }
        flush();
        std::vector<Reader> rr(runs.size()); for (size_t i = 0; i < runs.size(); i++) rr[i].open(runs[i]);
        typedef std::pair<K128, int> HE; auto cmp = [](const HE& a, const HE& b) { return a.first > b.first; };
        std::priority_queue<HE, std::vector<HE>, decltype(cmp)> pq(cmp);
        for (size_t i = 0; i < rr.size(); i++) if (rr[i].has) pq.push({rr[i].cur, (int)i});
        Reader A, B; A.open(layer_path(dir, d)); if (d > 0) B.open(layer_path(dir, d - 1));
        Reader M; bool useMeet = !meet.empty(); if (useMeet) M.open(meet);
        Writer w(layer_path(dir, d + 1)); K128 last = 0; bool haveLast = false; int minTot = 999;
        while (!pq.empty()) {
            HE top = pq.top(); pq.pop(); K128 k = top.first; int i = top.second; rr[i].next(); if (rr[i].has) pq.push({rr[i].cur, i});
            if (haveLast && k == last) continue; last = k; haveLast = true;
            while (A.has && A.cur < k) A.next(); if (A.has && A.cur == k) continue;
            while (B.has && B.cur < k) B.next(); if (B.has && B.cur == k) continue;
            w.put(k);
            int tot = (int)(k >> 122) + (int)((k >> 116) & 63); if (tot < minTot) minTot = tot;
            if (!notarget && k == target && status == 0) { status = 2; hitKey = k; hitLayer = d + 1; }
            if (useMeet && status == 0) { while (M.has && M.cur < k) M.next(); if (M.has && M.cur == k) { status = 3; hitKey = k; hitLayer = d + 1; } }
            if (below >= 0 && tot < below && status == 0) { status = 4; hitKey = k; hitLayer = d + 1; }
        }
        w.close(); for (auto& p : runs) remove(p.c_str());
        if (lean && d - 1 > 0) remove(layer_path(dir, d - 1).c_str());
        cum += w.count;
        double dt = now() - t0;
        fprintf(log, "%d\t%llu\t%llu\t%d\t%.1f\n", d + 1, (unsigned long long)w.count, (unsigned long long)cum, w.count ? minTot : -1, dt); fflush(log);
        printf("layer %d size %llu cum %llu min_total %d (%.1fs)\n", d + 1, (unsigned long long)w.count, (unsigned long long)cum, w.count ? minTot : -1, dt); fflush(stdout);
        if (w.count == 0 && status == 0) status = 1;
    }
    const char* names[] = {"OPEN", "CLOSED", "TARGET", "MEET", "BELOW", "MAXLAYER", "DISKFULL"};
    fprintf(log, "# RESULT %s states=%llu", names[status], (unsigned long long)cum);
    printf("RESULT %s states=%llu", names[status], (unsigned long long)cum);
    if (status >= 2 && status <= 4) { St h; unpack(hitKey, h); fprintf(log, " layer=%d state=%s", hitLayer, show(h).c_str()); printf(" layer=%d state=%s", hitLayer, show(h).c_str()); }
    fprintf(log, "\n"); printf("\n"); fclose(log);
    return 0;
}
static int cmd_union(int argc, char** argv) {
    std::string dir = argv[2]; std::vector<Reader> rr;
    for (int d = 0;; d++) { std::string p = layer_path(dir, d); if (access(p.c_str(), R_OK)) break; rr.emplace_back(); rr.back().open(p); }
    typedef std::pair<K128, int> HE; auto cmp = [](const HE& a, const HE& b) { return a.first > b.first; };
    std::priority_queue<HE, std::vector<HE>, decltype(cmp)> pq(cmp);
    for (size_t i = 0; i < rr.size(); i++) if (rr[i].has) pq.push({rr[i].cur, (int)i});
    Writer w(argv[3]); K128 last = 0; bool hl = false;
    while (!pq.empty()) { HE t = pq.top(); pq.pop(); rr[t.second].next(); if (rr[t.second].has) pq.push({rr[t.second].cur, t.second});
        if (hl && t.first == last) continue; last = t.first; hl = true; w.put(t.first); }
    w.close(); printf("union %llu states from %zu layers\n", (unsigned long long)w.count, rr.size()); return 0;
}
static int cmd_path(int argc, char** argv) {
    std::string dir = argv[2]; St s; if (!parse_state(argv[3], s)) { fprintf(stderr, "bad STATE\n"); return 1; }
    K128 k = pack(s); int D = -1; std::vector<MFile> L;
    for (int d = 0;; d++) { std::string p = layer_path(dir, d); if (access(p.c_str(), R_OK)) break; L.emplace_back(); L.back().open(p); if (D < 0 && L.back().has(k)) D = d; }
    if (D < 0) { fprintf(stderr, "state not in any layer\n"); return 1; }
    std::vector<int> back; St cur = s;
    for (int d = D; d > 0; d--) {
        bool found = false; St t;
        for (int m = 0; m < 14 && !found; m++) { if (!apply_move(cur, m, t)) continue; if (L[d-1].has(pack(t))) { back.push_back(INV[m]); cur = t; found = true; } }
        if (!found) { fprintf(stderr, "broken chain at layer %d\n", d); return 1; }
    }
    std::reverse(back.begin(), back.end());
    printf("["); for (size_t i = 0; i < back.size(); i++) printf("%s%d", i ? ", " : "", back[i]); printf("]\n");
    return 0;
}
static int cmd_intersect(int argc, char** argv) {
    Reader a, b; a.open(argv[2]); b.open(argv[3]); uint64_t n = 0; bool first = true;
    while (a.has && b.has) { if (a.cur < b.cur) a.next(); else if (b.cur < a.cur) b.next();
        else { if (first) { St s; unpack(a.cur, s); printf("first %s\n", show(s).c_str()); first = false; } n++; a.next(); b.next(); } }
    printf("common %llu\n", (unsigned long long)n); return 0;
}
static int cmd_selftest(int argc, char** argv) {
    for (int i = 2; i < argc; i++) { St s, t; if (!parse_state(argv[i], s)) return 1;
        for (int m = 0; m < 14; m++) { apply_move(s, m, t); printf("%s %d %s\n", argv[i], m, show(t).c_str()); } }
    return 0;
}
int main(int argc, char** argv) {
    if (argc < 2) { fprintf(stderr, "commands: bfs union path intersect selftest\n"); return 1; }
    std::string c = argv[1];
    if (c == "bfs") return cmd_bfs(argc, argv);
    if (c == "union" && argc >= 4) return cmd_union(argc, argv);
    if (c == "path" && argc >= 4) return cmd_path(argc, argv);
    if (c == "intersect" && argc >= 4) return cmd_intersect(argc, argv);
    if (c == "selftest") return cmd_selftest(argc, argv);
    fprintf(stderr, "unknown command\n"); return 1;
}
