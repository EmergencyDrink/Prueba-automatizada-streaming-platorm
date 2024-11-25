from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from jinja2 import Environment, FileSystemLoader
import time

# Configuración del driver
driver = webdriver.Chrome()
driver.maximize_window()

if not os.path.exists('screenshots'):
    os.makedirs('screenshots')

# Diccionario para registrar el estado de las pruebas
resultadosReportes = {
    1: False,  # Inicio de Sesión
    2: False,  # Selección de Perfil
    3: False,  # Escoger Categoría
    4: False,  # Reproducción de Contenido
    5: False   # Cambio al Perfil de Niños
}

# Definición de funciones para las pruebas
def iniciar_sesion():
    try:
        driver.get("https://www.netflix.com/login")
        driver.implicitly_wait(15)
        driver.save_screenshot("screenshots/Captura_iniciar_sesion.png")

        username_field = driver.find_element(By.NAME, "userLoginId")
        username_field.send_keys("TuPerfil")
        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys("TUContraseña")
        password_field.submit()
        driver.save_screenshot("screenshots/Captura_iniciar_sesion_Datos.png")

        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "profile-icon")))
        driver.save_screenshot("screenshots/Captura_perfiles.png")
        resultadosReportes[1] = True  # Actualizar estado como exitoso
    except Exception as e:
        raise RuntimeError(f"Error en iniciar sesión: {e}")

def elegir_perfil():
    try:
        primer_perfil = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "profile-name")))
        primer_perfil.click()
        resultadosReportes[2] = True  # Actualizar estado como exitoso
    except Exception as e:
        raise RuntimeError(f"Error al seleccionar el perfil: {e}")

def escoger_categoria():
    try:
        time.sleep(5)
        driver.save_screenshot("screenshots/Captura_pantalla_principal.png")

        link_series = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/browse/genre/83']")))
        link_series.click()

        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "slider-item")))
        driver.save_screenshot("screenshots/Captura_navegar_categoria.png")
        resultadosReportes[3] = True  # Actualizar estado como exitoso
    except Exception as e:
        raise RuntimeError(f"Error al escoger categoría: {e}")

def reproducir_contenido():
    try:
        WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CLASS_NAME, "slider-item")))
        preview_elements = driver.find_elements(By.CLASS_NAME, "slider-item")
        preview_elements[0].click()
        driver.save_screenshot("screenshots/Captura_preview_serie.png")
        time.sleep(10)

        try:
            play_button = driver.find_element(By.CLASS_NAME, "primary-button")
            play_button.click()
        except:
            pass

        time.sleep(10)
        driver.save_screenshot("screenshots/Captura_reproduciendo_serie.png")
        driver.get("https://www.netflix.com/browse")
        resultadosReportes[4] = True  # Actualizar estado como exitoso
    except Exception as e:
        raise RuntimeError(f"Error al reproducir contenido: {e}")

def cambiar_perfil_niños():
    try:
        boton_niños = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='nav-element show-kids']/a")))
        boton_niños.click()
        driver.save_screenshot("screenshots/Captura_perfil_niños.png")
        resultadosReportes[5] = True  # Actualizar estado como exitoso
    except Exception as e:
        raise RuntimeError(f"Error al cambiar al perfil de niños: {e}")

# Ejecución principal
try:
    print("Ejecutando prueba 1: Iniciar sesión")
    iniciar_sesion()
    print("Prueba 1: Completada correctamente.")

    print("Ejecutando prueba 2: Seleccionar perfil")
    elegir_perfil()
    print("Prueba 2: Completada correctamente.")

    print("Ejecutando prueba 3: Escoger categoría")
    escoger_categoria()
    print("Prueba 3: Completada correctamente.")

    print("Ejecutando prueba 4: Reproducir contenido")
    reproducir_contenido()
    print("Prueba 4: Completada correctamente.")

    print("Ejecutando prueba 5: Cambiar al perfil de niños")
    cambiar_perfil_niños()
    print("Prueba 5: Completada correctamente.")

except RuntimeError as e:
    print(e)
    driver.quit()
    # Generar reporte hasta el paso completado y salir
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template("Reportes/Informe-plantilla.html")
    html_content = template.render(resultadosReportes=resultadosReportes)

    with open("Reportes/Informe.html", "w") as file:
        file.write(html_content)

    exit(1)  # Salir del programa con error

# Generación del reporte final
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template("Reportes/Informe-plantilla.html")
html_content = template.render(resultadosReportes=resultadosReportes)

with open("Reportes/Informe.html", "w") as file:
    file.write(html_content)

driver.quit()
