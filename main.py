from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import subprocess
from selenium.webdriver.common.keys import Keys

# define user-agent (you can get it from the user)
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
chrome_options = Options()
chrome_options.add_argument(USER_AGENT)

# Initialize Chromedriver
driver = webdriver.Chrome()
driver.maximize_window()


def save_data(
    covered_distance, price, color, engin_volume, acceleration, img_url, car_model
):
    # save data to a file
    subprocess.run(["wget", "--no-proxy", "-P", "data/images", img_url])

    data = ""

    if covered_distance:
        data += covered_distance + "$"
    if price:
        data += price + "$"
    if color:
        data += color + "$"
    if engin_volume:
        data += engin_volume + "$"
    if acceleration:
        data += acceleration + "$"
    if img_url:
        data += img_url

    with open(f"data/data/{car_model}.txt", "a") as f:
        f.write(data + "\n")

    print("saved data")


def scroll_down():
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")


def crawl_data(car_model):
    for i in range(2, 102):
        covered_distance = False
        price = False
        color = False
        engin_volume = False
        acceleration = False
        img_url = False
        element = driver.find_element(
            By.XPATH,
            f'//*[@id="__layout"]/div/div[1]/section/div[2]/div/div[{i}]',
        )
        element.click()

        # exit()

        # static part
        try:
            covered_distance = driver.find_element(
                By.XPATH,
                '//*[@id="__layout"]/div/div[1]/section/div[3]/div[2]/div[2]/div/div[2]/div[4]/div[1]/span',
            ).text
            print(covered_distance)
        except:
            print("err on covered_distance ")
        try:
            price = driver.find_element(
                By.XPATH,
                '//*[@id="__layout"]/div/div[1]/section/div[3]/div[2]/div[2]/div/div[2]/div[1]/div[2]/div[2]/span/span',
            ).text
            print(price)
        except:
            print("err on price")

        try:
            color = driver.find_element(
                By.XPATH,
                '//*[@id="__layout"]/div/div[1]/section/div[3]/div[2]/div[2]/div/div[2]/div[4]/div[4]/span',
            ).text
            print(color)
        except:
            print("err on color")

        try:
            engin_volume = driver.find_element(
                By.XPATH,
                '//*[@id="__layout"]/div/div[1]/section/div[3]/div[2]/div[2]/div/div[3]/div[3]/div/div[2]/div[1]/span[2]',
            ).text
            print(engin_volume)
        except:
            print("err on engin volume")

        try:
            acceleration = driver.find_element(
                By.XPATH,
                '//*[@id="__layout"]/div/div[1]/section/div[3]/div[2]/div[2]/div/div[3]/div[3]/div/div[2]/div[3]/span[2]',
            ).text
            print(acceleration)
        except:
            print("err acceleration")
        try:
            img_url = driver.find_element(
                By.XPATH, '//*[@id="main-slider-clone03"]/div/img'
            ).get_attribute("src")
            print(img_url)
        except:
            print("err on image")

        try:
            save_data(
                covered_distance,
                price,
                color,
                engin_volume,
                acceleration,
                img_url,
                car_model,
            )
            element = driver.find_element(
                By.XPATH,
                f'//*[@id="__layout"]/div/div[1]/section/div[3]/div[2]/div[1]/div/div',
            )
            element.click()
            scroll_down()
        except:
            print("err on saving data")


def send_request(urls):
    for url in urls:
        # Send requests to each URL
        driver.get(url)

        # webpage gets loaded
        sleep(5)

        # get car model from url for saving data
        parts = url.split("/")
        last_part = parts[-1]
        # Extract the keyword by removing the prefix "https://bama.ir/car/"
        car_model = str(last_part.replace("https://bama.ir/car/", ""))

        # beacuse of err on makeing directory
        car_model_update = car_model.replace("-", "")
        print(car_model_update)
        crawl_data(car_model_update)


def read_links():
    # Read URLs from a text file
    with open("urls.txt", "r") as file:
        urls = file.readlines()

    # Remove whitespace and newlines from URLs
    urls = [url.strip() for url in urls]
    return urls


def main():
    urls = read_links()
    send_request(urls)


if __name__ == "__main__":
    main()
