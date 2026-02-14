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
from tkinter import ttk
from tkinter import *
import subprocess, os
import zipfile
import shutil
import glob

subprocess.run(f'cd {os.getcwd()}', shell=True)

class FileManager(Frame):
    def __init__(self, parent, path):
        Frame.__init__(self, parent)
        self.path = path

        self.pathlabel = Label(self, text=self.path)
        self.elements = Listbox(self)
        self.elementsscroll = ttk.Scrollbar(self, orient="vertical", command=self.elements.yview)

        self.pathlabel.place(relx=0, rely=0, relwidth=1, relheight=0.05)
        self.elements.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)
        self.elementsscroll.pack(side=RIGHT, fill=Y)

        self.elements.bind("<<ListboxSelect>>", self.checknupdate)
        self.elements["yscrollcommand"] = self.elementsscroll.set

        self.updatepath(path)

    def checknupdate(self, _):
        if not self.elements.get(0, END)[self.elements.curselection()[0]] == ' ↵ ..':
            newpath = f'{self.path}/{self.elements.get(0, END)[self.elements.curselection()[0]][2:]}'

            if os.path.isdir(newpath):
                self.updatepath(newpath)

            else:
                subprocess.run(f'xdg-open {newpath}', shell=True)

        else:
            newpath = '/'.join(self.path.split('/')[0:-1])

            self.updatepath(newpath)

    def updatepath(self, path):
        self.path = path

        cdcontains = os.listdir('/' if path.strip() == '' else path)
        cdcontains.sort()

        self.pathlabel.configure(text='/' if self.path.strip() == '' else self.path)
        self.elements.configure(listvariable=Variable(value=[' ↵ ..'] + [f'{'📂' if os.path.isdir(f'{self.path}/{entry}') else '📄'} {entry}' for entry in cdcontains]))

class InstallWizard(Toplevel):
    def __init__(self, parent, appname):
        Toplevel.__init__(self, parent)

        self.geometry('500x500')
        self.resizable(False, False)
        self.title('WeAreModding! build wizard')

        self.steps = ttk.Notebook(self)

        self.step1 = Frame(self.steps)
        Label(self.step1, text='WeAreModding! build wizard', font='Arial 17').place(x=0, y=0, relwidth=1, relheight=0.2)
        Label(self.step1, text='Click \'Next\' to go proceed or click \'Close\' to stop this operation.\nThis operation will build application and install it on your device via ADB.', justify="left").place(x=0, rely=0.2, relwidth=1, relheight=0.8)
        self.step2 = Frame(self.steps)
        Label(self.step2, text='Step 1: generating keystore', font='Arial 17').place(x=0, y=0, relwidth=1, relheight=0.1)
        self.cnentry = Entry(self.step2)
        self.ouentry = Entry(self.step2)
        self.oentry = Entry(self.step2)
        self.lentry = Entry(self.step2)
        self.sentry = Entry(self.step2)
        self.centry = Entry(self.step2)
        self.passentry = Entry(self.step2)
        self.cnentry.place(relx=0.4, rely=0.13, relwidth=0.6, relheight=0.05)
        self.ouentry.place(relx=0.4, rely=0.18, relwidth=0.6, relheight=0.05)
        self.oentry.place(relx=0.4, rely=0.23, relwidth=0.6, relheight=0.05)
        self.lentry.place(relx=0.4, rely=0.28, relwidth=0.6, relheight=0.05)
        self.sentry.place(relx=0.4, rely=0.33, relwidth=0.6, relheight=0.05)
        self.centry.place(relx=0.4, rely=0.38, relwidth=0.6, relheight=0.05)
        self.passentry.place(relx=0.4, rely=0.43, relwidth=0.6, relheight=0.05)
        Label(self.step2, text='Name').place(relx=0, rely=0.13, relwidth=0.4, relheight=0.05)
        Label(self.step2, text='Organization unit').place(relx=0, rely=0.18, relwidth=0.4, relheight=0.05)
        Label(self.step2, text='Organization').place(relx=0, rely=0.23, relwidth=0.4, relheight=0.05)
        Label(self.step2, text='City').place(relx=0, rely=0.28, relwidth=0.4, relheight=0.05)
        Label(self.step2, text='State').place(relx=0, rely=0.33, relwidth=0.4, relheight=0.05)
        Label(self.step2, text='Country').place(relx=0, rely=0.38, relwidth=0.4, relheight=0.05)
        Label(self.step2, text='Keystore password').place(relx=0, rely=0.43, relwidth=0.4, relheight=0.05)
        #Button(self.step2, text='Generate keystore', command=lambda x=None: self.genkeytool(self.cnentry.get(), self.ouentry.get(), self.oentry.get(), self.lentry.get(), self.sentry.get(), self.centry.get().upper()[0:2], f'{self.passentry.get()}123456pass')).place(relx=0, rely=0.95, relwidth=1, relheight=0.05)
        self.step3 = Frame(self.steps)
        Label(self.step3, text='Step 2: building and transfering to device', font='Arial 17').place(x=0, y=0, relwidth=1,relheight=0.1)
        #Button(self.step3, text='Build and transfer').place(relx=0, rely=0.95, relwidth=1, relheight=0.05)

        self.steps.add(self.step1, text='Step 1')
        self.steps.add(self.step2, text='Step 2')
        self.steps.add(self.step3, text='Step 3')
        self.steps.select(0)
        self.steps.place(x=0, y=0, relwidth=1, relheight=0.95)
        Button(self, text='Close', command=lambda x=None: self.goback()).place(x=0, rely=0.95, relwidth=0.5, relheight=0.05)
        Button(self, text='Proceed', command=lambda x=None: self.gonext(appname)).place(relx=0.5, rely=0.95, relwidth=0.5, relheight=0.05)

    def genkeytool(self, cn, ou, o, l, s, c, keypass):
        if os.path.exists(f'{os.getcwd()}/keystore.jks'):
            os.remove('keystore.jks')
        subprocess.run(f'keytool -genkey -v -keystore keystore.jks -alias keystoreofmod -keyalg RSA -keysize 2048 -validity 10000 -dname \"CN=.{cn.replace(' ', '_')}, OU=.{ou.replace(' ', '_')}, O=.{o.replace(' ', '_')}, L=.{l.replace(' ', '_')}, S=.{s.replace(' ', '_')}, C={c.replace(' ', '_') if not c.strip() == '' else 'UK'}\" -keypass {keypass.replace(' ', '_')} -storepass {keypass.replace(' ', '_')}', shell=True)

    def build(self, keypass, appname):
        if os.path.exists(f'{os.getcwd()}/base.apk'):
            os.remove('base.apk')
        if os.path.exists(f'{os.getcwd()}/basealigned.apk'):
            os.remove('basealigned.apk')
        if os.path.exists(f'{os.getcwd()}/basefull.apk'):
            os.remove('basefull.apk')
        if os.path.exists(f'{os.getcwd()}/basefull.apk.idsig'):
            os.remove('basefull.apk.idsig')

        with zipfile.ZipFile("base.apk", "w", zipfile.ZIP_STORED) as apk:
            for root, dirs, files in os.walk(f'{os.getcwd()}/temp'):
                for file in files:
                    file_path = os.path.join(root, file)
                    apk.write(file_path, os.path.relpath(file_path, f'{os.getcwd()}/temp'))

        subprocess.run(f'zipalign -p -f -v 4 base.apk basealigned.apk', shell=True)
        subprocess.run(f'apksigner sign --ks keystore.jks --ks-key-alias keystoreofmod --ks-pass pass:{keypass} -key-pass pass:{keypass} --out basefull.apk basealigned.apk', shell=True)
        subprocess.run(f'adb uninstall {appname}', shell=True)
        subprocess.run(f'adb install basefull.apk', shell=True)

    def goback(self):
        self.destroy()

    def gonext(self, appname):
        if self.steps.index('current') == 1:
            self.genkeytool(self.cnentry.get(), self.ouentry.get(), self.oentry.get(), self.lentry.get(),
                           self.sentry.get(), self.centry.get().upper()[0:2], f'{self.passentry.get()}123456pass')
        elif self.steps.index('current') == 2:
            self.build(f'{self.passentry.get()}123456pass'.replace(' ', '_'), appname)

        try:
            self.steps.select(self.steps.index('current') + 1)
        except:
            self.destroy()

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
                Button(step2, text='Modify', command=lambda x=None: show_explorer(f'{os.getcwd()}/temp')).place(relx=0, rely=0.8, relwidth=1, relheight=0.1)
                Button(step2, text='Build and transfer', command=lambda x=None: install(appname)).place(relx=0, rely=0.9, relwidth=1, relheight=0.1)

def show_explorer(path):
    explorer = Toplevel(window)
    explorer.geometry('800x600')
    FileManager(explorer, path).place(x=0, y=0, relwidth=1, relheight=1)

def install(appname):
    #step2.place_forget()
    #chooseappcombo.current(0)

    InstallWizard(window, appname)

window = Tk()
window.title('WeAreModding! v1.0')
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
