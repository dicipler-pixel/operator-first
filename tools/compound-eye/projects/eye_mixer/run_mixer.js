/* Reproduce a saved browser recipe outside the browser. */
const fs=require('fs'),path=require('path'),E=require('./mixer_core.js'),P=require('./mixer_plot.js');
if(process.argv.length<3){console.error('Usage: node projects/eye_mixer/run_mixer.js recipe.json [output_directory]');process.exit(2)}
const input=E.read(fs.readFileSync(process.argv[2],'utf8')),d=input.dataset,s=input.settings||E.defaults(d),out=path.resolve(process.argv[3]||'mixer_output');
fs.mkdirSync(out,{recursive:true});let m=E.mix(d,s),b=input.baseline?E.mix(input.baseline.dataset,input.baseline.settings):null;if(b&&b.unit!==m.unit)b=null;
fs.writeFileSync(path.join(out,'combined.csv'),E.csv(d,s));fs.writeFileSync(path.join(out,'combined.svg'),P.svg(d,s,m,b));
fs.writeFileSync(path.join(out,'results.json'),JSON.stringify({recipe:E.recipe(d,s,input.baseline),result:m},null,2));console.log(JSON.stringify({status:'complete',active_channels:m.activeCount,output_directory:out}));
