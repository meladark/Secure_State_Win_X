import ctypes
import configparser
import logging
import os
import pathlib
import platform
import sys
import subprocess
import threading
import time
import webbrowser
import winreg
from itertools import chain, cycle
# Необходимо установить стороннюю библиотеку: "pip install pywin32"
import win32con
import win32event
import win32process
from win32com.shell import shellcon
from win32com.shell.shell import ShellExecuteEx

import HTML_con
from config_data import CONFIG_SECTIONS, TRACKING_AND_TELEMETRY
from regkeys_data import REGKEYS_DICT, ValueEntry

_SCRIPT_PATH = pathlib.WindowsPath(__file__).resolve()
_CWD = _SCRIPT_PATH.parent
_CONFIG_PATH = _CWD.joinpath("config.cfg")
_DOWNLOAD_PATH = pathlib.WindowsPath.home().joinpath(r"Downloads\config.cfg")

_LOGRECORD_FORMAT = "%(asctime)s | %(levelname)-8s | %(message)s"
logging.basicConfig(filename=_CWD.joinpath("logfile.log"), filemode="w", format=_LOGRECORD_FORMAT, level=logging.INFO)


def progressbar(process_name):
    def wrapper(func):
        def wrapped_func(*args, **kwargs):
            animations = cycle("|/—\\")
            t = threading.Thread(target=func, args=args, kwargs=kwargs)
            t.start()
            print(f"{process_name}...", end="  ")
            while t.is_alive():
                t.join(.1)
                print(f"\b{next(animations)}", end="", flush=True)
            print("\bЗавершено.")
            time.sleep(.5)
        return wrapped_func
    return wrapper


def is_user_an_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        # If admin check failed, assuming not an admin
        return False


def run_as_admin(*cmd_line, wait=True):
    verb = "runas"
    if not cmd_line:
        cmd_line = [sys.executable] + sys.argv
    cmd = cmd_line[0]
    params = " ".join(str(x) for x in cmd_line[1:])
    process_info = ShellExecuteEx(
        nShow=win32con.SW_SHOWNORMAL,
        fMask=shellcon.SEE_MASK_NOCLOSEPROCESS,
        lpVerb=verb,
        lpFile=cmd,
        lpParameters=params
    )
    if wait:
        process_handle = process_info['hProcess']
        win32event.WaitForSingleObject(process_handle, win32event.INFINITE)
        return_code = win32process.GetExitCodeProcess(process_handle)
    else:
        return_code = None
    return return_code


def create_default_config(config, config_path):
    for section, options in sorted(CONFIG_SECTIONS.items()):
        config.add_section(section)
        if options is None:
            config.set(section, "disable", "no")
        else:
            for option in options:
                config.set(section, option, "no")
    with open(config_path, "w") as config_file:
        config.write(config_file)
    return config


def get_config(config_path):
    config = configparser.ConfigParser()
    config.BOOLEAN_STATES.update({"": False})
    if not os.path.exists(config_path):
        return create_default_config(config, config_path)
    try:
        config.read(config_path)
    except configparser.ParsingError as pars_err:
        print(f"Config file {config_path!r} contains errors:")
        for line_number, key_name in pars_err.errors:
            key_name = key_name.replace("\'", "").replace("\\n", "")
            print(f"\t[line {line_number}] Key {key_name!r} without value")
        raise
    for section in config:
        try:
            if section != "DEFAULT" and section not in CONFIG_SECTIONS:
                raise configparser.NoSectionError(section)
        except configparser.NoSectionError:
            print(f"Incorrect section name {section!r} in config file {config_path!r}."
                  f"\nAvailable sections names: {', '.join(name for name in CONFIG_SECTIONS)}")
            raise
    return config


def set_regkey_value(value_entry):
    try:
        opened_regkey = winreg.CreateKeyEx(
            value_entry.root_key, value_entry.subkey, 0, winreg.KEY_WOW64_64KEY + winreg.KEY_WRITE
        )
        winreg.SetValueEx(opened_regkey, value_entry.name, 0, value_entry.data_type, value_entry.data)
        winreg.CloseKey(opened_regkey)
        logging.info(f"Set {str(value_entry).lower()}")
        HTML_con.html_in(str(value_entry))
    except Exception:
        HTML_con.html_in(str(value_entry), Param=False)


def run_pwrshell_cmd(*args):
    logging.info(f"Run PowerShell command {' '.join(args)!r}")
    pwrshell_proc = subprocess.run(
        ["powershell", "-Command", *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    if not pwrshell_proc.returncode:
        logging.info(f"[OK] The exit status of last command is 0")
    else:
        logging.warning(f"[FAIL] The exit status of last command is non-zero")
    return pwrshell_proc


def run_shell_cmd(command):
    logging.info(f'Run command {command!r}')
    proc = subprocess.run(command.split(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc


def disable_service(service_name):
    sc_proc = run_shell_cmd(f"sc.exe query {service_name}")
    if sc_proc.returncode != 1060:
        run_shell_cmd(f"sc.exe stop {service_name}")
        run_shell_cmd(f"sc.exe config {service_name} start=disabled")
        logging.info(f"Service {service_name!r} is disabled")
        HTML_con.html_in(service_name)
    else:
        logging.error(f"{service_name!r} does not exist as an installed service")
        HTML_con.html_in(f"Служба {service_name!r} уже отключена")


@progressbar("Удаление встроенных приложений")
def delete_builtin_apps(config_options):
    HTML_con.html_in("Удаленные приложения:",0)
    for app_name, delete in config_options:
        if delete:
            pwrshell_proc = run_pwrshell_cmd(fr'if ((Get-AppxPackage *{app_name}*)){{return 1}}else{{return 0}}')  # TODO: Remove-AppxPackage
            if(pwrshell_proc.stdout == b'1\r\n'): 
                HTML_con.html_in(app_name)
            elif(pwrshell_proc.stdout == b'0\r\n'): 
                HTML_con.html_in(app_name, Param = False)
                HTML_con.html_in("Такого приложения не найдено, вероятно оно не было установлено.",2)
        else:
            HTML_con.html_in(app_name, Param = False)
            HTML_con.html_in("Отключено в конфигурационном файле",2)


@progressbar("Отключение микрофона")
def Out_microphone():
    HTML_con.html_in("Выключение микрофона",0)
    PATH = r"SOFTWARE\Microsoft\Windows\CurrentVersion\MMDevices\Audio\Capture"
    aKey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, PATH, 0, winreg.KEY_WOW64_64KEY + winreg.KEY_READ)
    try:
        for j in range(winreg.QueryInfoKey(aKey)[0]):
            new_Key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, fr'{PATH}\{winreg.EnumKey(aKey,j)}', 0, winreg.KEY_WOW64_64KEY + winreg.KEY_READ)
            for i in range(winreg.QueryInfoKey(new_Key)[0]):
                try:
                    asubkey_name = winreg.EnumKey(new_Key, i)
                    asubkey = winreg.OpenKey(new_Key,asubkey_name)
                    val = winreg.QueryValueEx(asubkey, "{a45c254e-df1c-4efd-8020-67d146a850e0},2")
                    if (('Microphone' in val) or ('Микрофон' in val)):
                        # Добавил логирование
                        value_entry = ValueEntry(winreg.HKEY_LOCAL_MACHINE, fr"{PATH}\{winreg.EnumKey(aKey,j)}", "DeviceState", winreg.REG_DWORD, 10000001)
                        Key_for_delete = winreg.OpenKey(value_entry.root_key, value_entry.subkey, 0, winreg.KEY_WOW64_64KEY + winreg.KEY_SET_VALUE + winreg.KEY_READ)
                        winreg.SetValueEx(Key_for_delete, value_entry.name, 0, value_entry.data_type, value_entry.data)
                        logging.info(f"Set {str(value_entry).lower()}")
                        # Две строки ниже можно убрать, но пока оставил...
                        # winreg.CloseKey(Key_for_delete)
                        # Key_for_delete = winreg.OpenKeyEx(value_entry.root_key, value_entry.subkey, 0, winreg.KEY_WOW64_64KEY + winreg.KEY_READ)
                        if (winreg.QueryValueEx(Key_for_delete,"DeviceState")[0] == 10000001):
                            HTML_con.html_in("Микрофон отключен")                  #10000001
                        else:
                            HTML_con.html_in("Микрофон не отключен", Param = False)
                        winreg.CloseKey(Key_for_delete)
                except EnvironmentError as e:
                    pass
                    # print(e)
                except FileNotFoundError:
                    pass
    except WindowsError as e:
        logging.error(e)
        pass
    winreg.CloseKey(aKey)
    winreg.CloseKey(new_Key)


@progressbar("Отключение веб-камеры")
def Out_webcam():
    HTML_con.html_in("Состояние Веб-камеры",0)
    Command_for_find_PnPDevice = 'if ((get-pnpDevice | where {{$_.FriendlyName -like "*Webcam*"}})){{return 1}}else{{return 0}}'
    Command_for_disabled_PnPDevice = '| Disable-PnpDevice'
    proc = subprocess.run(['powershell',fr'if ((get-pnpDevice | where {{$_.FriendlyName -like "*Webcam*"}})){{return 1}}else{{return 0}}'], stdout = subprocess.PIPE)
    if(proc.stdout == b'1\r\n'):
        #subprocess.run(['powershell',get-pnpDevice | where {{$_.FriendlyName -like "*Webcam*"}}{Command_for_disabled_PnPDevice}])
        HTML_con.html_in("Веб-камера отключена успешно.")
    elif(proc.stdout == b'0\r\n'):
        HTML_con.html_in("Устройство Веб-камеры не было найдено", Param = False)
    else:
        HTML_con.html_in(proc.stdout,3)
    logging.info(proc.stdout)


def disable_powershell_scripts_execution():
    HTML_con.html_in("Выполнение сценариев PowerShell", 0)
    regkeys = REGKEYS_DICT.get("powershell")
    HTML_con.html_in("Установленные параметры реестра:", 3)
    for regkey in regkeys.get("exec_policy"):
        set_regkey_value(regkey)


@progressbar("Отключение Internet Explorer")
def disable_internet_explorer():
    HTML_con.html_in("Internet Explorer", 0)
    dism_params = "/Online /Disable-Feature /FeatureName:Internet-Explorer-Optional-amd64 /NoRestart"
    dism_proc = run_shell_cmd(f"dism.exe {dism_params}")
    if not dism_proc.returncode:
        HTML_con.html_in("Internet Explorer был отключен")
        HTML_con.html_in("Примечание: чтобы изменение вступило в силу, необходимо перезагрузить компьютер", 2)
        HTML_con.html_in("Важно! Поскольку Internet Explorer остается установленным на компьютере даже после "
                         "его отключения, следует и впредь устанавливать обновления безопасности, применимые "
                         "к Internet Explorer", 2)
    else:
        HTML_con.html_in("Internet Explorer НЕ был отключен", Param=False)


@progressbar("Удаление OneDrive")
def uninstall_onedrive():
    HTML_con.html_in("OneDrive", 0)
    regkeys = REGKEYS_DICT.get("onedrive")
    run_shell_cmd("taskkill.exe /f /im OneDrive.exe")
    # Remove OneDrive
    is_64bit = True if platform.architecture()[0] == "64bit" else False
    sys_folder = "SysWOW64" if is_64bit else "System32"
    run_shell_cmd(os.path.expandvars(rf"%SystemRoot%\{sys_folder}\OneDriveSetup.exe /uninstall"))
    HTML_con.html_in("OneDrive отключен")
    HTML_con.html_in("Установленные параметры реестра:", 3)
    # Disable OneDrive via Group Policies
    for regkey in regkeys.get("group_policies"):
        set_regkey_value(regkey)
    # Remove Onedrive from explorer sidebar
    set_regkey_value(regkeys.get("explorer_sidebar").get("default"))
    if is_64bit:
        set_regkey_value(regkeys.get("explorer_sidebar").get("64bit"))
    # Removing startmenu entry
    run_pwrshell_cmd(
        "Remove-Item -Force -ErrorAction SilentlyContinue",
        os.path.expandvars(r"'%UserProfile%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\OneDrive.lnk'")
    )
    # Removing scheduled task
    run_pwrshell_cmd(
        r"Get-ScheduledTask -TaskPath '\' -TaskName 'OneDrive*' -ErrorAction SilentlyContinue", "|",
        "Unregister-ScheduledTask -Confirm:$false"
    )


@progressbar("Отключение удаленного доступа")
def disable_remote_access():
    HTML_con.html_in("Удаленный доступ", 0)
    regkeys = REGKEYS_DICT.get("remote_access")
    HTML_con.html_in("Установленные параметры реестра:", 3)
    # Disable Remote Assistance
    for regkey in regkeys.get("remote_assistance"):
        set_regkey_value(regkey)
    # Disable Remote Desktop
    for regkey in regkeys.get("remote_desktop"):
        set_regkey_value(regkey)
    HTML_con.html_in("Удаленный помощник (Remote Assistance) отключен")
    HTML_con.html_in("Удаленный рабочий стол (Remote Desktop) отключен")


@progressbar("Отключение определения местоположения")
def disable_location_and_sensors():
    HTML_con.html_in("Местоположение и сенсоры", 0)
    regkeys = REGKEYS_DICT.get("location_and_sensors")
    HTML_con.html_in("Установленные параметры реестра:", 3)
    for regkey in regkeys:
        set_regkey_value(regkey)
    HTML_con.html_in("Службы определения местоположения были отключены")


@progressbar("Отключение функций слежения и телеметрии")
def disable_diagtracking_and_telemetry(config_options):
    HTML_con.html_in("Функции слежения и телеметрия", 0)
    regkeys = REGKEYS_DICT.get("diagtracking_and_telemetry")
    for option, disable in config_options:
        if disable:
            HTML_con.html_in(TRACKING_AND_TELEMETRY.get(option))
            if option == "connected_user_experiences_and_telemetry":
                HTML_con.html_in("Отключенные службы:", 3)
                # Disable Diagnostics Tracking Service
                disable_service("DiagTrack")
                # Disable Microsoft Diagnostics Hub Standard Collector Service
                disable_service("diagnosticshub.standardcollector.service")
                # Disable WAP Push Message Routing Service
                disable_service("dmwappushservice")
            option_regkeys = regkeys.get(option)
            if isinstance(option_regkeys, dict):
                option_regkeys = chain(*option_regkeys.values())
            HTML_con.html_in("Установленные параметры реестра:", 3)
            for regkey in option_regkeys:
                set_regkey_value(regkey)


if __name__ == "__main__":
    if not is_user_an_admin():
        try:
            run_as_admin("cmd", "/C", sys.executable, _SCRIPT_PATH)
        except Exception:
            print("Please run this program as administrator!")
            logging.critical("You need to run a program as administrator!")
            exit(1)
    else:
        try:
            webbrowser.open_new(_CWD.joinpath("Web_Form_For_Conf.html"))
            while not pathlib.WindowsPath.exists(_DOWNLOAD_PATH):
                time.sleep(1)
            _DOWNLOAD_PATH.replace(_CONFIG_PATH)
            config = get_config(_CONFIG_PATH)
        except Exception:
            logging.critical("Unable to read config file")
            exit(1)
        else:
            # TODO: добавить аргумент с путём до каталога, где будет создаваться HTML-файл
            HTML_con.Init_html()
            funcs = {
                "delete_builtin_apps": delete_builtin_apps,
                "diagnostic_tracking_and_telemetry": disable_diagtracking_and_telemetry,
                "internet_explorer": disable_internet_explorer,
                "location_and_sensors": disable_location_and_sensors,
                "microphone": Out_microphone,
                "onedrive": uninstall_onedrive,
                "powershell_scripts_execution": disable_powershell_scripts_execution,
                "remote_access": disable_remote_access,
                "webcam": Out_webcam,
            }
            for section in CONFIG_SECTIONS:
                if config.has_section(section):
                    config_options = {option: config[section].getboolean(option) for option in config[section]}
                    if config_options.get("disable"):
                        funcs.get(section.lower(), lambda: None)()
                    if "disable" not in config_options:
                        funcs.get(section.lower())(config_options.items())
            # TODO: добавить аргумент с путём до каталога, откуда будет открываться HTML-файл
            HTML_con.Out()
            input("\nPress any key to exit...")
