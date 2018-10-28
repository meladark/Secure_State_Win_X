from dataclasses import dataclass
from typing import Any
from winreg import HKEY_CURRENT_USER as HKCU
from winreg import HKEY_LOCAL_MACHINE as HKLM
from winreg import HKEY_CLASSES_ROOT as HKCR
from winreg import REG_SZ
from winreg import REG_DWORD


REGISTRY_HIVES = {
    HKCU: 'HKCU',
    HKLM: 'HKLM',
    HKCR: 'HKCR'
}


REGISTRY_VALUE_TYPES = {
    REG_SZ: 'REG_SZ',
    REG_DWORD: 'REG_DWORD'
}


@dataclass()
class ValueEntry:
    root_key: int
    subkey: str
    name: str
    data_type: int = None
    data: Any = None

    def __repr__(self):
        registry_key = "\\".join((REGISTRY_HIVES[self.root_key], self.subkey))
        return (
            fr"Value entry (name={self.name!r}, type={REGISTRY_VALUE_TYPES[self.data_type]!r}, data={self.data!r}) "
            fr"of registry key {registry_key!r}"
        )


if __name__ == "__main__":
    import winreg
    opened_regkey = winreg.CreateKeyEx(
        winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Remote Assistance", 0, winreg.KEY_READ + winreg.KEY_WOW64_64KEY
    )
    print(winreg.QueryValueEx(opened_regkey, "fAllowFullControl"))
