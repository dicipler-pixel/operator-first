// eye_log v1 — the information-preserving compound eye.
//
// The mixer is a verifier AND a compound eye. It does not reduce work to
// PASS/FAIL and it does not force unlike outputs onto one axis. Two levels
// are kept, permanently and separately:
//
//   1. EVERY EYE KEEPS ITS OWN OUTPUT — its payload in its own shape, its
//      unit, assumptions, source, failure mode and evidence class. Nothing is
//      collapsed away. An eye at weight zero is stored in full.
//
//   2. COMBINATION IS OPT-IN AND SCOPED. Numeric addition happens only inside
//      a `commensurable_set` that an eye explicitly declares, and only when
//      mathematics genuinely supplies the shared coordinate. Eyes that declare
//      no set are never auto-grouped. There is no global x-axis.
//
// The unit guard means "do not falsely add unlike outputs", not "silence the
// eyes that cannot be added". A theorem eye, a null-space eye, a numerical
// search eye and a counterexample eye say different kinds of true things about
// one claim; that difference is the signal.
//
//   node tools/acc/eye_log_v1.js claim   <claim.json>
//   node tools/acc/eye_log_v1.js observe <observation.json|[...]>
//   node tools/acc/eye_log_v1.js mix     <claim_id>

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..');
const E = require(path.join(ROOT, 'tools/compound-eye/projects/eye_mixer/mixer_core.js'));
const LOG = require(path.join(ROOT, 'tools/acc/mixer_log_v1.js'));

// Tests point this at a scratch directory; the default is the real ledger.
const DIR = process.env.ACC_EYE_DIR || path.join(ROOT, 'ledger', 'eyes');
const CLAIMS = path.join(DIR, 'claims_v1.jsonl');
const OBS = path.join(DIR, 'observations_v1.jsonl');
const SETS = path.join(DIR, 'sets_v1.jsonl');

// What an eye can say about a claim. None of these is a score.
//   supports   evidence for the claim
//   refutes    evidence against it
//   orthogonal a true statement about the object that does not settle the claim
//   obstructs  a structural barrier: why this route cannot close
//   silent     the instrument exists but has no input it can see
const VERDICT = new Set(['supports', 'refutes', 'orthogonal', 'obstructs', 'silent']);

function fail(m) { console.error('eye_log: ' + m); process.exit(2); }
function slug(s) { return String(s).replace(/[^A-Za-z0-9._-]+/g, '-').replace(/^-+|-+$/g, ''); }
function readJsonl(p) {
  if (!fs.existsSync(p)) return [];
  return fs.readFileSync(p, 'utf8').split('\n').filter(l => l.trim()).map(JSON.parse);
}
function append(p, row) {
  fs.mkdirSync(path.dirname(p), { recursive: true });
  fs.appendFileSync(p, JSON.stringify(row) + '\n');
  return row;
}

// A JSON number past 2^53 has already lost digits by the time JSON.parse hands
// it over — a discriminant near 1e29 silently becomes the wrong integer. Refuse
// it rather than store a corrupted value that looks exact.
function checkExactIntegers(value, where) {
  if (typeof value === 'number' && Math.abs(value) > Number.MAX_SAFE_INTEGER) {
    fail(`${where}: ${value} is past 2^53 and JSON.parse has already rounded it. ` +
         `Quote large integers as strings so the digits survive.`);
  }
  if (value && typeof value === 'object') {
    for (const [k, v] of Object.entries(value)) checkExactIntegers(v, `${where}.${k}`);
  }
}

function recordClaim(c) {
  for (const f of ['claim_id', 'claim']) if (!c[f]) fail(`claim needs ${f}`);
  if (!Array.isArray(c.eyes_wanted) || !c.eyes_wanted.length) {
    fail('a claim must declare eyes_wanted: the roster of eyes that ought to see it. ' +
         'Eyes on the roster with no observation are the blind spots, and naming ' +
         'them is how the report can say what no eye could see.');
  }
  return append(CLAIMS, {
    schema: 'compound-eye-claim-v1',
    written_utc: new Date().toISOString(),
    claim_id: slug(c.claim_id),
    claim: c.claim,
    handoff_id: c.handoff_id || null,   // the sealed envelope that fixed this claim
    eyes_wanted: c.eyes_wanted,
    note: c.note || null,
  });
}

function recordObservation(o) {
  for (const f of ['claim_id', 'eye_id', 'verdict', 'evidence']) {
    if (!o[f]) fail(`observation needs ${f}`);
  }
  if (!VERDICT.has(o.verdict)) fail(`verdict must be one of ${[...VERDICT].join(', ')}`);
  if (!LOG.EVIDENCE.has(o.evidence)) fail(`evidence must be one of ${[...LOG.EVIDENCE].join(', ')}`);

  // An eye that moves the claim needs something behind it.
  if ((o.verdict === 'supports' || o.verdict === 'refutes') && o.evidence === 'none') {
    fail(`${o.eye_id}: a verdict of ${o.verdict} needs evidence stronger than none`);
  }
  // A silent eye must say what it is waiting for, or it is just absent.
  if (o.verdict === 'silent' && !o.blocked_on) {
    fail(`${o.eye_id}: a silent eye must declare blocked_on — the capability or input ` +
         `that would let it see. That is what makes the blind spot addressable.`);
  }
  checkExactIntegers(o.output, `${o.eye_id}.output`);

  // Weight zero is legal and preserved. Negative weight is not a thing.
  const weight = o.weight === undefined ? 1 : Number(o.weight);
  if (!(weight >= 0)) fail(`${o.eye_id}: weight must be >= 0 (zero is allowed and kept)`);

  // Numeric combination is opt-in. No set declared means this eye is never
  // added to anything, and that costs it nothing.
  if (o.commensurable_set) {
    for (const f of ['unit', 'coordinate', 'x_unit', 'x', 'values']) {
      if (o[f] === undefined) {
        fail(`${o.eye_id}: joining set '${o.commensurable_set}' requires ${f}; ` +
             `an eye without a genuine shared coordinate must leave ` +
             `commensurable_set unset rather than have one invented for it`);
      }
    }
    if (o.x.length !== o.values.length) {
      fail(`${o.eye_id}: ${o.values.length} values against ${o.x.length} coordinates`);
    }
  }

  return append(OBS, {
    schema: 'compound-eye-observation-v1',
    observed_utc: new Date().toISOString(),
    claim_id: slug(o.claim_id),
    eye_id: slug(o.eye_id),
    eye_kind: o.eye_kind || 'unspecified',
    sees: o.sees || null,
    verdict: o.verdict,
    weight,
    evidence: o.evidence,
    // The eye's own complete output, in the eye's own shape. Never flattened.
    output: o.output === undefined ? null : o.output,
    unit: o.unit || null,
    assumptions: o.assumptions || [],
    failure_mode: o.failure_mode || null,
    blocked_on: o.blocked_on || null,
    reproduce: o.reproduce || null,
    source: o.source || null,
    commensurable_set: o.commensurable_set || null,
    coordinate: o.coordinate || null,
    x_unit: o.x_unit || null,
    x: o.x || null,
    values: o.values || null,
  });
}

// Level 2. Combine only inside a declared set, through the frozen instrument.
function mixSets(claimId) {
  claimId = slug(claimId);
  const obs = readJsonl(OBS).filter(o => o.claim_id === claimId);
  if (!obs.length) fail(`no observations for claim ${claimId}`);

  const bySet = new Map();
  for (const o of obs) {
    if (!o.commensurable_set) continue;
    if (!bySet.has(o.commensurable_set)) bySet.set(o.commensurable_set, []);
    bySet.get(o.commensurable_set).push(o);
  }
  const ungrouped = obs.filter(o => !o.commensurable_set);
  const out = [];

  for (const [setId, members] of bySet) {
    // Weight zero stays in the record but contributes nothing to the scalar.
    const contributing = members.filter(m => m.weight > 0);
    const silenced = members.filter(m => m.weight === 0);
    if (!contributing.length) {
      out.push(append(SETS, {
        schema: 'compound-eye-set-v1', claim_id: claimId, set_id: setId,
        mixed: false, members: members.map(m => m.eye_id),
        zero_weight: silenced.map(m => m.eye_id),
        note: 'every eye in this set is at weight zero; kept in full, combined into nothing',
      }));
      continue;
    }
    const head = contributing[0];
    if (contributing.some(m => m.x.length !== head.x.length)) {
      fail(`set ${setId}: members disagree on the length of the shared coordinate`);
    }

    const dataset = LOG.buildDataset({
      lane: 'eyes', run_id: `${claimId}__${setId}`,
      title: `${claimId} / ${setId}`,
      claim: `set-level combination of ${contributing.length} commensurable eyes`,
      object_id: claimId, model_id: setId,
      coordinate: head.coordinate, x_unit: head.x_unit,
      evidence: contributing.map(m => m.evidence).sort(
        (a, b) => [...LOG.EVIDENCE].indexOf(a) - [...LOG.EVIDENCE].indexOf(b))[0],
      x: head.x,
      channels: contributing.map(m => ({
        id: m.eye_id, label: m.sees || m.eye_id, unit: m.unit, values: m.values,
        source: m.source ? JSON.stringify(m.source) : `eye ${m.eye_id}`,
      })),
    });

    const settings = E.defaults(dataset);
    // Carry the declared weights into the instrument.
    for (const t of settings.traces || []) {
      const m = contributing.find(c => c.eye_id === t.id);
      if (m && t.weight !== undefined) t.weight = m.weight;
    }

    // The unit guard firing is a finding about the set, not an error to hide.
    let commensurable = true, refusal = null, mixed;
    try { mixed = E.mix(dataset, settings); }
    catch (err) {
      commensurable = false; refusal = err.message;
      settings.normalization = 'rms';
      mixed = E.mix(dataset, settings);
    }

    const recipe = E.recipe(dataset, settings);
    const back = E.read(JSON.stringify(recipe));
    const roundtrip = JSON.stringify(E.mix(back.dataset, back.settings).combined)
                    === JSON.stringify(mixed.combined);

    const dir = path.join(DIR, claimId);
    fs.mkdirSync(dir, { recursive: true });
    const tp = path.join(dir, `${setId}.traces.json`);
    const rp = path.join(dir, `${setId}.recipe.json`);
    fs.writeFileSync(tp, JSON.stringify(dataset, null, 1));
    fs.writeFileSync(rp, JSON.stringify(recipe, null, 1));

    out.push(append(SETS, {
      schema: 'compound-eye-set-v1',
      mixed_utc: new Date().toISOString(),
      claim_id: claimId, set_id: setId, mixed: true,
      members: members.map(m => m.eye_id),
      contributing: contributing.map(m => m.eye_id),
      zero_weight: silenced.map(m => m.eye_id),
      coordinate: head.coordinate, x_unit: head.x_unit, points: head.x.length,
      units_commensurable: commensurable, unit_guard_message: refusal,
      normalization: mixed.normalization, active_channels: mixed.activeCount,
      rms_combined: mixed.rmsCombined, rms_residual: mixed.rmsResidual,
      missing: mixed.missing, roundtrip_ok: roundtrip,
      traces_path: path.relative(ROOT, tp), recipe_path: path.relative(ROOT, rp),
    }));
  }

  return { sets: out, ungrouped: ungrouped.map(o => o.eye_id) };
}

function main() {
  const [cmd, arg] = process.argv.slice(2);
  if (!cmd || !arg) {
    console.error('usage: node tools/acc/eye_log_v1.js claim|observe|mix <arg>');
    process.exit(2);
  }
  if (cmd === 'mix') {
    const { sets, ungrouped } = mixSets(arg);
    for (const s of sets) {
      if (!s.mixed) { console.log(`set ${s.set_id}: not mixed — ${s.note}`); continue; }
      console.log(`set ${s.set_id}: ${s.contributing.length} eyes on "${s.coordinate}"` +
        `  ${s.units_commensurable ? 'units commensurable' : 'UNIT GUARD REFUSED'}` +
        `  ${s.roundtrip_ok ? 'replays' : 'REPLAY FAILED'}` +
        (s.zero_weight.length ? `  (${s.zero_weight.length} at weight zero, kept)` : ''));
    }
    console.log(`${ungrouped.length} eye(s) declare no commensurable set and are ` +
                `combined with nothing — their output is kept whole.`);
    return;
  }
  const payload = JSON.parse(fs.readFileSync(arg, 'utf8'));
  const items = Array.isArray(payload) ? payload : [payload];
  for (const it of items) {
    const row = cmd === 'claim' ? recordClaim(it)
              : cmd === 'observe' ? recordObservation(it)
              : fail(`unknown command ${cmd}`);
    console.log(cmd === 'claim'
      ? `claim ${row.claim_id} — ${row.eyes_wanted.length} eyes wanted`
      : `eye ${row.eye_id} -> ${row.claim_id}  ${row.verdict}  w=${row.weight}  ${row.evidence}`);
  }
}

if (require.main === module) main();
module.exports = { recordClaim, recordObservation, mixSets, VERDICT,
                   CLAIMS, OBS, SETS, readJsonl };
