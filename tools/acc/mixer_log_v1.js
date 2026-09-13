// mixer_log v1 — record one run through the frozen Compound Eye mixer.
//
// This is the project's logging, tracking and tracing path. Every lane (ACC,
// Lean, FrontierMath, anything else) hands a run to this recorder and it:
//
//   1. builds a compound-eye-traces-v1 dataset from the run's channels;
//   2. VALIDATES it through tools/compound-eye/projects/eye_mixer/mixer_core.js,
//      which is frozen and never modified, so the record cannot drift from the
//      instrument;
//   3. runs the mixer defaults and records whether the unit guard refused —
//      a refusal is a real finding about the run, not an error to suppress;
//   4. emits a compound-eye-mixer-recipe-v1 so the composition replays exactly;
//   5. appends one line to the append-only run ledger.
//
// A run with no numeric channels is recorded honestly as mixable:false with no
// fabricated coordinate. Inventing a coordinate to make something mixable would
// be the same error as fitting a pairing after seeing the outcome.
//
// Usage:
//   node tools/acc/mixer_log_v1.js record <run.json>
//   node tools/acc/mixer_log_v1.js record -            # read JSON on stdin
//
// Run JSON fields:
//   required: lane, run_id, claim, evidence, status
//   optional: title, reproduce, caveat, depends_on, supersedes, source,
//             object_id, model_id, coordinate, x_unit, x, channels, observed
//   channels: [{id, label, unit, values}]

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..');
const E = require(path.join(ROOT, 'tools/compound-eye/projects/eye_mixer/mixer_core.js'));

const LEDGER_DIR = path.join(ROOT, 'ledger', 'mixer');
const LEDGER = path.join(LEDGER_DIR, 'run_ledger_v1.jsonl');

// Same vocabulary as research/acc/dag/schema.md, so one claim language covers
// the whole repository.
const EVIDENCE = new Set(['exact-replay', 'computation', 'repo-provenance',
                          'external-source', 'none']);
const STATUS = new Set(['verified', 'refuted', 'open', 'blocked']);

function fail(msg) {
  console.error('mixer_log: ' + msg);
  process.exit(2);
}

function slug(s) {
  return String(s).replace(/[^A-Za-z0-9._-]+/g, '-').replace(/^-+|-+$/g, '');
}

function buildDataset(run) {
  const channels = run.channels || [];
  const x = run.x || channels.length ? (run.x || channels[0].values.map((_, i) => i)) : [];
  const traces = channels.map((c, k) => {
    if (!c.id || !Array.isArray(c.values)) fail('each channel needs id and values[]');
    if (c.values.length !== x.length) {
      fail(`channel ${c.id} has ${c.values.length} values but the coordinate has ${x.length}`);
    }
    return {
      id: slug(c.id),
      label: c.label || c.id,
      unit: c.unit || 'undeclared unit',
      source: c.source || `${run.lane} run ${run.run_id}`,
      color: E.colors[k % E.colors.length],
      values: c.values,
      defaultRoute: k === 0 ? 'x' : 'y',
    };
  });
  return E.validate({
    schema: 'compound-eye-traces-v1',
    id: slug(run.lane + '__' + run.run_id),
    title: run.title || `${run.lane} / ${run.run_id}`,
    description: run.claim,
    context: {
      object_id: run.object_id || run.lane,
      model_id: run.model_id || run.run_id,
      coordinate: run.coordinate || 'step',
      x_unit: run.x_unit || 'index',
      // The frozen schema already carries a provenance field. Evidence class
      // goes here, so the instrument itself records how much weight the run has.
      source_stage: run.evidence,
    },
    x,
    traces,
  });
}

function record(run) {
  for (const f of ['lane', 'run_id', 'claim', 'evidence', 'status']) {
    if (!run[f]) fail(`missing required field: ${f}`);
  }
  if (!EVIDENCE.has(run.evidence)) {
    fail(`evidence must be one of ${[...EVIDENCE].join(', ')}`);
  }
  if (!STATUS.has(run.status)) {
    fail(`status must be one of ${[...STATUS].join(', ')}`);
  }
  if (run.status === 'verified' && run.evidence === 'none') {
    fail('a verified run needs evidence stronger than none (DAG invariant 4)');
  }

  const lane = slug(run.lane);
  const runId = slug(run.run_id);
  const outDir = path.join(LEDGER_DIR, lane);
  fs.mkdirSync(outDir, { recursive: true });

  const channels = run.channels || [];
  const row = {
    schema: 'compound-eye-run-ledger-v1',
    recorded_utc: new Date().toISOString(),
    lane,
    run_id: runId,
    claim: run.claim,
    status: run.status,
    evidence: run.evidence,
    reproduce: run.reproduce || null,
    caveat: run.caveat || null,
    depends_on: run.depends_on || [],
    supersedes: run.supersedes || null,
    source: run.source || null,
    observed: run.observed || null,
    mixable: channels.length > 0,
  };

  if (!channels.length) {
    // Honest boundary: no numeric channels means nothing to mix. Record the
    // claim and its evidence, and say plainly that no trace exists.
    row.traces_path = null;
    row.recipe_path = null;
    row.channel_count = 0;
    row.note = 'no numeric channels on a common coordinate; recorded as a claim only';
  } else {
    const dataset = buildDataset(run);
    const defaults = E.defaults(dataset);

    // The unit guard is a measurement, not an error. If the mixer refuses to
    // combine these channels under source units, that fact is the finding.
    let unitsCommensurable = true;
    let refusal = null;
    let mixed;
    try {
      mixed = E.mix(dataset, defaults);
    } catch (err) {
      unitsCommensurable = false;
      refusal = err.message;
      defaults.normalization = 'rms';
      mixed = E.mix(dataset, defaults);
    }

    const recipe = E.recipe(dataset, defaults);

    // Round trip: recipe -> read -> mix must reproduce the same combined array.
    const back = E.read(JSON.stringify(recipe));
    const again = E.mix(back.dataset, back.settings);
    const roundtrip = JSON.stringify(again.combined) === JSON.stringify(mixed.combined);

    const tracesPath = path.join(outDir, `${runId}.traces.json`);
    const recipePath = path.join(outDir, `${runId}.recipe.json`);
    fs.writeFileSync(tracesPath, JSON.stringify(dataset, null, 1));
    fs.writeFileSync(recipePath, JSON.stringify(recipe, null, 1));

    Object.assign(row, {
      traces_path: path.relative(ROOT, tracesPath),
      recipe_path: path.relative(ROOT, recipePath),
      channel_count: dataset.traces.length,
      coordinate: dataset.context.coordinate,
      x_unit: dataset.context.x_unit,
      points: dataset.x.length,
      units_commensurable: unitsCommensurable,
      unit_guard_message: refusal,
      normalization: mixed.normalization,
      active_channels: mixed.activeCount,
      rms_combined: mixed.rmsCombined,
      rms_residual: mixed.rmsResidual,
      missing: mixed.missing,
      roundtrip_ok: roundtrip,
    });
    if (!roundtrip) row.note = 'RECIPE ROUND TRIP FAILED — this run does not replay';
  }

  fs.mkdirSync(LEDGER_DIR, { recursive: true });
  fs.appendFileSync(LEDGER, JSON.stringify(row) + '\n');
  return row;
}

function main() {
  const [cmd, arg] = process.argv.slice(2);
  if (cmd !== 'record' || !arg) {
    console.error('usage: node tools/acc/mixer_log_v1.js record <run.json|->');
    process.exit(2);
  }
  const text = arg === '-' ? fs.readFileSync(0, 'utf8') : fs.readFileSync(arg, 'utf8');
  let runs = JSON.parse(text);
  if (!Array.isArray(runs)) runs = [runs];
  const rows = runs.map(record);
  for (const r of rows) {
    const bits = [r.lane + '/' + r.run_id, r.status, r.evidence];
    if (r.mixable) {
      bits.push(`${r.channel_count} channels`,
                r.units_commensurable ? 'units commensurable' : 'unit guard refused',
                r.roundtrip_ok ? 'replays' : 'REPLAY FAILED');
    } else {
      bits.push('claim only');
    }
    console.log('recorded  ' + bits.join('  |  '));
  }
}

if (require.main === module) main();
module.exports = { record, buildDataset, LEDGER, EVIDENCE, STATUS };
