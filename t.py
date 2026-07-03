
from playwright.sync_api import sync_playwright
logs=[]
with sync_playwright() as pw:
    b = pw.chromium.launch(headless=True, args=["--use-gl=swiftshader","--enable-webgl","--ignore-gpu-blocklist","--no-sandbox"])
    pg = b.new_page(viewport={"width":1500,"height":950})
    pg.on("console", lambda m: logs.append("[%s] %s"%(m.type,m.text[:200])))
    pg.on("pageerror", lambda e: logs.append("[PAGEERROR] "+str(e)[:250]))
    pg.goto("file:///workspace/consorcio_verde_ecoinvest_v9.html", wait_until="domcontentloaded")
    pg.wait_for_timeout(2500)
    pg.click("[onclick*=\"'c5'\"]")
    try:
        pg.wait_for_selector("#arcgisMap canvas", timeout=90000)
        print("CANVAS_OK")
    except Exception:
        print("CANVAS_FAIL")
        print("container:", pg.eval_on_selector("#arcgisMap","e=>e.innerHTML.slice(0,300)"))
    pg.wait_for_timeout(12000)
    el = pg.query_selector("#c5"); el.screenshot(path="/workspace/teste_mapa_c5.png")
    pg.click("[onclick*=\"'c1'\"]"); pg.wait_for_timeout(400)
    print("NAV_OK:", pg.eval_on_selector("#c1","e=>e.classList.contains('active')"))
    b.close()
print("---- console ----")
for l in logs[:45]: print(l)
