#Import necessary librarieas
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from tkinter import *
import numpy as np
import time
import random
from datetime import datetime


def Marathon(web_drv,nmb_for_search, nmb_for_insert):

    web_drv.get(F"https://www.betmarathon.com/en")
    web_drv.maximize_window()
    web_drv.implicitly_wait(10)

    while True:
        try:
            web_drv.get(F"https://www.betmarathon.com/su/live/popular")
            sports = web_drv.find_elements_by_xpath(
                "/html/body//div[@id = 'container_EVENTS']//div[contains(@class, 'collapsed')]")
            links = list()
            for sport in sports:
                ssport = sport.get_attribute("data-category-treeid")
                links.append(ssport)
            llink = "https://www.betmarathon.com/su/live/popular?ecids="
            for link in links:
                llink += str(link) + ","
            web_drv.get(llink)
            web_drv.implicitly_wait(10)
            footer = web_drv.find_element_by_id("footer")
            web_drv.execute_script("return arguments[0].scrollIntoView();", footer)
            prices = web_drv.find_elements_by_xpath("//td[contains(@class, 'price')]/span[contains(@class, 'selection-link')]")
            for price in prices:
                pprice = float(price.get_attribute("data-selection-price"))
                print(pprice)
                for stk in nmb_for_search:
                    if round(stk, 4) == round(pprice, 4):
                        web_drv.execute_script("return arguments[0].scrollIntoView();", price)
                        print("FOUND")
                        # parent = price.find_element_by_xpath("..")
                        web_drv.execute_script("return arguments[0].click();", price)
                        time.sleep(4)
                        inputs = web_drv.find_element_by_xpath("html/body//td[contains(@class, 'stake')]/input[@name='stake']")
                        print("Stake value: " + str(nmb_for_insert))
                        web_drv.execute_script("return arguments[0].click();", inputs)
                        time.sleep(1)
                        inputs.send_keys(nmb_for_insert)
                        rules = web_drv.find_element_by_id("betslip_apply_choices")
                        if rules:
                            web_drv.execute_script("return arguments[0].click();", rules)
                        print("PLACING BET")
                        bet = web_drv.find_element_by_xpath("html/body//td[contains(@class, 'panel-bet-cell')]/span[@id='betslip_placebet_btn_id']")
                        web_drv.execute_script("return arguments[0].click();", bet)
                        res = "Bet placed. Waiting."
                        bet_pause = random.randint(5, 15);
                        print("Paused for " + str(bet_pause) + "s.")
                        time.sleep(bet_pause)
                        return res
            print("NOTHING FOUND, REFRESHING")

        except NoSuchElementException:
            print("NoSuchElementException")
            running = False

        except Exception as e:
            print("ERROR")
            print(str(e))

    # print("RESULTS \n")
    # print("Total bets: " + str(bets))
    # print("Needed bets: " + str(golden_bets))
    # stats = [bets, golden_bets]
    # return stats

def controller(web_drv, nmb_for_search, nmb_for_insert, min_balance):
    while True:
        try:
            web_drv.get(F"https://www.betmarathon.com/su/myaccount/myaccount.htm")
            web_drv.implicitly_wait(7)
            balance = web_drv.find_element_by_xpath("//div[@id='my_account_menu_header']//table[@class='block-accout-info']" 
                                                    "//td[@class='value']" 
                                                    "//span[@data-punter-balance-type='main']")
            bbalance = float(balance.get_attribute("data-punter-balance-value"))
            print("Balance: " + str(bbalance))
            if bbalance >= min_balance:
                print("Balance is OK. Looking for bets.")
                print(str(datetime.today()))
                msg = Marathon(web_drv, nmb_for_search, nmb_for_insert)
                print(msg)
            else:
                print("Balance is too low. Waiting.")
                print(str(datetime.today()))
                t_t_w = random.randint(40, 320)
                print("Pausing for: " + str(t_t_w) + "s.")
                time.sleep(t_t_w)

        except NoSuchElementException:
            print("NoSuchElementException")

        except Exception as e:
            print("ERROR")
            print(str(e))


def bot_GUI(web_drv):
    master = Tk()
    master.title("Marathon Bot v. 1.0")
    # Подписи

    lable_1 = Label(master,text = "Минимальный К для поиска").grid(row=0, sticky=E)
    lable_2 = Label(master,text = "Максимальный К для поиска").grid(row=1, sticky=E)
    # lable_3 = Label(master,text = "Выберите режим").grid(row=4, sticky=E)
    lable_4 = Label(master, text = "Размер ставки").grid(row=3, sticky=E)
    lable_5 = Label(master, text = "Минимальный баланс").grid(row=2, sticky=E)

    # Ввод

    # Режим работы 1 - just search, 2 - search and click, 3 - search, click and insert, 4 - search, click, insert and place a bet
    # OPTIONS = [1, 2, 3, 4]
    # mode_var = IntVar(master)
    # mode_var.set(OPTIONS[0])  # default value
    # mode_win = OptionMenu(master, mode_var, *OPTIONS)
    # mode_win.grid(row=4, column=1)

    # Минимальный и максимальный К для поиска
    min_var = Entry(master)
    min_var.grid(row=0, column=1)

    max_var = Entry(master)
    max_var.grid(row=1, column=1)

    min_bal = Entry(master)
    min_bal.grid(row=2, column=1)


    # Размер ставки
    stk_var = Entry(master)
    stk_var.grid(row=3, column=1)



    def bt_handler(wb_drv):
        min_v = min_var.get()
        max_v = max_var.get()
        min_b = min_bal.get()
        s_v = stk_var.get()
        stk_target = np.arange(float(min_v), float(max_v), float(0.001))
        print("LIST GENERATED \n")
        print(stk_target)
        controller(wb_drv, stk_target, s_v, float(min_b))
        # msg = "Всего ставок на сайте: " + str(stat[0]) + "\n " + "Подходящих ставок найдено: " + str(stat[1])
        # messagebox.showinfo("Статистика", msg)

    # Кнопочки
    start = Button(master, text='Запуск', command=lambda: bt_handler(web_drv)).grid(row=5, column=0, sticky=E, pady=4)
    q_btn = Button(master, text='Выход', command=master.quit).grid(row=5, column=1, sticky=E, pady=4)


    # Упаковываем
    master.mainloop()





def main():
    options = webdriver.ChromeOptions()
    options.add_argument("user-data-dir=C:/Path/To/Chrome/Profile")
    chrome_path = "/path/to/chromedriver.exe"
    d = webdriver.Chrome(chrome_path, chrome_options=options)
    d.get(F"https://www.betmarathon.com/en")
    d.implicitly_wait(5)
    # На будущеее для геко драйверa System.setProperty("webdriver.gecko.driver","D:\marathonbot")
    # /html/body//div[contains(@class, 'prematch-sport-sub-menu-header')]//a[@class='label']

    bot_GUI(d)
    # statss = Marathon(d, stk_target, NUMBER_FOR_INSERT, 1)
    # print(statss)


if __name__ == '__main__':
    main()






























