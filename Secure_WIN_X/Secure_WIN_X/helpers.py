import winreg
import logging
import subprocess


def set_regkey_value(value_entry):
    opened_regkey = winreg.CreateKeyEx(
        value_entry.root_key, value_entry.subkey, 0, winreg.KEY_WOW64_64KEY + winreg.KEY_WRITE
    )
    winreg.SetValueEx(opened_regkey, value_entry.name, 0, value_entry.data_type, value_entry.data)
    winreg.CloseKey(opened_regkey)
    logging.info(f"Set {str(value_entry).lower()}")


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
    else:
        logging.error(f"{service_name!r} does not exist as an installed service")