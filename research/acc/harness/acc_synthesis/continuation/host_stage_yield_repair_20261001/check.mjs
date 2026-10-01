import fs from 'node:fs';
import assert from 'node:assert/strict';
const source = fs.readFileSync(new URL('../../helpers/host_driver.js', import.meta.url), 'utf8');
const start = source.indexOf('async function shell(cmd){');
const end = source.indexOf('\n async function refresh()', start);
assert(start >= 0 && end > start);
const factory = new Function('tools', 'parent', 'return (' + source.slice(start, end).trim() + ')');
let polls = 0;
const yielded = factory({
  exec_command: async () => ({output: '{"v":', session_id: 42}),
  write_stdin: async args => {
    assert.equal(args.session_id, 42);
    polls++;
    return polls === 1 ? {output: '3', session_id: 42} : {output: '}', exit_code: 0};
  }
}, '/tmp');
assert.equal(await yielded('stage'), '{"v":3}');
assert.equal(polls, 2);
const crashed = factory({
  exec_command: async () => ({output: 'partial', session_id: 43}),
  write_stdin: async () => ({output: 'crash', exit_code: -4})
}, '/tmp');
await assert.rejects(() => crashed('stage'), /exit -4.*partialcrash/);
console.log(JSON.stringify({yielded_session_resumed: true, chunks_preserved: true, negative_exit_rejected: true}));
