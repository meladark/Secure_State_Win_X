import winreg
import subprocess
import logging

def Delete_microsoft_programm():
    List_of_programm = ['camera','Facebook','xbox',
                        'Microsoft.SkypeApp','Messaging',
                        'Netflix','OneNote',
                        'CommsPhone','SkypeApp','Twitter',
                        'soundrecorder','XboxOneSmartGlass',
                        'OneConnect','Minecraft',
                        'HiddenCityMysteryofShadows','MarchofEmpires',
                        'CandyCrush','People']
    logging.basicConfig(filename ="Log.txt", level=logging.INFO)
    for List in List_of_programm:
        try:
            #proc = subprocess.Popen(['powershell','Get-AppxPackage *%s*| Remove-AppxPackage;' % List])
            logging.info("Success %s" % List)
        except:
            logging.info('Unsuccess %s' % List)
    proc = subprocess.Popen(['powershell','C:\Windows\SysWOW64\OneDriveSetup.exe /uninstall'])
    proc.wait()

def Out_microfon():
    PATH = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
    Reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
    keyVal = r"SOFTWARE\Microsoft\Windows\CurrentVersion\MMDevices\Audio\Capture\{3d08eafc-1fbe-4572-b102-3e217b70c85d}"
    aKey = winreg.OpenKeyEx(winreg.HKEY_LOCAL_MACHINE, PATH, 0, winreg.KEY_READ)
    for i in range(1024):
        try:
            #i = 0
            #while True:
                #print(winreg.EnumKey(aKey, i),i)
                asubkey_name = winreg.EnumKey(aKey, i)
                #winreg.OpenKeyEx(aKey,winreg.EnumKey(aKey, i))
                asubkey=winreg.OpenKey(aKey,asubkey_name)
                val=winreg.QueryValue(asubkey, "DisplayName")
                print (val)
                #print(winreg.QueryValueEx(winreg.OpenKeyEx(aKey,winreg.EnumKey(aKey, i)),"Name"))
                #i += 1
        except EnvironmentError:
            break
        #except WindowsError:
         #   break


if __name__ == '__main__':
    #Delete_microsoft_programm()
    Out_microfon()