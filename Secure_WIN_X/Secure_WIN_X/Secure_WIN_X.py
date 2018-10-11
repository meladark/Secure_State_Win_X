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

def Out_microphone():
    PATH = r"SOFTWARE\Microsoft\Windows\CurrentVersion\MMDevices\Audio\Capture"
    Reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
    aKey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, PATH, 0,winreg.KEY_WOW64_64KEY + winreg.KEY_READ) # 
    try:
        for j in range(winreg.QueryInfoKey(aKey)[0]):
            new_Key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,fr'{PATH}\{winreg.EnumKey(aKey,j)}',0,winreg.KEY_READ)
            #print(new_Key)
            for i in range(winreg.QueryInfoKey(new_Key)[0]):
                try:
                    #print(winreg.EnumKey(new_Key, i),i)
                    asubkey_name = winreg.EnumKey(new_Key, i)
                    asubkey = winreg.OpenKey(new_Key,asubkey_name)
                    val = winreg.QueryValueEx(asubkey, "{a45c254e-df1c-4efd-8020-67d146a850e0},2")
                    if (('Microphone' in val) or ('Микрофон' in val)):
                        print(winreg.EnumKey(aKey,j))
                        print(winreg.EnumKey(new_Key, i))
                        print(val)
                        print(fr'{PATH}\{winreg.EnumKey(aKey,j)}')
                        Key_for_delete = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,fr'{PATH}\{winreg.EnumKey(aKey,j)}',0,winreg.KEY_SET_VALUE)
                        #winreg.SetValueEx(Key_for_delete,"DeviceState",0,winreg.REG_DWORD,0x00000009) # добавить правильное значение ключа.
                        winreg.CloseKey(Key_for_delete)
                except EnvironmentError:
                    pass 
    except WindowsError as e:
        print(e)
        pass

if __name__ == '__main__':
    #Delete_microsoft_programm()
    Out_microphone()