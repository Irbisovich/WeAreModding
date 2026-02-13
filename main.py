# WeAreModding! by irbisovich, 2026
# main.py

import xml.etree.ElementTree as ET
from PIL import Image as PILImage
from axml.axml import AXMLPrinter
from axml.arsc import ARSCPrinter
from tkinter.ttk import Combobox
from tkinter import scrolledtext
from tkinter import messagebox
from PIL import ImageTk
from tkinter import *
import subprocess, os
import zipfile
import shutil
import glob

subprocess.run(f'cd {os.getcwd()}', shell=True)

def extract_apk_to_folder(appname, folder):
    subprocess.run(f'adb pull {subprocess.run(f'adb shell pm path {appname}'.split(' '), capture_output=True, text=True).stdout.replace('package:', '')}', shell=True)
    with zipfile.ZipFile('base.apk', 'r', zipfile.ZIP_DEFLATED) as apk:
        apk.extractall(folder)

    os.remove('base.apk')

def find_value_by_id(xml_string, target_id):
    """
    Ищет в XML (строке) элемент <public> с заданным id и возвращает атрибут name.
    target_id должен быть в формате '@7F0800BD' или '0x7f0800bd'.
    """
    # Приводим ID к нижнему регистру и убираем '@'
    target = target_id.replace('@', '0x').lower()
    root = ET.fromstring(xml_string)
    # Ищем все элементы с тегом 'public' (регистр важен)
    for elem in root.findall('.//public'):
        elem_id = elem.attrib.get('id', '').lower()
        if elem_id == target:
            return elem
    return None


def find_resource_files(extracted_dir, res_type, res_name):
    """
    Ищет файлы ресурса по типу и имени в распакованной APK папке.

    Args:
        extracted_dir (str): путь к корню распакованного APK (где есть папка res)
        res_type (str): тип ресурса, например 'drawable'
        res_name (str): имя ресурса, например 'ic_launcher'

    Returns:
        list: список путей к найденным файлам (может быть пустым)
    """
    # Сначала ищем в папках типа res/{res_type}* (например, drawable-hdpi, drawable-xhdpi)
    pattern = os.path.join(extracted_dir, 'res', f'{res_type}*', f'{res_name}.*')
    files = glob.glob(pattern)

    if files:
        return files

    # Если ничего не нашли, ищем рекурсивно во всех подпапках res
    fallback_pattern = os.path.join(extracted_dir, 'res', '**', f'{res_name}.*')
    files = glob.glob(fallback_pattern, recursive=True)
    return files

def check_apk(appname):
    step2.place_forget()

    if appname == 'Choose app from the list':
        pass

    else:
        try:
            shutil.rmtree('temp')

        finally:
            step2.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)
            extract_apk_to_folder(appname, 'temp')

            try:
                approot = ET.fromstring(AXMLPrinter(open('temp/AndroidManifest.xml', 'rb+').read()).get_xml().decode('utf-8'))
                resourcesroot = ARSCPrinter(open('temp/resources.arsc', 'rb+').read()).get_xml().decode('utf-8')

                appinfo = {key.replace('{http://schemas.android.com/apk/res/android}', ''): value for key, value in approot.find('application').attrib.items()}

                iconpath = find_resource_files('temp', find_value_by_id(resourcesroot, appinfo['icon']).attrib['type'], find_value_by_id(resourcesroot, appinfo['icon']).attrib['name'])[0]

                icon = PILImage.open(iconpath).resize((int(500 * 0.3), int(500 * 0.3)), PILImage.Resampling.LANCZOS)
                icontk = ImageTk.PhotoImage(icon)
                iconlbl = Label(step2, image=icontk)
                iconlbl.image = icontk
                iconlbl.place(relx=0, rely=0, relwidth=0.3, relheight=0.3)
                Label(step2, text=appinfo['name']).place(relx=0.3, rely=0, relwidth=0.7, relheight=0.3)

                appinfolbl = scrolledtext.ScrolledText(step2)
                appinfolbl.insert(INSERT, '\n'.join([f'{key.upper()}: {value}' for key, value in appinfo.items()]))
                appinfolbl.place(relx=0, rely=0.31, relwidth=1, relheight=0.49)
            except Exception as e:
                Label(step2, text=f'App info can\'t be viewed due to exception.\n\n{e.__class__}: {e}').place(relx=0, rely=0, relwidth=1, relheight=0.8)

            finally:
                Button(step2, text='Modify').place(relx=0, rely=0.8, relwidth=1, relheight=0.1)
                Button(step2, text='Build').place(relx=0, rely=0.9, relwidth=1, relheight=0.1)
window = Tk()
window.title('WeAreModding!')
window.geometry('500x500')
window.resizable(False, False)

apps = [option.replace('package:', '') for option in subprocess.run(f'adb shell pm list packages -3'.split(' '), capture_output=True, text=True).stdout.split('\n')]
apps.sort()
apps.remove('')

if len(apps) == 0:
    messagebox.showwarning('Connect your device', 'Apps not found.\nPlease, enable ADB (USB Debugging) or check connection of your device and computer.')

Label(window, text='Choose app to modify').place(relx=0, rely=0, relwidth=1, relheight=0.05)
chooseappcombo = Combobox(window, values=[f'Choose app from the list'] + apps)
chooseappcombo.current(0)
chooseappcombo.place(relx=0, rely=0.05, relwidth=1, relheight=0.05)
chooseappcombo.bind("<<ComboboxSelected>>", lambda x=None: check_apk(chooseappcombo.get()))

step2 = Frame(window)
Label(step2, text='idk lol').pack()

window.mainloop()
