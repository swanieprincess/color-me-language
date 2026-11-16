import sys, asyncio
from playwright.async_api import async_playwright
async def main(html, out):
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/opt/pw-browsers/chromium")
        pg = await b.new_page()
        await pg.goto("file://" + html)
        await pg.wait_for_timeout(500)
        await pg.pdf(path=out, format="Letter", print_background=True, prefer_css_page_size=True)
        await pg.screenshot(path=out.replace(".pdf", ".png"), full_page=True)
        await b.close()
asyncio.run(main(sys.argv[1], sys.argv[2]))
