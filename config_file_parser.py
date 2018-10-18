import configparser
import os

BUILTIN_APPS = [
    '3DBuilder', 'Appconnector', 'BingFinance', 'BingNews', 'BingSports', 'BingTranslator', 'BingWeather', 'CandyCrush',
    'CommsPhone', 'Facebook', 'HiddenCityMysteryOfShadows', 'MarchOfEmpires', 'Messaging', 'Microsoft3DViewer',
    'MicrosoftOfficeHub', 'MicrosoftPowerBIForWindows', 'MicrosoftSolitaireCollection', 'MicrosoftStickyNotes',
    'Minecraft', 'Netflix', 'NetworkSpeedTest', 'OfficeLens', 'OneConnect', 'OneNote', 'People', 'Photos', 'Print3D',
    'SkypeApp', 'Twitter', 'Wallet', 'Whiteboard', 'WindowsAlarms', 'WindowsCalculator', 'WindowsCamera', 'WindowsMaps',
    'WindowsPhone', 'WindowsSoundRecorder', 'Xbox', 'YourPhone', 'ZuneMusic', 'ZuneVideo', 'windowscommunicationsapps'
]

SECTIONS_NAMES = [
    'DELETE_BUILTIN_APPS',
    'DIAGNOSTIC_TRACKING_AND_TELEMETRY',
    'INTERNET_EXPLORER',
    'LOCATION_AND_SENSORS',
    'MICROPHONE',
    'ONEDRIVE',
    'POWERSHELL_SCRIPTS_EXECUTION',
    'REMOTE_ACCESS',
    'WEBCAM',
]


def create_default_config(config, config_path):
    for section in SECTIONS_NAMES:
        config.add_section(section)
        if 'BUILTIN_APPS' in section:
            for app in BUILTIN_APPS:
                config.set('DELETE_BUILTIN_APPS', app, 'no')
        else:
            config.set(section, 'disable', 'no')
    with open(config_path, 'w') as config_file:
        config.write(config_file)
    return config


def get_config(config_path):
    config = configparser.ConfigParser()
    config.BOOLEAN_STATES.update({'': False})
    if not os.path.exists(config_path):
        return create_default_config(config, config_path)
    try:
        config.read(config_path)
    except configparser.ParsingError as pars_err:
        print(f'Config file {config_path!r} contains errors:')
        for line_number, key_name in pars_err.errors:
            key_name = key_name.replace("\'", "").replace('\\n', '')
            print(f'\t[line {line_number}] Key {key_name!r} without value')
        raise
    for section in config:
        try:
            if section != 'DEFAULT' and section not in SECTIONS_NAMES:
                raise configparser.NoSectionError(section)
        except configparser.NoSectionError:
            print(f'Incorrect section name {section!r} in config file {config_path!r}.'
                  f'\nAvailable sections names: {", ".join(name for name in SECTIONS_NAMES)}')
            raise
    return config
