# SCRIPT: MIXER-5-2-BROWSER-CHECK-01
import asyncio, sys
from playwright.async_api import async_playwright
async def run(path, tag):
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/opt/pw-browsers/chromium' if False else None)
        pg = await b.new_page(viewport={'width':1400,'height':900})
        errs=[]; pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda m: m.type=='error' and errs.append(m.text))
        await pg.goto('file://'+path); await pg.wait_for_timeout(2500)
        await pg.screenshot(path=f'{tag}_top.png')
        await pg.click('button[data-tab="catalog"]'); await pg.wait_for_timeout(800)
        cnt = await pg.inner_text('#count')
        await pg.select_option('#family', label='Phase Playground (coupled-waveguide phase)') if tag=='m52' else None
        await pg.wait_for_timeout(400); cnt2 = await pg.inner_text('#count')
        await pg.screenshot(path=f'{tag}_catalog.png')
        await pg.click('button[data-tab="recovery"]'); await pg.wait_for_timeout(600)
        rec = await pg.inner_text('#adapterRecovery') if await pg.query_selector('#adapterRecovery') else ''
        await pg.screenshot(path=f'{tag}_recovery.png')
        await pg.click('button[data-tab="mixer"]'); await pg.wait_for_timeout(800)
        await pg.screenshot(path=f'{tag}_mixer.png')
        print(tag, '| catalog:', cnt, '| filtered:', cnt2, '| errors:', errs[:5]); print('  recovery:', rec[:300].replace('\n',' '))
        await b.close()
asyncio.run(run(sys.argv[1], sys.argv[2]))
