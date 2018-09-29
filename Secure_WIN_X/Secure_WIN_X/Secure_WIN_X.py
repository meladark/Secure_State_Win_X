import winreg
import subprocess

def Delete_microsoft_programm():
    List_of_programm = ['Get-AppxPackage *camera*| Remove-AppxPackage;','Get-AppxPackage *Facebook* | Remove-AppxPackage;',
                        'Get-AppxPackage *xbox* | Remove-AppxPackage;','Get-AppxPackage *Microsoft.SkypeApp* | Remove-AppxPackage;',
                        'Get-AppxPackage *Messaging* | Remove-AppxPackage;','Get-AppxPackage *Netflix* | Remove-AppxPackage;',
                        'Get-AppxPackage *OneNote* | Remove-AppxPackage;','Get-AppxPackage *CommsPhone* | Remove-AppxPackage;',
                        'Get-AppxPackage *SkypeApp* | Remove-AppxPackage;','Get-AppxPackage *Twitter* | Remove-AppxPackage;',
                        'Get-AppxPackage *soundrecorder* | Remove-AppxPackage;','Get-AppxPackage *XboxOneSmartGlass* | Remove-AppxPackage;',
                        'Get-AppxPackage *OneConnect*| Remove-AppxPackage;','Get-AppxPackage *Minecraft* | Remove-AppxPackage;',
                        'Get-AppxPackage *HiddenCityMysteryofShadows*| Remove-AppxPackage;','Get-AppxPackage *MarchofEmpires*| Remove-AppxPackage;',
                        'Get-AppxPackage *CandyCrush*| Remove-AppxPackage;','Get-AppxPackage *People*| Remove-AppxPackage;']
    for List in List_of_programm:
        try:
            proc = subprocess.Popen(['powershell',List])
        except:
            pass
    proc.wait()

def Out_microfon():
    PATH = r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\MMDevices\\Audio\\Capture"
    Reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
    keyVal = r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\MMDevices\\Audio"
    aKey = winreg.OpenKeyEx(winreg.HKEY_LOCAL_MACHINE, keyVal, 0, winreg.KEY_ALL_ACCESS)
    try:
        i = 0
        while True:
            print(winreg.EnumKey(aKey, i))
            i += 1
    except WindowsError:
        pass

Delete_microsoft_programm()