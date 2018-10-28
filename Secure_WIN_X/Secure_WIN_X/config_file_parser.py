import configparser
import os

from config_data import BUILTIN_APPS, TRACKING_AND_TELEMETRY


CONFIG_SECTIONS = {
    "DELETE_BUILTIN_APPS": BUILTIN_APPS,
    "DIAGNOSTIC_TRACKING_AND_TELEMETRY": TRACKING_AND_TELEMETRY,
    "INTERNET_EXPLORER": None,
    "LOCATION_AND_SENSORS": None,
    "MICROPHONE": None,
    "ONEDRIVE": None,
    "POWERSHELL_SCRIPTS_EXECUTION": None,
    "REMOTE_ACCESS": None,
    "WEBCAM": None,
}


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


if __name__ == "__main__":
    get_config('abc.cfg')
