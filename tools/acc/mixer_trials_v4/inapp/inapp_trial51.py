# inapp_trial51 — run a predict->intervene->observe trial INSIDE the Canonical 5.1 page (the real app), export its ledger, screenshot the plot
import asyncio, sys, os, json, re
from playwright.async_api import async_playwright
H='/tmp/claude-0/-home-user-operator-first/134a87db-34f4-5773-8170-2c301f6ca866/scratchpad/mixer51/Compound_Eye_Matrix_Mixer_Canonical_5_1.html'
out=sys.argv[1]; recipe=sys.argv[2]; solo_label=sys.argv[3]; prediction=sys.argv[4]; os.makedirs(out,exist_ok=True)
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
        ctx=await b.new_context(viewport={'width':1400,'height':1000},accept_downloads=True); pg=await ctx.new_page(); errors=[]; pg.on('pageerror', lambda e: errors.append(str(e)))
        await pg.goto('file://'+H, wait_until='load'); await pg.wait_for_timeout(800)
        await pg.evaluate("()=>{const d=document.querySelector('#mixPaste')?.closest('details'); if(d) d.open=true}")
        await pg.fill('#mixPaste', open(recipe,encoding='utf-8').read()); await pg.click('#mixApplyPaste'); await pg.wait_for_timeout(500)
        title=await pg.evaluate("()=>{const s=document.getElementById('mixDataset');return s.options[s.selectedIndex]?.textContent}")
        stats0=await pg.evaluate("()=>document.getElementById('mixStats')?.textContent||''")
        # 1. predict, in the app
        await pg.fill('#mixPrediction', prediction); await pg.click('#mixStartTrial'); await pg.wait_for_timeout(200)
        # 2. intervene, in the app: press the Solo button of the named channel
        n=await pg.evaluate("""(label)=>{const boxes=[...document.querySelectorAll('.mixchannel')];const box=boxes.find(b=>b.textContent.includes(label));if(!box)return 'no box';const btn=[...box.querySelectorAll('button')].find(x=>x.textContent.trim()==='Solo');if(!btn)return 'no solo';btn.click();return boxes.length}""", solo_label)
        await pg.wait_for_timeout(400)
        # 3. observe, from the app's own stats line
        stats1=await pg.evaluate("()=>document.getElementById('mixStats')?.textContent||''")
        enabled=await pg.evaluate("()=>[...document.querySelectorAll('.mixchannel')].filter(b=>b.querySelector('input[type=checkbox]')?.checked).map(b=>b.querySelector('label,strong,b,span')?.textContent?.trim().slice(0,50))")
        await pg.fill('#mixObservation', f'stats after solo: {stats1.strip()[:400]} | enabled: {enabled}')
        await pg.select_option('#mixVerdict', sys.argv[5] if len(sys.argv)>5 else 'matched'); await pg.click('#mixCloseTrial'); await pg.wait_for_timeout(200)
        log=await pg.evaluate("()=>document.getElementById('mixTrialLog').textContent")
        # 4. export the app's ledger (real download)
        async with pg.expect_download() as dl: await pg.click('#mixExportTrials')
        d=await dl.value; path=os.path.join(out,'Compound_Eye_Intervention_Ledger_inapp.json'); await d.save_as(path)
        # 5. screenshot the plot
        await pg.evaluate("()=>window.scrollTo(0,0)"); await pg.wait_for_timeout(200)
        g=await pg.query_selector('#mixGraphic')
        if g: await g.screenshot(path=os.path.join(out,'plot_shape.png'))
        opts=await pg.evaluate("()=>[...document.getElementById('mixView').options].map(o=>o.value)")
        for v in opts:
            await pg.select_option('#mixView', v); await pg.wait_for_timeout(300)
            g=await pg.query_selector('#mixGraphic')
            if g: await g.screenshot(path=os.path.join(out,f'plot_{v}.png'))
        print('views:',opts)
        await pg.screenshot(path=os.path.join(out,'page_top.png'))
        print('title:',title); print('channels boxes:',n); print('stats before:',stats0.strip()[:300]); print('stats after :',stats1.strip()[:300]); print('enabled after solo:',enabled)
        print('app ledger saved:',path,'trials:',len(json.load(open(path))['trials'])); print('page errors:',errors[:3])
        await b.close()
asyncio.run(main())
