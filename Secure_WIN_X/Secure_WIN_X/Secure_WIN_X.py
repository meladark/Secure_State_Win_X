import winreg
import subprocess
import logging
import os

def Delete_microsoft_programm():
    List_of_programm = ['camera','Facebook','xbox',
                        'Microsoft.SkypeApp','Messaging',
                        'Netflix','OneNote',
                        'CommsPhone','SkypeApp','Twitter',
                        'soundrecorder','XboxOneSmartGlass',
                        'OneConnect','Minecraft',
                        'HiddenCityMysteryofShadows','MarchofEmpires',
                        'CandyCrush','People','NetworkSpeedTest','todos',
                        'WhiteBoard','OfficeLens']
    
    for List in List_of_programm:
        try:
            #proc = subprocess.run(['powershell','Get-AppxPackage *%s*| Remove-AppxPackage;' % List])
            logging.info("Success %s" % List)
        except WindowsError as e:
            logging.info('Unsuccess %s \n %s' % List,e)
    #proc = subprocess.run(['powershell','C:\Windows\SysWOW64\OneDriveSetup.exe /uninstall'])

def Out_microphone():
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
                        print(winreg.EnumKey(aKey,j))
                        print(winreg.EnumKey(new_Key, i))
                        print(val)
                        print(fr'{PATH}\{winreg.EnumKey(aKey,j)}')
                        Key_for_delete = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,fr'{PATH}\{winreg.EnumKey(aKey,j)}',0,winreg.KEY_WOW64_64KEY + winreg.KEY_SET_VALUE)                      
                        #winreg.SetValueEx(Key_for_delete,"DeviceState",0,winreg.REG_DWORD,1000001) # добавить правильное значение ключа.
                        winreg.CloseKey(Key_for_delete)
                except EnvironmentError:
                    pass 
    except WindowsError as e:
        print(e)
        pass
    winreg.CloseKey(aKey)
    winreg.CloseKey(new_Key)

def Out_webcam():
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

def Beautiful_conclusion(Text_output_for_html):
    #Text_output_for_html.replace(r"\\",r" ")
    file = open("Test.html","w")
    file.write(f"<html><body><pre>{Text_output_for_html}</pre></body></html>")
    os.startfile("Test.html")

if __name__ == '__main__':
    logging.basicConfig(filename ="Log.doc", level=logging.INFO)
    #Delete_microsoft_programm()
    string = Out_webcam()
    #Out_microphone()
    Beautiful_conclusion(string)