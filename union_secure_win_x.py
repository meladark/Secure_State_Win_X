import ctypes
import inspect
import logging
import os
import platform
import subprocess
import sys
import winreg

from config_file_parser import get_config, SECTIONS_NAMES
from regkey_value_entry import ValueEntry, HKLM, HKCU, HKCR


def set_regkey_value(value_entry):
    opened_regkey = winreg.CreateKeyEx(value_entry.root_key, value_entry.subkey, 0, winreg.KEY_WRITE)
    winreg.SetValueEx(opened_regkey, value_entry.name, 0, value_entry.data_type, value_entry.data)
    winreg.CloseKey(opened_regkey)
    logging.info(f'Set {str(value_entry).lower()}')


def run_pwrshell_cmd(*args):
    logging.info(f'Run PowerShell command {" ".join(args)!r}')
    try:
        pwrshell_proc = subprocess.run(['powershell', '-Command', *args], capture_output=True, check=True)
        logging.info(f'[OK] The exit status of last command is 0')
    except subprocess.CalledProcessError:
        logging.warning(f'[FAIL] The exit status of last command is non-zero')
    return pwrshell_proc


def run_shell_cmd(command):
    logging.info(f'Run command {command!r}')
    proc = subprocess.run(command.split(), shell=True, capture_output=True)
    return proc


def disable_service(service_name):
    sc_proc = run_shell_cmd(f'sc.exe query {service_name}')
    if sc_proc.returncode != 1060:
        run_shell_cmd(f'sc.exe stop {service_name}')
        run_shell_cmd(f'sc.exe config {service_name} start=disabled')
        logging.info(f'Service {service_name!r} is disabled')
    else:
        logging.error(f'{service_name!r} does not exist as an installed service')


def delete_builtin_apps(apps):
    for app, delete in apps:
        if delete:
            run_pwrshell_cmd(f'Get-AppxPackage *{app.name}* | Remove-AppxPackage')


def disable_microphone():
    PATH = r"SOFTWARE\Microsoft\Windows\CurrentVersion\MMDevices\Audio\Capture"
    aKey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, PATH, 0,winreg.KEY_WOW64_64KEY + winreg.KEY_READ) # 
    try:
        for j in range(winreg.QueryInfoKey(aKey)[0]):
            new_Key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,fr'{PATH}\{winreg.EnumKey(aKey,j)}',0,winreg.KEY_WOW64_64KEY + winreg.KEY_READ)
            for i in range(winreg.QueryInfoKey(new_Key)[0]):
                try:
                    asubkey_name = winreg.EnumKey(new_Key, i)
                    asubkey = winreg.OpenKey(new_Key,asubkey_name)
                    val = winreg.QueryValueEx(asubkey, "{a45c254e-df1c-4efd-8020-67d146a850e0},2")
                    if (('Microphone' in val) or ('Микрофон' in val)):
                        Key_for_delete = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,fr'{PATH}\{winreg.EnumKey(aKey,j)}',0,winreg.KEY_WOW64_64KEY + winreg.KEY_SET_VALUE)                      
                        winreg.SetValueEx(Key_for_delete,"DeviceState",0,winreg.REG_DWORD,1000001) # добавить правильное значение ключа.
                        winreg.CloseKey(Key_for_delete)
                except EnvironmentError:
                    pass 
    except WindowsError as e:
        logging.error(e)
        pass
    winreg.CloseKey(aKey)
    winreg.CloseKey(new_Key)


def disable_webcam():
    string = ""
    print('Start')
    Command_for_find_PnPDevice = 'get-pnpDevice | where {$_.FriendlyName -like "*Webcam*"}'
    Command_for_disabled_PnPDevice = '| Disable-PnpDevice'
    proc = subprocess.run(['powershell',Command_for_find_PnPDevice], shell=True, stdout = subprocess.PIPE)
    print(proc.stdout)
    string += str(proc.stdout)
    logging.info(proc.stdout)
    print('Over')
    return string


def disable_powershell_scripts_execution():
    set_regkey_value(ValueEntry(HKLM, r'SOFTWARE\Microsoft\PowerShell\1\ShellIds\Microsoft.PowerShell', 'ExecutionPolicy', winreg.REG_SZ, 'Restricted'))


def disable_internet_explorer():
    dism_params = '/Online /Disable-Feature /FeatureName:Internet-Explorer-Optional-amd64 /NoRestart'
    run_shell_cmd(f'dism.exe {dism_params}')


def uninstall_onedrive():
    run_shell_cmd('taskkill.exe /f /im OneDrive.exe')
    # Remove OneDrive
    sys_folder = 'SysWOW64' if platform.architecture()[0] == '64bit' else 'System32'
    run_shell_cmd(os.path.expandvars(rf'%SystemRoot%\{sys_folder}\OneDriveSetup.exe /uninstall'))
    # Disable OneDrive via Group Policies
    set_regkey_value(ValueEntry(HKLM, 'SOFTWARE\Policies\Microsoft\Windows\OneDrive', 'DisableFileSyncNGSC', winreg.REG_DWORD, 1))
    set_regkey_value(ValueEntry(HKLM, 'SOFTWARE\Policies\Microsoft\Windows\OneDrive', 'DisableFileSync', winreg.REG_DWORD, 1))
    set_regkey_value(ValueEntry(HKLM, 'SOFTWARE\Policies\Microsoft\Windows\OneDrive', 'DisableMeteredNetworkFileSync', winreg.REG_DWORD, 1))
    set_regkey_value(ValueEntry(HKLM, 'SOFTWARE\Policies\Microsoft\Windows\OneDrive', 'DisableLibrariesDefaultSaveToOneDrive', winreg.REG_DWORD, 1))
    # Remove Onedrive from explorer sidebar
    value_entry = ValueEntry(HKCR, r'CLSID\{018D5C66-4533-4307-9B53-224DE2ED1FE6}', 'System.IsPinnedToNameSpaceTree', winreg.REG_DWORD, 0)
    set_regkey_value(value_entry)
    if platform.architecture()[0] == '64bit':
        value_entry.subkey = rf'Wow6432Node\{value_entry.subkey}'
        set_regkey_value(value_entry)
    # Removing startmenu entry
    run_pwrshell_cmd(
        'Remove-Item -Force -ErrorAction SilentlyContinue',
        os.path.expandvars(r'"%UserProfile%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\OneDrive.lnk"')
    )
    # Removing scheduled task
    run_pwrshell_cmd(
        r'Get-ScheduledTask -TaskPath "\" -TaskName "OneDrive*" -ErrorAction SilentlyContinue', '|',
        'Unregister-ScheduledTask -Confirm:$false'
    )


def disable_remote_access():
    # Disable Remote Assistance
    set_regkey_value(ValueEntry(HKLM, r'SYSTEM\CurrentControlSet\Control\Remote Assistance', 'fAllowToGetHelp', winreg.REG_DWORD, 0))
    set_regkey_value(ValueEntry(HKLM, r'SYSTEM\CurrentControlSet\Control\Remote Assistance', 'fAllowFullControl', winreg.REG_DWORD, 0))
    # Disable Remote Desktop
    set_regkey_value(ValueEntry(HKLM, r'SYSTEM\CurrentControlSet\Control\Terminal Server', 'fDenyTSConnections', winreg.REG_DWORD, 1))


def disable_location_and_sensors():
    set_regkey_value(ValueEntry(HKLM, r'SOFTWARE\Policies\Microsoft\Windows\LocationAndSensors', 'DisableLocation', winreg.REG_DWORD, 1))
    set_regkey_value(ValueEntry(HKLM, r'SOFTWARE\Policies\Microsoft\Windows\LocationAndSensors', 'DisableLocationScripting', winreg.REG_DWORD, 1))
    set_regkey_value(ValueEntry(HKLM, r'SOFTWARE\Policies\Microsoft\Windows\LocationAndSensors', 'DisableSensors', winreg.REG_DWORD, 1))
    set_regkey_value(ValueEntry(HKLM, r'SOFTWARE\Policies\Microsoft\Windows\LocationAndSensors', 'DisableWindowsLocationProvider', winreg.REG_DWORD, 1))
    set_regkey_value(ValueEntry(HKLM, r'SYSTEM\CurrentControlSet\Services\lfsvc', 'Start', winreg.REG_DWORD, 4))
    set_regkey_value(ValueEntry(HKCU, r'SOFTWARE\Microsoft\Windows NT\CurrentVersion\Sensor\Permissions\{BFA794E4-F964-4FDB-90F6-51056BFE4B44}', 'SensorPermissionState', winreg.REG_DWORD, 0))
    set_regkey_value(ValueEntry(HKLM, r'SOFTWARE\Microsoft\Windows NT\CurrentVersion\Sensor\Overrides\{BFA794E4-F964-4FDB-90F6-51056BFE4B44}', 'SensorPermissionState', winreg.REG_DWORD, 0))


def disable_diagnostic_tracking_and_telemetry():
    # Disable Diagnostics Tracking Service
    disable_service('DiagTrack')
    # Disable Microsoft Diagnostics Hub Standard Collector Service
    disable_service('diagnosticshub.standardcollector.service')
    # Disable WAP Push Message Routing Service
    disable_service('dmwappushservice')
    # disable_service('WMPNetworkSvc')  # Windows Media Player Network Sharing Service
    # Disable telemetry
    set_regkey_value(ValueEntry(HKLM, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\DataCollection', 'AllowTelemetry', winreg.REG_DWORD, 0))
    set_regkey_value(ValueEntry(HKLM, r'SOFTWARE\Policies\Microsoft\Windows\DataCollection', 'AllowTelemetry', winreg.REG_DWORD, 0))
    set_regkey_value(ValueEntry(HKLM, r'SYSTEM\ControlSet001\Services\DiagTrack', 'Start', winreg.REG_DWORD, 4))
    set_regkey_value(ValueEntry(HKLM, r'SYSTEM\ControlSet001\Services\dmwappushsvc', 'Start', winreg.REG_DWORD, 4))
    set_regkey_value(ValueEntry(HKLM, r'SYSTEM\CurrentControlSet\Services\dmwappushservice', 'Start', winreg.REG_DWORD, 4))
    set_regkey_value(ValueEntry(HKLM, r'SYSTEM\CurrentControlSet\Services\diagnosticshub.standardcollector.service', 'Start', winreg.REG_DWORD, 4))
    # Disable Application Telemetry
    set_regkey_value(ValueEntry(HKLM, r'SOFTWARE\Policies\Microsoft\Windows\AppCompat', 'AITEnable', winreg.REG_DWORD, 0))
    # Disable Inventory Collector
    set_regkey_value(ValueEntry(HKLM, r'SOFTWARE\Policies\Microsoft\Windows\AppCompat', 'DisableInventory', winreg.REG_DWORD, 1))
    # Disable keylogger
    set_regkey_value(ValueEntry(HKLM, r'SOFTWARE\Microsoft\InputPersonalization', 'RestrictImplicitInkCollection', winreg.REG_DWORD, 1))
    set_regkey_value(ValueEntry(HKLM, r'SOFTWARE\Microsoft\InputPersonalization', 'RestrictImplicitTextCollection', winreg.REG_DWORD, 1))
    set_regkey_value(ValueEntry(HKCU, r'SOFTWARE\Microsoft\InputPersonalization\TrainedDataStore', 'HarvestContacts', winreg.REG_DWORD, 0))
    set_regkey_value(ValueEntry(HKLM, r'SOFTWARE\Policies\Microsoft\Windows\TabletPC', 'PreventHandwritingDataSharing', winreg.REG_DWORD, 1))
    set_regkey_value(ValueEntry(HKLM, r'SOFTWARE\Policies\Microsoft\Windows\HandwritingErrorReports', 'PreventHandwritingErrorReports', winreg.REG_DWORD, 1))
    # Disable loggers
    set_regkey_value(ValueEntry(HKLM, r'SYSTEM\ControlSet001\Control\WMI\AutoLogger\AutoLogger-Diagtrack-Listener', 'Start', winreg.REG_DWORD, 0))
    set_regkey_value(ValueEntry(HKLM, r'SYSTEM\CurrentControlSet\Control\WMI\AutoLogger\AutoLogger-Diagtrack-Listener', 'Start', winreg.REG_DWORD, 0))
    set_regkey_value(ValueEntry(HKLM, r'SYSTEM\CurrentControlSet\Control\WMI\AutoLogger\SQMLogger', 'Start', winreg.REG_DWORD, 0))
    # Disable Windows Customer Experience Improvement Program
    set_regkey_value(ValueEntry(HKLM, r'SOFTWARE\Policies\Microsoft\SQMClient\Windows', 'CEIPEnable', winreg.REG_DWORD, 0))
    set_regkey_value(ValueEntry(HKLM, r'SOFTWARE\Policies\Microsoft\SQMClient', 'CorporateSQMURL', winreg.REG_SZ, '0.0.0.0'))
    # Disable Windows Feedback
    set_regkey_value(ValueEntry(HKCU, r'SOFTWARE\Microsoft\Siuf\Rules', 'NumberOfSIUFInPeriod', winreg.REG_DWORD, 0))
    set_regkey_value(ValueEntry(HKCU, r'SOFTWARE\Microsoft\Siuf\Rules', 'PeriodInNanoSeconds', winreg.REG_DWORD, 0))
    set_regkey_value(ValueEntry(HKLM, r'SOFTWARE\Policies\Microsoft\Windows\DataCollection', 'DoNotShowFeedbackNotifications', winreg.REG_DWORD, 1))
    # Disable Microsoft Help Feedback
    set_regkey_value(ValueEntry(HKCU, r'SOFTWARE\Policies\Microsoft\Assistance\Client\1.0', 'NoExplicitFeedback', winreg.REG_DWORD, 1))
    # Disable Advertising ID
    set_regkey_value(ValueEntry(HKLM, r'SOFTWARE\Microsoft\Windows\CurrentVersion\AdvertisingInfo', 'Enabled', winreg.REG_DWORD, 0))
    set_regkey_value(ValueEntry(HKCU, r'SOFTWARE\Microsoft\Windows\CurrentVersion\AdvertisingInfo', 'Enabled', winreg.REG_DWORD, 0))
    set_regkey_value(ValueEntry(HKLM, r'SOFTWARE\Policies\Microsoft\Windows\AdvertisingInfo', 'DisabledByGroupPolicy', winreg.REG_DWORD, 1))
    # Disable browser access to local language
    set_regkey_value(ValueEntry(HKCU, r'Control Panel\International\User Profile', 'HttpAcceptLanguageOptOut', winreg.REG_DWORD, 1))


if __name__ == '__main__':
    logrecord_format = '%(asctime)s | %(levelname)-8s | %(message)s'
    logging.basicConfig(filename='logfile.log', filemode='w', format=logrecord_format, level=logging.DEBUG)
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print('Please run this program as administrator!')
        logging.critical(f'You need to run a program as administrator!')
        exit(1)
    else:
        # TODO: Add main config function
        try:
            config = get_config('config.cnf')
        except Exception:
            logging.critical(f'Unable to read config file')
        else:
            for section in SECTIONS_NAMES:
                if config.has_section(section):
                    if section == 'DELETE_BUILTIN_APPS':
                        section_items = ((option, config[section].getboolean(option)) for option in config[section])
                        delete_builtin_apps(section_items)
                    if section == 'DIAGNOSTIC_TRACKING_AND_TELEMETRY':
                        pass
                    if section == 'INTERNET_EXPLORER':
                        pass
                    if section == 'LOCATION_AND_SENSORS':
                        pass
                    if section == 'MICROPHONE':
                        pass
                    if section == 'ONEDRIVE':
                        pass
                    if section == 'POWERSHELL_SCRIPTS_EXECUTION':
                        pass
                    if section == 'REMOTE_ACCESS':
                        pass
                    if section == 'WEBCAM':
                        pass
