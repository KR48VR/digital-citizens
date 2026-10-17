"""Download World Values Survey wave 7 country files (CSV codes, CSV text labels, codebook) with the container browser.
No login is required; the WVS terms of use (research use, cite the WVS) apply. Files are saved under data/raw/wvs (git-ignored).
Usage: .venv/bin/python scripts/download_wvs.py data/raw/wvs   (needs: uv pip install playwright; Chromium at /opt/pw-browsers/chromium)
"""
import asyncio, sys
from pathlib import Path
from playwright.async_api import async_playwright

OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
FILES = {  # DOID -> (country row to click, label)
    "13161": ("Singapore 2020", "sg_csv"), "13331": ("Singapore 2020", "sg_csvtext"), "11395": ("Singapore 2020", "sg_codebook"),
    "13125": ("China 2018", "cn_csv"), "13295": ("China 2018", "cn_csvtext"),
    "13169": ("USA 2017", "us_csv"), "13339": ("USA 2017", "us_csvtext"),
}

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/opt/pw-browsers/chromium")
        ctx = await b.new_context(accept_downloads=True)
        pg = await ctx.new_page()
        await pg.goto("https://www.worldvaluessurvey.org/WVSDocumentationWV7.jsp", wait_until="networkidle", timeout=90000)
        fr = next(f for f in pg.frames if "AJDocumentation.jsp" in f.url)
        for doid, (country, label) in FILES.items():
            await fr.get_by_text(country, exact=True).click(); await pg.wait_for_timeout(2500)
            sf = next(f for f in pg.frames if "AJDocumentationSmpl" in f.url)
            try:
                async with pg.expect_download(timeout=120000) as dl_info:
                    await sf.evaluate(f"DocDownload('{doid}')")
                dl = await dl_info.value
                dest = OUT / dl.suggested_filename
                await dl.save_as(dest)
                print("saved", label, dest.name, dest.stat().st_size, "bytes")
            except Exception as e:
                print("FAILED", label, doid, type(e).__name__, str(e)[:200])
            await pg.wait_for_timeout(1500)
        await b.close()
asyncio.run(main())
