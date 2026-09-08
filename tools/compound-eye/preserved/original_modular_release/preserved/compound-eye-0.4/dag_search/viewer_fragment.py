"""Embed the completed search report in the existing standalone viewer."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parent


def build():
    audit = json.loads((ROOT/'results/complete_bundle_audit.json').read_text())
    if not audit['all_passed']:
        raise ValueError('Cannot display an unverified bundle as completed.')
    html = (ROOT/'EXECUTION_REPORT.html').read_text()
    body = re.search(r'<body[^>]*>([\s\S]*?)</body>', html).group(1)
    body = body.replace('id="title-block-header"', 'id="execution04-report-title"')
    style = '''<style>
    #execution04{background:#081322;color:#e5edf8;border:1px solid #2b4665;border-radius:16px;padding:26px;margin:0 0 32px;font:17px/1.7 system-ui,sans-serif}
    #execution04 .eyebrow{color:#83ddf1;letter-spacing:.1em;font-size:12px;text-transform:uppercase}
    #execution04 h2{color:#f0cf8b;margin:8px 0 18px;font:600 30px/1.25 Georgia,serif}
    #execution04 .cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:14px;margin:22px 0}
    #execution04 .card{padding:18px;background:#10243a;border:1px solid #2b4665;border-radius:10px}
    #execution04 .number{display:block;color:#f0cf8b;font-size:30px;line-height:1.3}
    #execution04 .label{color:#c9d8e9;font-size:14px}
    #execution04 details{border-top:1px solid #2b4665;margin-top:22px;padding-top:16px}
    #execution04 summary{cursor:pointer;color:#83ddf1;font-weight:600}
    #execution04 .report{padding-top:26px;overflow-wrap:anywhere}
    #execution04 .report p{margin:0 0 22px}
    #execution04 .report h1{color:#f0cf8b;font:600 36px/1.2 Georgia,serif;margin:0 0 18px}
    #execution04 .report .subtitle{color:#83ddf1;font-size:21px}
    #execution04 .report .date{font-size:14px;color:#b3c5da}
    #execution04 strong{color:#f0cf8b}
    #execution04 a{color:#83ddf1;text-decoration:underline}
    #execution04 table{display:block;width:100%;overflow-x:auto;border-collapse:collapse;font-size:15px;margin:24px 0;background:#0e2035}
    #execution04 th,#execution04 td{text-align:left;vertical-align:top;border:1px solid #2b4665;padding:13px;min-width:160px}
    #execution04 th{color:#f0cf8b;background:#122942}
    #execution04 pre{background:#06101c;border:1px solid #2b4665;border-radius:6px;padding:18px;overflow-x:auto}
    #execution04 code{color:#b7effa;font-size:.88em}
    #execution04 math{color:#f3e6c8}
    #execution04 math[display="block"]{display:block;overflow-x:auto;margin:20px 0;padding:18px;background:#10243a;border-left:3px solid #f0cf8b}
    </style>'''
    return style+'''<section id="execution04">
    <div class="eyebrow">Compound Eye · edition 0.4 · checked search memory</div>
    <h2>Remember the reason. Share the work.</h2>
    <p>The decision DAG and reusable obstruction records are implemented. Every declared finite region has a checked coverage certificate.</p>
    <div class="cards"><div class="card"><span class="number">470,232</span><span class="label">distinct new Kakeya configurations excluded</span></div>
    <div class="card"><span class="number">24,976</span><span class="label">new Earth–Moon graphs excluded</span></div>
    <div class="card"><span class="number">35.9×</span><span class="label">faster baseline proof production and checking; raw search time unchanged</span></div></div>
    <p>All initial known sets are covered at the target score for 33 specified Kakeya tower-and-pool cases. Both full Epoch problems remain open. The earlier light and flow demonstrations continue below.</p>
    <details><summary>Read the complete execution report and reproduction instructions</summary><div class="report">'''+body+'''</div></details></section>'''
