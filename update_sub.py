import requests
import random
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

URL = "https://mibcloudb.com/"
OUTPUT_FILE = "Sub.txt"

SNI_LIST = [
    "amanita_design.samorost3.gp",
    "android",
    "au.com.shiftyjelly.pocketcasts",
    "bbc.mobile.news.ww",
    "be.mygod.vpnhotspot",
    "ch.protonmail.android",
    "co.wanqu.android",
    "com.alphainventor.filemanager",
    "com.amazon.kindle",
    "com.amazon.mshop.android.shopping",
    "com.android.chrome",
    "com.android.providers.downloads",
    "com.android.providers.downloads.ui",
    "com.android.providers.telephony",
    "com.android.settings",
    "com.android.vending",
    "com.discord",
    "com.spotify.music",
    "com.termux",
    "com.whatsapp",
    "org.telegram.messenger",
    "org.mozilla.firefox",
    "org.wikipedia",
    "com.ted.android"
]

FIXED_SNI = "www.speedtest.com"


def replace_sni(vless_url, new_sni):
    parsed = urlparse(vless_url)
    query = parse_qs(parsed.query)
    query["sni"] = [new_sni]
    new_query = urlencode(query, doseq=True)

    return urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        new_query,
        parsed.fragment
    ))


def main():
    r = requests.get(URL, timeout=15)
    r.raise_for_status()
    data = r.json()

    raw_configs = []
    raw_configs += data.get("add_config", "").strip().splitlines()
    raw_configs += data.get("ads_config", "").strip().splitlines()

    raw_configs = [c for c in raw_configs if c.startswith("vless://")]

    if not raw_configs:
        print("No configs found!")
        return

    output = []

    # یکی با speedtest
    first = replace_sni(raw_configs[0], FIXED_SNI)
    output.append(first)

    # بقیه رندوم
    for cfg in raw_configs[1:]:
        sni = random.choice(SNI_LIST)
        output.append(replace_sni(cfg, sni))

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(output))

    print(f"Written {len(output)} configs to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
