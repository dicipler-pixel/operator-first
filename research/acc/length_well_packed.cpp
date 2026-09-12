// Exact packed finite length-well scanner for rank-2 Andrews--Curtis states.
// C++17, no external dependencies.
//
// For total relator length <= 31, an ordered state is encoded collision-free:
//   - 2 bits per letter for up to 31 letters (bits 0..61),
//   - |r0| in bits 64..68,
//   - |r1| in bits 69..73.
// The length fields are deliberately above bit 63 so they cannot overlap the
// 31st letter.  This file refuses caps above 31.
//
// The move kernel matches SAIR ac-r2-v1 exactly.  A complete cap-B scan with
// no state shorter than the start is a finite computational closure result;
// ACCWell.lean proves the abstract implication from such closure to a
// bottleneck theorem.

#include <bits/stdc++.h>
using namespace std;

using U128 = unsigned __int128;
struct State { string a, b; };

struct Hash128 {
  size_t operator()(U128 x) const noexcept {
    uint64_t lo = (uint64_t)x, hi = (uint64_t)(x >> 64);
    uint64_t z = lo ^ (hi + 0x9e3779b97f4a7c15ULL + (lo << 6) + (lo >> 2));
    z ^= z >> 30; z *= 0xbf58476d1ce4e5b9ULL;
    z ^= z >> 27; z *= 0x94d049bb133111ebULL;
    z ^= z >> 31;
    return (size_t)z;
  }
};

static inline uint8_t code(int8_t c) {
  if (c == 1) return 0;
  if (c == -1) return 1;
  if (c == 2) return 2;
  return 3;
}
static inline int8_t decode(uint8_t c) {
  if (c == 0) return 1;
  if (c == 1) return -1;
  if (c == 2) return 2;
  return -2;
}

static inline U128 key(const State& s) {
  U128 x = 0;
  int p = 0;
  for (char q : s.a) x |= U128(code(int8_t(q))) << (2 * p++);
  for (char q : s.b) x |= U128(code(int8_t(q))) << (2 * p++);
  x |= U128(s.a.size()) << 64;
  x |= U128(s.b.size()) << 69;
  return x;
}

static inline State from_key(U128 x) {
  int la = int((x >> 64) & 31), lb = int((x >> 69) & 31);
  State s;
  s.a.resize(la); s.b.resize(lb);
  for (int i = 0; i < la; ++i) s.a[i] = char(decode(uint8_t((x >> (2*i)) & 3)));
  for (int j = 0; j < lb; ++j) s.b[j] = char(decode(uint8_t((x >> (2*(la+j))) & 3)));
  return s;
}

static string inverse_word(const string& w) {
  string r; r.reserve(w.size());
  for (auto it = w.rbegin(); it != w.rend(); ++it) r.push_back(char(-int8_t(*it)));
  return r;
}
static string reduce_cat(const string& a, const string& b) {
  string out = a; out.reserve(a.size() + b.size());
  for (char q : b) {
    int8_t c = q;
    if (!out.empty() && int8_t(out.back()) == -c) out.pop_back();
    else out.push_back(char(c));
  }
  return out;
}
static string conjugate(const string& w, int8_t g) {
  string out; out.reserve(w.size() + 2);
  auto add = [&](int8_t c) {
    if (!out.empty() && int8_t(out.back()) == -c) out.pop_back();
    else out.push_back(char(c));
  };
  add(g); for (char q : w) add(int8_t(q)); add(-g);
  return out;
}

static State move_ac(const State& s, int m) {
  State z = s;
  if (m == 0) z.a = inverse_word(s.a);
  else if (m == 1) z.b = inverse_word(s.b);
  else if (m == 2) z.a = reduce_cat(s.a, s.b);
  else if (m == 3) z.a = reduce_cat(s.a, inverse_word(s.b));
  else if (m == 4) z.b = reduce_cat(s.b, s.a);
  else if (m == 5) z.b = reduce_cat(s.b, inverse_word(s.a));
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
    if (i == 0) z.a = conjugate(s.a, g); else z.b = conjugate(s.b, g);
  }
  return z;
}

static inline int total_length(const State& s) { return int(s.a.size() + s.b.size()); }
static string W(initializer_list<int> xs) {
  string s; for (int x : xs) s.push_back(char(int8_t(x))); return s;
}

static State ac00015_well2() {
  return {W({2,2,2,-1,-1,-2,-1,-1,2}),
          W({-2,1,2,1,-2,-2,1,-2,1,-2,1})};
}

int main(int argc, char** argv) {
  int cap = argc > 1 ? stoi(argv[1]) : 29;
  size_t limit = argc > 2 ? stoull(argv[2]) : 30000000ULL;
  if (cap < 20 || cap > 31) {
    cerr << "cap must lie in [20,31] for this exact packing\n";
    return 2;
  }

  State start = ac00015_well2();
  const int start_len = total_length(start);
  auto t0 = chrono::steady_clock::now();

  unordered_set<U128, Hash128> seen;
  seen.reserve(min(limit, size_t(20000000)));
  vector<U128> q;
  q.reserve(min(limit, size_t(12000000)));
  array<size_t, 32> hist{};

  U128 k0 = key(start);
  seen.insert(k0); q.push_back(k0); hist[start_len] = 1;
  size_t head = 0;

  while (head < q.size()) {
    State s = from_key(q[head++]);
    for (int m = 0; m < 14; ++m) {
      State z = move_ac(s, m);
      int lz = total_length(z);
      if (lz > cap) continue;
      U128 kz = key(z);
      if (!seen.insert(kz).second) continue;
      if (lz < start_len) {
        cout << "FOUND_DESCENT cap=" << cap << " states=" << seen.size()
             << " processed=" << head << " length=" << lz << "\n";
        return 1;
      }
      hist[lz]++;
      q.push_back(kz);
      if (seen.size() >= limit) {
        cout << "LIMIT cap=" << cap << " states=" << seen.size()
             << " processed=" << head << "\n";
        return 3;
      }
    }
  }

  double sec = chrono::duration<double>(chrono::steady_clock::now() - t0).count();
  cout << "COMPLETE cap=" << cap << " states=" << seen.size()
       << " min=" << start_len << " seconds=" << fixed << setprecision(3) << sec << "\n";
  for (int l = start_len; l <= cap; ++l)
    if (hist[l]) cout << "L" << l << "=" << hist[l] << (l == cap ? '\n' : ' ');

  if (cap == 29 && seen.size() != 5149128ULL) {
    cerr << "cap-29 regression mismatch\n";
    return 4;
  }
  if (cap == 30 && seen.size() != 9096912ULL) {
    cerr << "cap-30 regression mismatch\n";
    return 5;
  }
  return 0;
}
