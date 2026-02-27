import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

df = pd.read_csv("dnd_monsters_completed.csv")

def check_legendary(name, driver):
    url = f"https://www.aidedd.org/dnd/monstres.php?vo={name}"
    try:
        driver.get(url)
        time.sleep(3)
        
        rub_divs = driver.find_elements(By.CLASS_NAME, "rub")
        for div in rub_divs:
            if "legendary actions" in div.text.lower():
                return True
        return False
    
    except Exception as e:
        print(f"Error checking {name}: {e}")
        return None  # None = uncertain 
        # True = confirmed legendary,   False = confirmed not legendary

service = Service(r"D:\\UserFiles\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe")
driver = webdriver.Chrome(service=service)

for idx, row in df.iterrows():
    name = row["name"]
    print(f"Checking {name}")
    result = check_legendary(name, driver)
    df.at[idx, "legendary"] = result

driver.quit()
df.to_csv("dnd_monsters_completed.csv", index=False)
print("Done!")