from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class P2:
    def __init__(self, urlLogin):
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.urlLogin = urlLogin

    def ingresarDatosYEsperar(self, campo, datos, tiempoEspera=4):
        campo.clear()
        time.sleep(tiempoEspera)
        campo.send_keys(datos)

    def imprimir(self, msj):
        print(msj)

    def iniciarSesion(self, nombreUsuario, contrasena):
        while True:
            if nombreUsuario != "prueba" or contrasena != "programacion":
                nombreUsuario = input("Las credenciales son incorrectas. Ingrese el nombre de usuario del router: ")
                contrasena = input("Ingrese la contraseña del router: ")
            else:
                break

        self.driver.get(self.urlLogin)
        try:
            campoNombreUsuario = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, 'UserName'))
            )
            campoContrasena = self.driver.find_element(By.ID, 'Password')
            self.ingresarDatosYEsperar(campoNombreUsuario, nombreUsuario)
            self.ingresarDatosYEsperar(campoContrasena, contrasena)
            botonIniciarSesion = self.driver.find_element(By.CSS_SELECTOR, "input[value='Apply']")
            time.sleep(4)
            botonIniciarSesion.click()
            self.imprimir("Inicio de sesión exitoso")
        except Exception as e:
            self.imprimir(f"Ocurrió un error durante el inicio de sesión: {e}")
            return False
        return True

    def validarContrasenaWifi(self, contrasena):
        if not (8 <= len(contrasena) <= 63):
            raise ValueError("La contraseña debe tener entre 8 y 63 caracteres.")
        if not all(c.isascii() for c in contrasena):
            raise ValueError("La contraseña debe contener solo caracteres ASCII.")

    def configurarWifi(self, nuevoSsid, nuevaContrasenaWifi):
        while True:
            try:
                self.validarContrasenaWifi(nuevaContrasenaWifi)
                break
            except ValueError as e:
                self.imprimir(e)
                nuevaContrasenaWifi = input("Ingrese una nueva contraseña válida para la red Wi-Fi: ")

        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.ID, 'WirelessNetworkName'))
            )
            campoSsid = self.driver.find_element(By.ID, 'WirelessNetworkName')
            self.ingresarDatosYEsperar(campoSsid, nuevoSsid)
            campoContrasenaWifi = self.driver.find_element(By.ID, 'WifiPassword')
            self.ingresarDatosYEsperar(campoContrasenaWifi, nuevaContrasenaWifi)
            botonAplicar = self.driver.find_element(By.CSS_SELECTOR, "input[value='Aplicar']")
            time.sleep(4)
            botonAplicar.click()
            self.imprimir("Configuración Wi-Fi aplicada con éxito")
            time.sleep(10)
        except Exception as e:
            self.imprimir(f"Ocurrió un error durante la configuración de Wi-Fi: {e}")

    def configurarCanalWifi(self):
        try:
            self.driver.execute_script("window.location.href='router.html?wifi_basic'")
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.ID, 'Channel'))
            )

            while True:
                try:
                    canal = int(input("Ingrese el canal de transmisión (1-13): "))
                    if 1 <= canal <= 13:
                        break
                    else:
                        raise ValueError("El canal debe estar entre 1 y 13.")
                except ValueError as e:
                    self.imprimir(e)

            campoCanal = self.driver.find_element(By.ID, 'Channel')
            opcionesCanal = campoCanal.find_elements(By.TAG_NAME, 'option')
            for opcion in opcionesCanal:
                if opcion.get_attribute('value') == str(canal):
                    opcion.click()
                    break

            botonAplicar = self.driver.find_element(By.CSS_SELECTOR, "input[value='Aplicar']")
            time.sleep(4)
            botonAplicar.click()
            self.imprimir("Configuración del canal Wi-Fi aplicada con éxito")
        except Exception as e:
            self.imprimir(f"Ocurrió un error durante la configuración del canal Wi-Fi: {e}")

    def configurarLan(self, nuevaIp, nuevaMascaraSubred):
        try:
            self.driver.execute_script("window.location.href='router.html?lan_settings'")
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.ID, 'IPAddress'))
            )
            campoIpLan = self.driver.find_element(By.ID, 'IPAddress')
            self.ingresarDatosYEsperar(campoIpLan, nuevaIp)
            campoMascaraSubredLan = self.driver.find_element(By.ID, 'SubnetMask')
            self.ingresarDatosYEsperar(campoMascaraSubredLan, nuevaMascaraSubred)
            botonAplicar = self.driver.find_element(By.CSS_SELECTOR, "input[value='Aplicar']")
            time.sleep(4)
            botonAplicar.click()
            self.imprimir("Configuración de LAN aplicada con éxito")
            time.sleep(10)
        except Exception as e:
            self.imprimir(f"Ocurrió un error durante la configuración de LAN: {e}")

    def configurarWanEstatica(self, nuevaGateway):
        try:
            self.driver.execute_script("window.location.href='router.html?wan_static'")
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.ID, 'EnableStatic'))
            )
            checkboxHabilitarEstatica = self.driver.find_element(By.ID, 'EnableStatic')
            if not checkboxHabilitarEstatica.is_selected():
                checkboxHabilitarEstatica.click()
            time.sleep(4)
            campoGateway = self.driver.find_element(By.ID, 'GatewayAddress')
            self.ingresarDatosYEsperar(campoGateway, nuevaGateway)
            botonAplicar = self.driver.find_element(By.CSS_SELECTOR, "input[value='Aplicar']")
            time.sleep(4)
            botonAplicar.click()
            self.imprimir("Configuración WAN estática aplicada con éxito")
        except Exception as e:
            self.imprimir(f"Ocurrió un error durante la configuración WAN estática: {e}")

urlLogin = "http://192.168.0.1/router.html"
p2 = P2(urlLogin)

try:
    while True:
        try:
            nombreUsuario = input("Ingrese el nombre de usuario del router: ")
            contrasena = input("Ingrese la contraseña del router: ")

            if p2.iniciarSesion(nombreUsuario, contrasena):
                break
        except ValueError as e:
            p2.imprimir(e)

    nuevoSsid = input("Ingrese el nuevo nombre de la red (SSID): ")
    nuevaContrasenaWifi = input("Ingrese la nueva contraseña de la red Wi-Fi: ")
    p2.configurarWifi(nuevoSsid, nuevaContrasenaWifi)

    p2.configurarCanalWifi()

    nuevaIp = input("Ingrese la nueva dirección IP del router: ")
    nuevaMascaraSubred = input("Ingrese la nueva máscara de subred del router: ")
    p2.configurarLan(nuevaIp, nuevaMascaraSubred)

    nuevaGateway = input("Ingrese la nueva dirección de gateway: ")
    p2.configurarWanEstatica(nuevaGateway)
except ValueError as e:
    p2.imprimir(e)


