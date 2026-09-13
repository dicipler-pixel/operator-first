// Exact frontier dumper stacked on length_well_packed.cpp.
// Keeps the original official-kernel scanner untouched and reuses its state,
// packing, and move definitions in this translation unit.
#define main length_well_packed_embedded_main
#include "length_well_packed.cpp"
#undef main

static string frontier_hex128(U128 x) {
  static const char* H = "0123456789abcdef";
  string s(32, '0');
  for (int i = 31; i >= 0; --i) { s[i] = H[unsigned(x & 15)]; x >>= 4; }
  return s;
}

static string frontier_word_text(const string& w) {
  string out; out.reserve(w.size());
  for (char q : w) {
    switch (int8_t(q)) {
      case 1: out.push_back('x'); break;
      case -1: out.push_back('X'); break;
      case 2: out.push_back('y'); break;
      case -2: out.push_back('Y'); break;
      default: throw runtime_error("bad letter");
    }
  }
  return out;
}

static void frontier_u32(ofstream& f, uint32_t x) {
  f.write(reinterpret_cast<const char*>(&x), sizeof(x));
}
static void frontier_u64(ofstream& f, uint64_t x) {
  f.write(reinterpret_cast<const char*>(&x), sizeof(x));
}

int main(int argc, char** argv) {
  const int cap = argc > 1 ? stoi(argv[1]) : 30;
  const size_t limit = argc > 2 ? stoull(argv[2]) : 30000000ULL;
  const string prefix = argc > 3 ? argv[3] : "ac00015_cap30";
  if (cap < 20 || cap > 30) {
    cerr << "frontier cap must lie in [20,30]; cap+1 must fit the 31-letter packing\n";
    return 2;
  }

  State start = ac00015_well2();
  const int start_len = total_length(start);
  auto t0 = chrono::steady_clock::now();

  unordered_set<U128, Hash128> seen;
  seen.reserve(min(limit, size_t(20000000)));
  vector<U128> q;
  vector<uint32_t> parent;
  vector<uint8_t> via;
  q.reserve(min(limit, size_t(12000000)));
  parent.reserve(min(limit, size_t(12000000)));
  via.reserve(min(limit, size_t(12000000)));
  array<size_t, 32> hist{};

  U128 k0 = key(start);
  seen.insert(k0); q.push_back(k0); parent.push_back(UINT32_MAX); via.push_back(255);
  hist[start_len] = 1;
  size_t head = 0;

  while (head < q.size()) {
    const size_t src = head;
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
      parent.push_back(uint32_t(src));
      via.push_back(uint8_t(m));
      if (seen.size() >= limit) {
        cout << "LIMIT cap=" << cap << " states=" << seen.size()
             << " processed=" << head << "\n";
        return 3;
      }
    }
  }

  if (cap == 29 && seen.size() != 5149128ULL) {
    cerr << "cap-29 regression mismatch\n";
    return 4;
  }
  if (cap == 30 && seen.size() != 9096912ULL) {
    cerr << "cap-30 regression mismatch\n";
    return 5;
  }

  const string snap_path = prefix + ".wellbin";
  const string boundary_path = prefix + ".boundary.tsv";
  const string crossings_path = prefix + ".crossings.tsv";

  ofstream snap(snap_path, ios::binary);
  const char magic[8] = {'A','C','W','E','L','L','1','\0'};
  snap.write(magic, 8);
  frontier_u32(snap, uint32_t(cap));
  frontier_u32(snap, uint32_t(start_len));
  frontier_u64(snap, uint64_t(q.size()));
  for (size_t i = 0; i < q.size(); ++i) {
    frontier_u64(snap, uint64_t(q[i]));
    frontier_u64(snap, uint64_t(q[i] >> 64));
    frontier_u32(snap, parent[i]);
    snap.put(char(via[i]));
    const char pad[3] = {0,0,0}; snap.write(pad, 3);
  }
  if (!snap) { cerr << "snapshot write failed\n"; return 6; }

  ofstream boundary(boundary_path);
  boundary << "index\tkey_hex\ttotal\tr0\tr1\n";
  size_t boundary_n = 0;
  for (size_t i = 0; i < q.size(); ++i) {
    State s = from_key(q[i]);
    if (total_length(s) != cap) continue;
    boundary << i << '\t' << frontier_hex128(q[i]) << '\t' << cap << '\t'
             << frontier_word_text(s.a) << '\t' << frontier_word_text(s.b) << '\n';
    ++boundary_n;
  }
  if (!boundary) { cerr << "boundary write failed\n"; return 6; }

  ofstream crossings(crossings_path);
  crossings << "source_index\tsource_key_hex\tmove\ttarget_key_hex\ttarget_total\ttarget_r0\ttarget_r1\n";
  size_t edge_n = 0;
  for (size_t i = 0; i < q.size(); ++i) {
    State s = from_key(q[i]);
    if (total_length(s) != cap) continue;
    for (int m = 0; m < 14; ++m) {
      State z = move_ac(s, m);
      if (total_length(z) != cap + 1) continue;
      U128 kz = key(z);
      crossings << i << '\t' << frontier_hex128(q[i]) << '\t' << m << '\t'
                << frontier_hex128(kz) << '\t' << (cap + 1) << '\t'
                << frontier_word_text(z.a) << '\t' << frontier_word_text(z.b) << '\n';
      ++edge_n;
    }
  }
  if (!crossings) { cerr << "crossings write failed\n"; return 6; }

  double sec = chrono::duration<double>(chrono::steady_clock::now() - t0).count();
  cout << "COMPLETE cap=" << cap << " states=" << seen.size()
       << " min=" << start_len << " seconds=" << fixed << setprecision(3) << sec << "\n";
  for (int l = start_len; l <= cap; ++l)
    if (hist[l]) cout << "L" << l << "=" << hist[l] << (l == cap ? '\n' : ' ');
  cout << "SNAPSHOT file=" << snap_path << " records=" << q.size() << '\n';
  cout << "BOUNDARY file=" << boundary_path << " states=" << boundary_n << '\n';
  cout << "CROSSINGS file=" << crossings_path << " edges=" << edge_n << '\n';
  return 0;
}
