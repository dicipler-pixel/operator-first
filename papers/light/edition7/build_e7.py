import re, hashlib, sys
s=open('Light_Research_Edition_7_DRAFT.html',encoding='utf-8').read()
log=[]
def rep(old,new,count=1,regex=False,label=''):
    global s
    n=len(re.findall(old,s)) if regex else s.count(old)
    assert n==count, f"{label or old[:50]!r}: expected {count} found {n}"
    s=re.sub(old,new,s) if regex else s.replace(old,new)
    log.append(f"{label or old[:40]}: {n} replaced")

def wpat(lit):  # literal text with whitespace-insensitive gaps
    return r'\s+'.join(re.escape(x) for x in lit.split())
def wrep(old,new,count=1,label=''):
    rep(wpat(old),new.replace('\\','\\\\'),count=count,regex=True,label=label or old[:40])

REV7='41d9523a53ad679d2240e5e40ed07a7ea0cc2bac'; RUN7='34015381110'; RUN7X='34034732711'
REV21='f4e682ff428b5e941a3da7d2a1b211dc925bdbc6'; RUN21='34684818137'
PEEL='3987916ff947ee4cec6438ad384f16e0e8093aa8ad82ec77a95f5495c9cfc83c'

# E1 banner + E2 header
banner='''<!-- EDITION 7 BANNER --> <aside style="border:2px solid #0b1220;padding:1em;margin:1em 0"><strong>Research edition 7 — audit, certification labels and repair, 12 September 2026.</strong> This edition adds a claim-by-claim evidence audit (Appendix B.1–B.3), a fifth grade <strong>[L]</strong> for statements whose finite form is certified by kernel-checked Lean at a named source revision, two certified remarks imported from the Atlas formalization branch (Sections 3.1 and 5.2), a sequential numbering repair in Section 5, and the missing grade on the edition 6 proposition. Display equations no longer sit in horizontal scroll boxes and the one light-background figure now uses the manuscript palette. Editions 3–6 are preserved in full below. No new material measurements, no new physical identifications, and no new Lean compilation are claimed; every Lean citation names the revision and workflow run that produced it.</aside> '''
rep('<!-- EDITION 5 BANNER -->', banner+'<!-- EDITION 5 BANNER -->', label='E1 banner') if '<!-- EDITION 5 BANNER -->' in s else None
if '<!-- EDITION 7 BANNER -->' not in s:
    rep('<aside style="border:2px solid #526f95;', banner+'<aside style="border:2px solid #526f95;', label='E1 banner (fallback)')
rep('<p class="date">Research edition 3 · 6 September 2026</p>',
    '<p class="date">Research edition 7 · 12 September 2026</p>\n<p class="date" style="font-size:.85em">Edition history: 3 (6 Sep 2026) · 4 (7 Sep) · 5 and 6 (8 Sep) · 7 (12 Sep)</p>', label='E2 header')

# E3 grade [L]
wrep('<strong>[H]</strong> identifies an interpretation, constitutive\nassumption, or open physical identification.',
    '<strong>[H]</strong> identifies an interpretation, constitutive\nassumption, or open physical identification. <strong>[L]</strong>, new in\nedition 7, identifies a statement whose finite form is certified by a\nkernel-checked Lean declaration at a named source revision and workflow\nrun (Appendix B.1); the label covers exactly the displayed finite\nidentity, and any analytic, spectral or variational remainder keeps its\nown [T].', label='E3 grade L')

# E4/E5 split run-in environments into their own paragraphs
rep(r'</span>\s*<strong>Proposition 3\.1\.</strong>', '</span></p>\n<p><strong>Proposition 3.1 (integer winding under a positive branch guard).</strong>', regex=True, label='E4 Prop 3.1 split')
rep(r'</span>\s*<strong>Theorem 5\.1 \(coupling census\)\.</strong>', '</span></p>\n<p><strong>Theorem 5.1 (coupling census).</strong>', regex=True, label='E5 Thm 5.1 split')

# E6 sequential numbering in Section 5: Thm 5.1, Cor 5.2, Prop 5.3, Prop 5.4 (was duplicate 5.1), Thm 5.5 (was 5.4)
n54=s.count('Theorem 5.4'); log.append(f"Theorem 5.4 mentions: {n54}")
rep('Theorem 5.4','Theorem 5.5',count=n54,label='E6 Thm 5.4->5.5')
wrep('<strong>Proposition 5.1 (a specific calibration obstruction).</strong>','<strong>Proposition 5.4 (a specific calibration obstruction).</strong>',label='E6 Prop 5.1->5.4')
rep('Proposition 5.1 excludes','Proposition 5.4 excludes',label='E6 xref')

# E7 edition-6 proposition: harmonized label and grade
wrep('<strong>Proposition 4.9d.1. Support from finitely many signed responses.</strong>','<strong>Proposition 4.5e (support from finitely many signed responses; edition 6 label 4.9d.1).</strong>',label='E7 label')
wrep('residues are Hermitian. ◻</p>\n</div>','residues are Hermitian. ◻ <strong>[T]</strong></p>\n</div>',label='E7 grade')

# E8 certified remarks from PR #21
rem57=('<p><strong>Certified turning-point remark (edition 7).</strong> Write <span class="math inline">\\(s=\\sin\\theta_2\\)</span> and <span class="math inline">\\(C=R_1\\sin^2\\theta_1\\)</span>. Since <span class="math inline">\\(R_2\\ge0\\)</span> and <span class="math inline">\\(s^2\\le1\\)</span>, (5.7) forces <span class="math inline">\\(R_1\\sin^2\\theta_1\\le R_2\\)</span>: a real transmitted angle exists only below this barrier and the turning point is equality. The scalar inequality <span class="math inline">\\(g\\ge0,\\ s^2\\le1,\\ gs^2=C\\Rightarrow C\\le g\\)</span> is the declaration <code>AtlasFormal.refraction_turning_barrier</code> at revision <code>'+REV21+'</code> (draft PR #21, workflow run '+RUN21+', axiom audit and leanchecker passed, four false controls rejected). The variational derivation of (5.6) and the corner conditions remain [T]. <strong>[L]</strong></p>')
m=re.search(r'\\tag\{5\.7\}\s*\\\]</span>',s); assert m, 'tag 5.7'
j=s.find('</p>',m.end()); s=s[:j+4]+'\n'+rem57+s[j+4:]; log.append('E8 remark after (5.7)')
rem31=('<p><strong>Certified tangent-split remark (edition 7).</strong> For an idempotent <span class="math inline">\\(P\\)</span> and any <span class="math inline">\\(D\\)</span> with <span class="math inline">\\(PD+DP=D\\)</span>, <span class="math display">\\[ D=PD(I-P)+(I-P)DP. \\]</span> Every tangent to the idempotent manifold is exactly its two cross-subspace blocks, which is the finite form of the tangent constraint used above. This is <code>AtlasFormal.tangent_split</code> at revision <code>'+REV21+'</code> (draft PR #21, run '+RUN21+'), proved for any ring; it adds no statement about the metric or curvature. <strong>[L]</strong></p>\n')
m=re.search(r'<h2 id="[^"]*">3\.2 ',s); assert m
s=s[:m.start()]+rem31+s[m.start():]; log.append('E8 remark end of 3.1')

# E9 [L] tokens on certified environments (first [T] token after the environment head, within 4000 chars)
def add_L(head,note):
    global s
    mm=re.search(wpat(head),s); assert mm, head; i=mm.start()
    k=s.find('<strong>[T]</strong>',i); assert 0<k-i<4000, (head,k-i)
    s=s[:k]+'<strong>[T]</strong> <strong>[L'+note+']</strong>'+s[k+len('<strong>[T]</strong>'):]; log.append(f'E9 [L] on {head[8:40]} (+{k-i} chars)')
add_L('<strong>Proposition 4.2 (mixed-marker positivity at every rank).</strong>','')
add_L('<strong>Corollary 4.4 (subgap nullspaces).</strong>',': kernel equality (4.8)')
add_L('<strong>Proposition 4.5 (unique two-pole tune-out).</strong>','')
add_L('<strong>Theorem 5.1 (coupling census).</strong>',': block identity (5.2)')
add_L('<strong>Proposition 5.4 (a specific calibration obstruction).</strong>','')
add_L('<strong>Theorem 5.5 (scalar parity).</strong>',': finite identity (5.14)')

# E10 Appendix B rewrite: new opening paragraph + B.1-B.3 after the existing table
oldB='<p>The supplied formalization contains 62 bridge declarations, 12\nconstitutive declarations, and eight rigidity declarations.'
newB=('<p>Two verified Lean revisions stand behind this manuscript. The light-ledger revision <code>'+REV7+'</code> (draft PR #7; workflow run '+RUN7+' succeeded on 6 September 2026 with build, axiom audit restricted to <code>propext</code>, <code>Classical.choice</code>, <code>Quot.sound</code>, <code>leanchecker</code> recheck, and four false statements mathematically rejected; the duplicate run '+RUN7X+' was cancelled by the workflow, not failed) supplies the 91 declarations counted below. The peel revision <code>OpticalMetric.lean</code> with SHA-256 <code>'+PEEL+'</code> (archived report status PASS; two false controls rejected) contains the same 12 constitutive declarations plus <code>weighted_mono</code>, <code>weighted_nonneg</code>, <code>peel_null_persists</code> and <code>positive_reweighting_null_equivalence</code>, so the honest combined inventory is 95 distinct declarations. Two further declarations are cited from the Atlas formalization revision <code>'+REV21+'</code> (draft PR #21, run '+RUN21+'). The source-file headers of the PR #7 revision still carry a pre-run “not compiled” notice; the workflow record, not the header, is the evidence. The PR #7 evidence artifact is retained by GitHub for thirty days from the run and should be re-run or committed before it lapses.</p>\n'
      '<p>The supplied formalization contains 62 bridge declarations, 12\nconstitutive declarations, and eight rigidity declarations.')
wrep(oldB,newB,label='E10 Appendix B opening')
rows=[
('Proposition 2.1','regularized weak-transport response','2.3','[T]','Rigidity: denominator_pos, regularized_pos, regulator_cap, null_direction, inverse_identity, antitone_in_singular_value','scalar model of one specified singular value; the operator-norm identity (2.4) is written','written proof; Lean scalar components'),
('Proposition 3.1','integer winding under a positive branch guard','3.3','[T]','none','—','written proof; numerical gates NCA-GATE-01, WINDING-LADDER-GATE-01'),
('Proposition 4.1','pure balanced marker','4.2','[T]','Examples: orthogonal_marker_det; Gram: gram_posSemidef','components only','written proof; COMPLEMENTARITY-GRAM-GATE-01'),
('Proposition 4.2','mixed-marker positivity at every rank','4.2','[T] [L]','Gram: markerGram_posSemidef, gram_posSemidef','full statement for any W, U','kernel-certified Lean'),
('Theorem 4.3','transition-resolved constitutive weighting','4.8','[T]','OpticalMetric: response_is_weighted_metric, static_response, constant_gap_factor','single-transition scalar case; matrix symmetrization written','written proof; A.3 constitutive verifier'),
('Corollary 4.4','subgap nullspaces','4.9','[T] [L]','LightCompletion: weighted_matrix_kernel, response_metric_matrix_kernels; OpticalMetric bounds','kernel equality (4.8) full; Loewner bounds scalar/diagonal; derivation of J written','kernel-certified Lean (kernel equality); written proof (bounds)'),
('Proposition 4.5','unique two-pole tune-out','4.9','[T] [L]','LightCompletion: two_pole_zero_between, two_pole_numerator, two_pole_zero_iff, two_pole_tuneout','full statement','kernel-certified Lean'),
('Proposition 4.5a','positive response difference','4.9a','[T]','nearest: weighted_matrix_kernel (kernel step only)','divided-difference identity not formalized','written proof; atlas card OPT-TWO-FREQUENCY, intake pending'),
('Proposition 4.5b','probe certificate or invisible perturbation','4.9b','[T]','none','—','written proof; rational certificates not yet in the repository'),
('Proposition 4.5c','positive peel and surviving silent space','4.9c','[T]','peel revision: weighted_mono, weighted_nonneg, peel_null_persists, positive_reweighting_null_equivalence','scalar diagonal weights; ker G_t = U_t^⊥, rank and one-sided count written','written proof; archived scalar Lean components'),
('Corollary 4.5d','optical certificate for removed coupling','4.9c','[T]','none in either revision','—','written proof; check_light_peel.py exact checks not yet in the repository'),
('Proposition 4.5e','support from finitely many signed responses (was 4.9d.1)','4.9d','[T]','none','—','written proof; exact third-reading example'),
('Theorem 5.1','coupling census','5.1','[T] [L]','Census: projector_block_coupling, transition_weight_lower, transition_census_budget, transition_window_iff_weight, census_equals_coupling_count; Algebra: boundary_defect_of_block_idempotence','(5.2) full; (5.3) count algebra given the eigenvalues; spectral mapping written','kernel-certified Lean (5.2); written proof (5.3)'),
('Corollary 5.2','filtered channel bound','5.1','[T]','Census: filtered_response_range, filtered_response_finrank; Gram: filtered_gram_posSemidef','rank inequality full; threshold count written','written proof; Lean rank component'),
('Proposition 5.3','interface matching for the scalar action','5.2','[T]','Rigidity: interface_from_common_kinetic_factor, regulated_interface_iff; OpticalMetric: squared_phase_matching','matching algebra after the variational step','written proof; Lean matching component'),
('Proposition 5.4','a specific calibration obstruction (was 5.1)','5.2','[T] [L]','LightCompletion: calibration_product_strict, no_fixed_calibration_for_field_jacobian','full statement as displayed','kernel-certified Lean'),
('Theorem 5.5','scalar parity (was 5.4)','5.4','[T] [L]','Ledger: fixed_family_transpose, fixed_family_det_even, inverse_transpose_pair, inverse_transpose_trace, trace_symmetric_skew_zero','(5.14) full for finite matrices; contour evenness written','kernel-certified Lean (5.14); written proof (contour)'),
('Remark 3.1','certified tangent split','3.1','[L]','AtlasFormal: tangent_split (PR #21)','full statement, any ring','kernel-certified Lean'),
('Remark 5.2','certified turning-point barrier','5.2','[L]','AtlasFormal: refraction_turning_barrier (PR #21)','scalar inequality only','kernel-certified Lean'),
]
tbl='<h2 id="b.1-claim-by-claim-audit">B.1 Claim-by-claim audit (edition 7)</h2>\n<p>Every theorem-like environment in the paper, its grade tokens, the Lean declarations that support it at the revisions named above, what those declarations actually cover, and the evidence class the statement may honestly carry. Declarations are in the PR #7 revision unless marked otherwise.</p>\n<table>\n<thead><tr class="header"><th style="text-align: left;">Statement</th><th style="text-align: left;">Title</th><th style="text-align: left;">§</th><th style="text-align: left;">Grades</th><th style="text-align: left;">Lean declarations</th><th style="text-align: left;">Lean coverage</th><th style="text-align: left;">Evidence class</th></tr></thead>\n<tbody>\n'
for i,r in enumerate(rows):
    tbl+='<tr class="%s">'%('odd' if i%2==0 else 'even')+''.join('<td style="text-align: left;">%s</td>'%c for c in r)+'</tr>\n'
tbl+='</tbody>\n</table>\n'
tbl+=('<h2 id="b.2-declarations-supporting-prose">B.2 Declarations that support prose rather than a numbered statement</h2>\n'
'<p>Forty-seven of the 91 PR #7 declarations are not attached to a numbered environment. They are section support, not additional theorems, and are listed so the inventory can be traced: Algebra <code>redistribute_expansion</code>, <code>redistribute_double_commutator</code>, <code>redistribute_zero_of_commuting</code> (§3.2), <code>symmetric_skew_commutator</code> (eq. 2.1), <code>involution_factorization</code> (no matching display); Gram <code>frame_projector_idempotent</code>, <code>frame_projector_selfadjoint</code>, <code>frame_angle_kernel</code> (§3.7, eq. 3.9), <code>displacement_gram</code>, <code>graph_parallelogram</code> (§7.2–7.3); Census <code>boundary_mixing_peak</code> (§5.1 half-occupation remark); Coherence <code>covariant_square</code>, <code>tetrahedral</code>, <code>face_flat_iff</code>, <code>compression_associator</code>, <code>compression_associator_zero</code> (§7.5, A.2); Boundary <code>schur_interior_residual</code>, <code>schur_boundary_residual</code>, <code>boundary_lift_identity</code>, <code>boundary_hermitian_identity</code>, <code>boundary_accretive</code> (§8.6), <code>cayley_defect_identity</code>, <code>cayley_contractivity</code>, <code>boundary_loss_pullback</code>, <code>passive_boundary_chain</code> (§8.7, A.2); Ledger <code>inverse_pair_unique</code> (helper), <code>real_pairing_zero</code> (§8.5); ScalarOptics <code>smith_power_identity</code>, <code>smith_passive</code>, <code>sheet_power_sum</code>, <code>sheet_absorption_gap</code>, <code>sheet_absorption_bound</code> (§8.7), <code>threshold_exact_remainder</code> (§5.2 threshold), <code>isospectral_response_identity</code>, <code>probe_response_separates</code> (§8.8); Examples <code>obliqueP0_idempotent</code>, <code>obliqueP1_idempotent</code>, <code>oblique_trace_two</code> (§3.7 control), <code>separatedGram_value</code>, <code>separatedGram_singular</code>, <code>pairwise_separation_values</code> (§5.1 control), <code>stress_commutator</code>, <code>stress_exceeds_one</code> (§2.2), <code>real_round_trip_nonnegative</code> (§8.2); OpticalMetric <code>gram_zero_iff</code> (helper), <code>tune_out_metric_nonzero</code> (§4.9 remark); LightCompletion <code>same_metric_different_static_response</code> (§4.9 metric-only control). Sections 7 and 8 carry twenty-five certified declarations and no numbered statement; a future edition may promote the Schur–Cayley passivity chain and the sheet absorption bound to numbered results, which the backlog note of PR #29 rightly warns should be done for content, not count.</p>\n'
'<h2 id="b.3-what-is-not-formalized">B.3 What is not formalized, and what edition 7 did not do</h2>\n'
'<p>No Lean exists for Propositions 3.1, 4.1, 4.5a, 4.5b, 4.5e and Corollary 4.5d. The Lean behind Propositions 2.1, 4.3 and 4.5c is a scalar model of a matrix statement; the boxed operator-norm identity (2.4), the matrix symmetrization of (4.5) and the subspace statements of Proposition 4.5c are written proofs only. The exact certificates cited in §§4.9a–4.9c (<code>light_response_proofs.zip</code>, <code>check_light_peel.py</code>, <code>light_peel_checks.json</code>) are delivered files that are not yet in the repository, and the two atlas cards for 4.5a and 4.5b record “intake pending”. The Atlas formalization revision does not touch the two-frequency, probe-span or weighted-kernel results. Edition 7 performed no Lean compilation of its own; it cites the recorded runs. Newer electron and photon-loop material named in the editorial brief was not available in the repository or the shared hub at the time of this edition and has not been folded in.</p>\n')
rep('<h1 id="appendix-c.-publication-files">', tbl+'<h1 id="appendix-c.-publication-files">', label='E10 Appendix B.1-B.3')

# E11 Appendix A.5
a5=('<h2 id="a.5-what-was-executed-for-edition-7">A.5 What was executed for edition 7</h2>\n'
'<p>Edition 7 executed no new numerical gate, no new Lean build and no new measurement. What was executed: a structural extraction of edition 6 (17 environments, 17 figures, 135 display equations, 37 references); a claim-by-claim comparison of every environment against the declaration lists of the two Lean revisions and the Atlas formalization branch, recorded in Appendix B.1; a rendering check in headless Chromium at 1000-pixel and 420-pixel widths, in which no display equation exceeds its column at desktop width after the scroll boxes were removed; and a colour audit of all seventeen figures, in which the admissible-domain plot (§3.3) was the only figure on a light background and was reset to the manuscript palette with its data unchanged. The edition 6 verification records in A.1–A.4 are inherited unchanged.</p>\n')
rep('<h1 id="appendix-b.-formalization-scope">', a5+'<h1 id="appendix-b.-formalization-scope">', label='E11 A.5')
m=re.search(r'<li><a href="#a\.4-rigidity-and-regulator-audit"[^>]*>A\.4 Rigidity and regulator\s+audit</a></li>',s)
if m:
    s=s[:m.end()]+'\n<li><a href="#a.5-what-was-executed-for-edition-7" id="toc-a.5">A.5 What was executed for edition 7</a></li>'+s[m.end():]; log.append('E11 TOC entry added')
else: log.append('E11 TOC A.4 entry not found; skipped')

# E12 Appendix C
wrep('<p>The exact verified source commit is\n<code>41d9523a53ad679d2240e5e40ed07a7ea0cc2bac</code>',
    '<p>Edition 7 is published as this HTML, a PDF printed from it with the same palette, <code>LIGHT_CHANGELOG.md</code> (every change with its evidence grade), <code>claim_audit.md</code> (the working audit behind Appendix B.1) and a source package holding the Lean files of both revisions, the verification scripts and the seventeen figures.</p>\n<p>The exact verified source commit is\n<code>41d9523a53ad679d2240e5e40ed07a7ea0cc2bac</code>', label='E12 Appendix C')

# fit-script floor
rep('Math.max(0.55,cw/w)','Math.max(0.4,cw/w)',label='fit floor')
open('Light_Research_Edition_7.html','w',encoding='utf-8').write(s)
print('\n'.join(log)); print('size',len(s),'sha256',hashlib.sha256(s.encode()).hexdigest())
