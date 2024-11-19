from selenium import webdriver
from colorama import init, Fore
import threading, sys, time

def loading_animation():
    animation = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    i = 0
    while loading:
       sys.stdout.write("\r" + Fore.YELLOW + f"Loading {animation[i % len(animation)]} " + Fore.RESET)
       sys.stdout.flush()
       time.sleep(0.1)
       i += 1

def get_driver(coin):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('disable-infobars')
    options.add_argument('start-maximized')
    options.add_argument('disable-dev-shm-usage')
    options.add_argument('no-sandbox')
    options.add_experimental_option('excludeSwitches', ["enable-automation"])
    options.add_argument("disable-blink-features=AutomationControlled")
    
    driver = webdriver.Chrome(options=options)
    driver.get(f"https://coinmarketcap.com/currencies/{coin}/")
    return driver

def get_coinmarket_price(coin):
    global loading
    loading = True
    animation_thread = threading.Thread(target=loading_animation)
    animation_thread.start()

    try:
        driver = get_driver(coin)
        element = driver.find_element("xpath", "//*[@id='section-coin-overview']/div[2]/span")
        result = element.text
    except:
        result = None
    finally:
        loading = False
        animation_thread.join()
        driver.quit()
        sys.stdout.write("\r" + " " * 20 + "\r")
       
    return result

init()
print(Fore.BLUE + "Hello to crypto_scraper!")
print(Fore.BLUE + "Please enter the full name of the coin (e.g. bitcoin, ethereum)")
print(Fore.BLUE + "Write exit to leave the program" + Fore.RESET)    

while 42:
    coin = input("Enter cryptocurrency name: ")
    if coin.lower() == "exit":
       print(Fore.BLUE + "Goodbye!" + Fore.RESET)
       break
    current_price = get_coinmarket_price(coin)
    if current_price:
        print(Fore.GREEN + f"Current {coin.capitalize()} Price: " + current_price + Fore.RESET)
    else:
        print(Fore.RED + f"Error: Cryptocurrency '{coin}' not found. Please use full name." + Fore.RESET)

