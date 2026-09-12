// Fast exact cap-component scanner for the ACC length-well eye.
// C++17, no external dependencies.
//
// This reproduces the same ac-r2-v1 move kernel as length_well_eye.py.
// It is intended for large finite closures that are too slow for the Python
// reference implementation.  A closed cap-B component with minimum length L0
// certifies that every descent from the start must visit length at least B+1.

#include <bits/stdc++.h>
using namespace std;

struct State { string a, b; };

static inline string invw(const string& w) {
    string r; r.reserve(w.size());
    for (auto it = w.rbegin(); it != w.rend(); ++it)
        r.push_back(char(-int8_t(*it)));
    return r;
}

static inline string redcat(const string& a, const string& b) {
    string o = a; o.reserve(a.size() + b.size());
    for (char cc : b) {
        int8_t c = cc;
        if (!o.empty() && int8_t(o.back()) == -c) o.pop_back();
        else o.push_back(char(c));
    }
    return o;
}

static inline string conj(const string& w, int8_t g) {
    string o; o.reserve(w.size() + 2);
    auto add = [&](int8_t c) {
        if (!o.empty() && int8_t(o.back()) == -c) o.pop_back();
        else o.push_back(char(c));
    };
    add(g); for (char cc : w) add(int8_t(cc)); add(-g);
    return o;
}

static inline State move_ac(const State& s, int m) {
    State z = s;
    if (m == 0) z.a = invw(s.a);
    else if (m == 1) z.b = invw(s.b);
    else if (m == 2) z.a = redcat(s.a, s.b);
    else if (m == 3) z.a = redcat(s.a, invw(s.b));
    else if (m == 4) z.b = redcat(s.b, s.a);
    else if (m == 5) z.b = redcat(s.b, invw(s.a));
    else {
        int8_t g; int i;
        if      (m == 6)  { g =  1; i = 0; }
        else if (m == 7)  { g = -1; i = 0; }
        else if (m == 8)  { g =  2; i = 0; }
        else if (m == 9)  { g = -2; i = 0; }
        else if (m == 10) { g =  1; i = 1; }
        else if (m == 11) { g = -1; i = 1; }
        else if (m == 12) { g =  2; i = 1; }
        else if (m == 13) { g = -2; i = 1; }
        else throw runtime_error("move id must be 0..13");
        if (i == 0) z.a = conj(s.a, g); else z.b = conj(s.b, g);
    }
    return z;
}

static inline int total_length(const State& s) {
    return int(s.a.size() + s.b.size());
}

static inline string key(const State& s) {
    string k; k.reserve(s.a.size() + 1 + s.b.size());
    k += s.a; k.push_back('\0'); k += s.b;
    return k;
}

static inline string W(initializer_list<int> xs) {
    string s; for (int x : xs) s.push_back(char(int8_t(x))); return s;
}

static State ac00002() {
    return {W({-2,-2,-2,1,2,1,-2,-1,-1,-1}),
            W({-2,-2,-2,-2,-2,-2,-2,-1,2,2,2,2,2,2,1})};
}

static State ac00015() {
    return {W({-2,-1,2,-1,-2,1,2,-1,2,1}),
            W({-2,-2,1,-2,1,-2,1,-2,1,2,1})};
}

// Length-20 endpoint of the certified first ac-00015 escape.
static State ac00015_well2() {
    return {W({2,2,2,-1,-1,-2,-1,-1,2}),
            W({-2,1,2,1,-2,-2,1,-2,1,-2,1})};
}

struct Result {
    bool escaped = false, closed = false;
    size_t states = 0;
    int min_length = 0;
    double seconds = 0.0;
};

static Result scan(const State& start, int cap, size_t max_states) {
    const int L0 = total_length(start);
    int mn = L0;
    unordered_set<string> seen;
    seen.reserve(min(max_states, size_t(5'000'000)));
    vector<State> q;
    q.reserve(min(max_states, size_t(5'000'000)));
    seen.insert(key(start)); q.push_back(start);
    size_t head = 0;
    auto t0 = chrono::steady_clock::now();

    while (head < q.size()) {
        State s = std::move(q[head++]);
        for (int m = 0; m < 14; ++m) {
            State z = move_ac(s, m);
            int lz = total_length(z);
            if (lz > cap) continue;
            string kz = key(z);
            if (!seen.insert(kz).second) continue;
            mn = min(mn, lz);
            if (lz < L0) {
                double sec = chrono::duration<double>(chrono::steady_clock::now()-t0).count();
                return {true, false, seen.size(), mn, sec};
            }
            if (seen.size() >= max_states) {
                double sec = chrono::duration<double>(chrono::steady_clock::now()-t0).count();
                return {false, false, seen.size(), mn, sec};
            }
            q.push_back(std::move(z));
        }
    }
    double sec = chrono::duration<double>(chrono::steady_clock::now()-t0).count();
    return {false, true, seen.size(), mn, sec};
}

int main(int argc, char** argv) {
    if (argc < 3) {
        cerr << "usage: length_well_fast INSTANCE CAP [MAX_STATES]\n"
             << "INSTANCE: ac-00002 | ac-00015 | ac-00015-well2\n";
        return 2;
    }
    string id = argv[1];
    State start;
    if (id == "ac-00002") start = ac00002();
    else if (id == "ac-00015") start = ac00015();
    else if (id == "ac-00015-well2") start = ac00015_well2();
    else { cerr << "unknown instance\n"; return 2; }
    int cap = stoi(argv[2]);
    size_t max_states = argc > 3 ? stoull(argv[3]) : 30'000'000ULL;
    if (cap < total_length(start)) { cerr << "cap below start length\n"; return 2; }
    auto r = scan(start, cap, max_states);
    cout << "instance=" << id
         << " start_length=" << total_length(start)
         << " cap=" << cap
         << " states=" << r.states
         << " min_length=" << r.min_length
         << " escaped=" << int(r.escaped)
         << " closed=" << int(r.closed)
         << " seconds=" << fixed << setprecision(3) << r.seconds << "\n";
}
