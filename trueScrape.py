import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import re

df = pd.read_csv("dnd_monsters.csv")
df = df[df["source"] != "Essentials Kit"] # drop essentials since theyre all the same human? not sure about this so go over again
print("Remaining rows:", len(df))


def safe_scrape(name, driver):
    url = f"https://www.aidedd.org/dnd/monstres.php?vo={name}"
    try:
        driver.get(url)
        time.sleep(3)

        carac_divs = driver.find_elements(By.CLASS_NAME, "carac")
        stats = {}
        for div in carac_divs:
            lines = div.text.strip().split("\n")
            if len(lines) >= 2:
                ability = lines[0].strip().lower()
                score = lines[1].strip().split(" ")[0]
                if ability in ["str", "dex", "con", "int", "wis", "cha"] and score.isdigit():
                    stats[ability] = int(score)

        if len(stats) == 6:
            return stats
        else:
            print(f"Incomplete stats ({len(stats)}/6) for {name}")
            return None

    except Exception as e:
        print(f"Error scraping {name}: {e}")
        return None

service = Service(r"D:\\UserFiles\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe")
# downloaded the chrome driver myself since it was bugging out
driver = webdriver.Chrome(service=service)

missing = df[df["str"].isna()].copy()
failures = []

for idx, row in missing.iterrows():
    name = row["name"]
    print(f"Scraping {name}")
    stats = safe_scrape(name, driver)
    if stats:
        for stat, val in stats.items():
            df.at[idx, stat] = val
    else:
        print(f"FAILED: {name}")
        failures.append(name)

driver.quit()
print("Failures:", failures)
df.to_csv("dnd_monsters_completed.csv", index=False)