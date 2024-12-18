from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import os
import time

# Masukkan URL E-Commerce
url = input("Masukkan url toko : ")

if url:
    # Konfigurasi Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    data = []

    # Scrape Ulasan Menjadi 3 halaman
    for i in range(0, 3):
        soup = BeautifulSoup(driver.page_source, "html.parser")
        containers = soup.findAll('article', attrs={'class': 'css-ccpe8t'})

        for container in containers:
            try:
                # Ekstrak Ulasan
                review = container.find('span', attrs={'data-testid': 'lblItemUlasan'}).text
                data.append((review))
            except AttributeError:
                continue

        print(f"Jumlah data terkumpul sejauh ini: {len(data)}")

        # Navigasi ke Halaman Selanjutnya
        time.sleep(2)
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label^='Laman berikutnya']")
            next_button.click()
            time.sleep(3)
        except:
            print("Tidak ada halaman berikutnya.")
            break

    driver.quit()

    # Simpan dan Ekstrak ke CSV
    if data:
        output_path = os.path.expanduser("~/Desktop/Tokopedia_Review_Store_Planet_Hobby_Indonesia.csv")
        df = pd.DataFrame(data, columns=["Ulasan"])
        df.to_csv(output_path, index=False)
        print(f"Data berhasil disimpan di {output_path}")
    else:
        print("Tidak ada data yang berhasil dikumpulkan.")
