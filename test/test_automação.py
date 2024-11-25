import pytest
import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestTelegramBot:
    @pytest.fixture(scope="class", autouse=True)
    def setup_teardown(self):
        """Setup do Selenium WebDriver e teardown após os testes."""
        self.driver = webdriver.Edge()  # Substitua por webdriver.Chrome() se necessário.
        self.driver.get('https://web.telegram.org/')
        print("Por favor, faça login manualmente no Telegram Web.")
        WebDriverWait(self.driver, 300).until(
            EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Search"]'))
        )
        print("Login detectado. Iniciando testes...")
        yield
        self.driver.quit()

    @pytest.mark.asyncio
    async def test_opcao1_gdp(self):
        """Testa o comando /opcao1 para verificar o PIB."""
        chat_name = "@zenEconomi_bot"
        search_box = self.driver.find_element(By.XPATH, '//input[@placeholder="Search"]')
        search_box.clear()
        search_box.send_keys(chat_name)
        await asyncio.sleep(2)  # Espera carregar os resultados
        search_box.send_keys(Keys.ENTER)

        # Testa o comando /opcao1
        await self.send_message("/opcao1")
        await asyncio.sleep(1)
        self.verify_response_contains("Enter the year you want to check the GDP of Brazil:")

        # Envia ano para verificar PIB
        await self.send_message("2020")
        await asyncio.sleep(3)
        self.verify_response_contains("The GDP of Brazil in 2020 was")

    @pytest.mark.asyncio
    async def test_opcao2_inflation(self):
        """Testa o comando /opcao2 para verificar a inflação."""
        await self.send_message("/opcao2")
        await asyncio.sleep(1)
        self.verify_response_contains("Enter the year you want to check the inflation rate of Brazil:")

        # Envia ano para verificar inflação
        await self.send_message("2020")
        await asyncio.sleep(3)
        self.verify_response_contains("The inflation in Brazil in 2020 was")

    @pytest.mark.asyncio
    async def test_opcao3_unemployment(self):
        """Testa o comando /opcao3 para verificar o desemprego."""
        await self.send_message("/opcao3")
        await asyncio.sleep(1)
        self.verify_response_contains("Enter the year you want to check the unemployment rate of Brazil:")

        # Envia ano para verificar taxa de desemprego
        await self.send_message("2020")
        await asyncio.sleep(3)
        self.verify_response_contains("The unemployment rate in Brazil in 2020 was")

    @pytest.mark.asyncio
    async def test_opcao4_exit(self):
        """Testa o comando /opcao4 para sair."""
        await self.send_message("/opcao4")
        await asyncio.sleep(1)
        self.verify_response_contains("see you in one day supertropical")

    # Funções auxiliares
    async def send_message(self, message):
        """Envia uma mensagem para o bot."""
        text_box = self.driver.find_element(By.XPATH, '//div[@contenteditable="true"]')
        text_box.clear()
        text_box.send_keys(message)
        text_box.send_keys(Keys.ENTER)

    def verify_response_contains(self, expected_text):
        """Verifica se a última mensagem no chat contém o texto esperado."""
        messages = self.driver.find_elements(By.XPATH, '//div[contains(@class, "message")]')
        assert any(expected_text in msg.text for msg in messages), f"Expected text '{expected_text}' not found in messages."
