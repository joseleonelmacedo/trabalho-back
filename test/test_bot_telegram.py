from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Caminho para o driver do Chrome usando webdriver_manager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

def test_login_telegram():
    driver.get("https://web.telegram.org/")
    
    # Esperar o login manual (coloque seu número e código)
    input("Press Enter after logging in...")

def test_enviar_mensagem_telegram(mensagem):
    # Encontre o campo de mensagem e envie o texto
    campo_mensagem = driver.find_element_by_xpath('//div[@contenteditable="true"]')
    campo_mensagem.send_keys(mensagem)
    campo_mensagem.send_keys(Keys.RETURN)

def test_testar_conversa():
    # Enviar mensagem "hi" para o Telegram Web
    test_enviar_mensagem_telegram("hi")
    
    # Esperar um pouco para que a resposta chegue
    time.sleep(2)

    # Verificar se a resposta correta aparece no chat
    mensagens = driver.find_elements_by_xpath('//div[@class="message"]')
    ultima_mensagem = mensagens[-1].text
    assert "Hello, I am ZenBot!" in ultima_mensagem

# Executar os testes
test_login_telegram()
test_testar_conversa()
