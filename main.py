import win32gui,win32process
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import psutil
import time

def enum_window_titles():
    def callback(handle, data):
        if win32gui.IsWindowVisible(handle) and len(win32gui.GetWindowText(handle)) > 0:
            hwnd.append(handle)
            titles.append(win32gui.GetWindowText(handle))
    hwnd =[]
    titles = []
    win32gui.EnumWindows(callback, None)
    return hwnd,titles

def obterPidProcesso(nomeProcesso):
    listapids =[]
    for processo in psutil.process_iter():
        if processo.name() == nomeProcesso:
            pid = processo.pid
            listapids.append(pid)
    return listapids

def obterNomeJanelaSpotify(pid,hwnd,titles):
    index = 0
    for handle in hwnd:
        threadid, windowPid = win32process.GetWindowThreadProcessId(handle)
        if (windowPid in pid and titles[index]!= 'Spotify Premium'):
            return titles[index]
        index = index + 1
    return None

def callWhtsapp(navegador,windowName):
    navegador.get('https://web.whatsapp.com/')
    time.sleep(15)
    foto = navegador.find_element_by_xpath('//*[@id="side"]/header/div[1]/div/img')
    foto.click()
    time.sleep(1)
    editar = navegador.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[1]/span/div/div/div/div[4]/div[2]/div[1]/span[2]/div')
    editar.click()
    time.sleep(0.5)
    campoTexto = navegador.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[1]/span/div/div/div/div[4]/div[2]/div[1]/div/div[2]')
    campoTexto.clear()
    campoTexto.send_keys(windowName)
    campoTexto.send_keys(Keys.ENTER)
    time.sleep(0.5)
    navegador.close()

def inicializarChromeDriver():
    options = webdriver.ChromeOptions()
    options.add_argument(r"user-data-dir=C:\Users\Danilo\PycharmProjects\spotifyWindow\temp")
    navegador = webdriver.Chrome("C:/Users/Danilo/PycharmProjects/spotifyWindow/chromedriver.exe", chrome_options=options)
    return navegador

nomeProcesso = "Spotify.exe"
nomeAntigo = ''
while True:
    try:
        hwnd,titles = enum_window_titles()
        pid = obterPidProcesso(nomeProcesso)
        nomeAtual = obterNomeJanelaSpotify(pid,hwnd,titles)
        if (nomeAntigo != nomeAtual and nomeAtual != None):
            print (nomeAtual)
            navegador = inicializarChromeDriver()
            callWhtsapp(navegador,nomeAtual)
            nomeAntigo = nomeAtual
    except:
        print ("Não foi possível realizar a troca no momento")
        navegador.close()
    time.sleep(10)

