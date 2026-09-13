# playback51 — load recipes into the Canonical 5.1 page (the real app), draw, screenshot. usage: playback51.py out_dir recipe1 [recipe2 ...]
import asyncio, sys, os, json
from playwright.async_api import async_playwright
H='/tmp/claude-0/-home-user-operator-first/134a87db-34f4-5773-8170-2c301f6ca866/scratchpad/mixer51/Compound_Eye_Matrix_Mixer_Canonical_5_1.html'
out=sys.argv[1]; files=sys.argv[2:]; os.makedirs(out,exist_ok=True)
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
        pg=await b.new_page(viewport={'width':1400,'height':1100}); errors=[]; pg.on('pageerror', lambda e: errors.append(str(e)))
        await pg.goto('file://'+H, wait_until='load'); await pg.wait_for_timeout(1200)
        await pg.evaluate("()=>{const d=document.querySelector('#mixPaste')?.closest('details'); if(d) d.open=true}")
        for f in files:
            await pg.goto('file://'+H, wait_until='load'); await pg.wait_for_timeout(800)   # fresh page per file: the app keeps one 'imported' slot
            await pg.evaluate("()=>{const d=document.querySelector('#mixPaste')?.closest('details'); if(d) d.open=true}")
            await pg.fill('#mixPaste', open(f,encoding='utf-8').read()); await pg.click('#mixApplyPaste'); await pg.wait_for_timeout(600)
            r=await pg.evaluate("""()=>{const e=document.getElementById('mixError');const sel=document.getElementById('mixDataset');const st=document.getElementById('mixStatus')||document.querySelector('.mixstatus');
              return {error:(e&&!e.hidden)?e.textContent:null,title:sel.options[sel.selectedIndex]?.textContent,status:st?st.textContent.slice(0,300):null}}""")
            name=os.path.basename(f).replace('.json','')
            cv=await pg.query_selector('canvas, svg#mixPlot, #mixPlot')
            await pg.screenshot(path=os.path.join(out,name+'.png'), full_page=False)
            print(name, '->', r['title'], '| error:', r['error'], '| status:', (r['status'] or '')[:160])
        print('page errors:', errors[:3]); await b.close()
asyncio.run(main())
