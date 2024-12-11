from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import time

def setup_browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    return driver

def test_adicionar_investimento():
    driver = setup_browser()
    try:
        # Acessa a aplicação Streamlit
        driver.get("http://localhost:8501")
        
        # Captura o estado inicial da página
        driver.save_screenshot("screenshot_initial.png")

        # Aguarda manualmente antes de procurar o elemento
        time.sleep(10)

        # Aguarda até que o campo esteja presente e visível
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label='Nome da Nova Carteira']"))
        )

        # Captura o estado da página antes de interagir
        driver.save_screenshot("screenshot_before_interaction.png")

        # Interage com o campo de entrada
        driver.find_element(By.CSS_SELECTOR, "[aria-label='Nome da Nova Carteira']").send_keys("Minha Carteira")
    finally:
        driver.quit()
