# SCRIPT: UPG-GATE-01 (Module I winding law; Section 1 F(Omega,Pi) theorems)
import numpy as np

print("=== G1: phase-transport -- winding around the zero is the honest integer ===")

def winding(loop_pts):
    a, b = loop_pts[:, 0], loop_pts[:, 1]
    ph = np.unwrap(np.arctan2(b, a))
    return (ph[-1] - ph[0]) / (2*np.pi)

th = np.linspace(0, 2*np.pi, 4001)
m, n = 0, 0
enc  = np.stack([0.30 + 0.25*np.cos(th) + m, 0.30 + 0.25*np.sin(th) + n], 1)
enc2 = np.stack([0.10*np.cos(th),   0.10*np.sin(th)],   1)
enc3 = np.stack([0.10*np.cos(2*th), 0.10*np.sin(2*th)], 1)
print(f"  loop not enclosing zero: winding = {winding(enc):+.6f}")
print(f"  loop enclosing zero:     winding = {winding(enc2):+.6f}")
print(f"  double loop:             winding = {winding(enc3):+.6f}")
print()

print("=== G3: Theorems 1.2/1.3 -- F(Omega,Pi) identities, random gates ===")
rng = np.random.default_rng(5)
ok_forms = ok_iff = ok_trace = ok_cross = True
for trial in range(200):
    N, k = 8, 3
    A = rng.normal(size=(N, N)) + 1j*rng.normal(size=(N, N))
    Om = A + A.conj().T
    Q, _ = np.linalg.qr(rng.normal(size=(N, k)) + 1j*rng.normal(size=(N, k)))
    Pi = Q @ Q.conj().T
    I = np.eye(N)
    F1 = (I - Pi) @ Om @ Pi + Pi @ Om @ (I - Pi)
    F2 = Om @ Pi + Pi @ Om - 2*Pi @ Om @ Pi
    C = Om @ Pi - Pi @ Om
    ok_forms &= np.allclose(F1, F2, atol=1e-10)
    ok_trace &= abs(np.trace(F1)) < 1e-10
    ok_cross &= (np.allclose(Pi @ F1 @ Pi, 0, atol=1e-10) and
                 np.allclose((I - Pi) @ F1 @ (I - Pi), 0, atol=1e-10))
    ok_iff &= (np.linalg.norm(F1) < 1e-10) == (np.linalg.norm(C) < 1e-10)

w = np.sort(rng.normal(size=8))
U, _ = np.linalg.qr(rng.normal(size=(8, 8)) + 1j*rng.normal(size=(8, 8)))
Om = U @ np.diag(w) @ U.conj().T
Pi = U[:, :3] @ U[:, :3].conj().T
F = (np.eye(8) - Pi) @ Om @ Pi + Pi @ Om @ (np.eye(8) - Pi)
print(f"  equivalent forms agree (200 trials):            {ok_forms}")
print(f"  Tr F = 0 (200 trials):                          {ok_trace}")
print(f"  cross-subspace only (Pi F Pi = 0 = Qc F Qc):    {ok_cross}")
print(f"  F=0 <=> [Om,Pi]=0, generic direction:           {ok_iff}")
print(f"  commuting pair gives ||F|| = {np.linalg.norm(F):.2e}")
