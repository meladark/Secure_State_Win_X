from regkey_value_entry import ValueEntry, HKLM, HKCU, HKCR, REG_SZ, REG_DWORD

REGKEYS_DICT = {
    "powershell": {
        "exec_policy": (
            ValueEntry(
                HKLM,
                r"SOFTWARE\Microsoft\PowerShell\1\ShellIds\Microsoft.PowerShell",
                "ExecutionPolicy",
                REG_SZ,
                "Restricted",
            ),
        )
    },
    "onedrive": {
        "group_policies": (
            ValueEntry(
                HKLM,
                r"SOFTWARE\Policies\Microsoft\Windows\OneDrive",
                "DisableFileSyncNGSC",
                REG_DWORD,
                1,
            ),
            ValueEntry(
                HKLM,
                r"SOFTWARE\Policies\Microsoft\Windows\OneDrive",
                "DisableFileSync",
                REG_DWORD,
                1,
            ),
            ValueEntry(
                HKLM,
                r"SOFTWARE\Policies\Microsoft\Windows\OneDrive",
                "DisableMeteredNetworkFileSync",
                REG_DWORD,
                1,
            ),
            ValueEntry(
                HKLM,
                r"SOFTWARE\Policies\Microsoft\Windows\OneDrive",
                "DisableLibrariesDefaultSaveToOneDrive",
                REG_DWORD,
                1,
            ),
        ),
        "explorer_sidebar": {
            "default": ValueEntry(
                HKCR,
                r"CLSID\{018D5C66-4533-4307-9B53-224DE2ED1FE6}",
                "System.IsPinnedToNameSpaceTree",
                REG_DWORD,
                0,
            ),
            "64bit": ValueEntry(
                HKCR,
                r"Wow6432Node\CLSID\{018D5C66-4533-4307-9B53-224DE2ED1FE6}",
                "System.IsPinnedToNameSpaceTree",
                REG_DWORD,
                0,
            ),
        },
    },
    "remote_access": {
        "remote_assistance": (
            ValueEntry(
                HKLM,
                r"SYSTEM\CurrentControlSet\Control\Remote Assistance",
                "fAllowToGetHelp",
                REG_DWORD,
                0,
            ),
            ValueEntry(
                HKLM,
                r"SYSTEM\CurrentControlSet\Control\Remote Assistance",
                "fAllowFullControl",
                REG_DWORD,
                0,
            ),
        ),
        "remote_desktop": (
            ValueEntry(
                HKLM,
                r"SYSTEM\CurrentControlSet\Control\Terminal Server",
                "fDenyTSConnections",
                REG_DWORD,
                1,
            ),
        ),
    },
    "location_and_sensors": (
        ValueEntry(
            HKLM,
            r"SOFTWARE\Policies\Microsoft\Windows\LocationAndSensors",
            "DisableLocation",
            REG_DWORD,
            1,
        ),
        ValueEntry(
            HKLM,
            r"SOFTWARE\Policies\Microsoft\Windows\LocationAndSensors",
            "DisableLocationScripting",
            REG_DWORD,
            1,
        ),
        ValueEntry(
            HKLM,
            r"SOFTWARE\Policies\Microsoft\Windows\LocationAndSensors",
            "DisableSensors",
            REG_DWORD,
            1,
        ),
        ValueEntry(
            HKLM,
            r"SOFTWARE\Policies\Microsoft\Windows\LocationAndSensors",
            "DisableWindowsLocationProvider",
            REG_DWORD,
            1,
        ),
        ValueEntry(HKLM, r"SYSTEM\CurrentControlSet\Services\lfsvc", "Start", REG_DWORD, 4),
        ValueEntry(
            HKCU,
            r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Sensor\Permissions\{BFA794E4-F964-4FDB-90F6-51056BFE4B44}",
            "SensorPermissionState",
            REG_DWORD,
            0,
        ),
        ValueEntry(
            HKLM,
            r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Sensor\Overrides\{BFA794E4-F964-4FDB-90F6-51056BFE4B44}",
            "SensorPermissionState",
            REG_DWORD,
            0,
        ),
    ),
    "diagtracking_and_telemetry": {
        "connected_user_experiences_and_telemetry": {
            "telemetry": (
                # Disable telemetry
                ValueEntry(
                    HKLM,
                    r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\DataCollection",
                    "AllowTelemetry",
                    REG_DWORD,
                    0,
                ),
                ValueEntry(
                    HKLM,
                    r"SOFTWARE\Policies\Microsoft\Windows\DataCollection",
                    "AllowTelemetry",
                    REG_DWORD,
                    0,
                ),
                ValueEntry(
                    HKLM, r"SYSTEM\ControlSet001\Services\DiagTrack", "Start", REG_DWORD, 4
                ),
                ValueEntry(
                    HKLM,
                    r"SYSTEM\ControlSet001\Services\dmwappushsvc",
                    "Start",
                    REG_DWORD,
                    4,
                ),
                ValueEntry(
                    HKLM,
                    r"SYSTEM\CurrentControlSet\Services\dmwappushservice",
                    "Start",
                    REG_DWORD,
                    4,
                ),
                ValueEntry(
                    HKLM,
                    r"SYSTEM\CurrentControlSet\Services\diagnosticshub.standardcollector.service",
                    "Start",
                    REG_DWORD,
                    4,
                ),
            ),
            "app_telemetry": (
                # Disable Application Telemetry
                ValueEntry(
                    HKLM,
                    r"SOFTWARE\Policies\Microsoft\Windows\AppCompat",
                    "AITEnable",
                    REG_DWORD,
                    0,
                ),
            ),
            "keylogger": (
                # Disable loggers
                ValueEntry(
                    HKLM,
                    r"SYSTEM\ControlSet001\Control\WMI\AutoLogger\AutoLogger-Diagtrack-Listener",
                    "Start",
                    REG_DWORD,
                    0,
                ),
                ValueEntry(
                    HKLM,
                    r"SYSTEM\CurrentControlSet\Control\WMI\AutoLogger\AutoLogger-Diagtrack-Listener",
                    "Start",
                    REG_DWORD,
                    0,
                ),
                ValueEntry(
                    HKLM,
                    r"SYSTEM\CurrentControlSet\Control\WMI\AutoLogger\SQMLogger",
                    "Start",
                    REG_DWORD,
                    0,
                ),
            ),
            "feedback_on_write": (
                # Disable feedback on write
                ValueEntry(HKLM, r"SOFTWARE\Microsoft\Input\TIPC", "Enabled", REG_DWORD, 0),
                ValueEntry(HKCU, r"SOFTWARE\Microsoft\Input\TIPC", "Enabled", REG_DWORD, 0),
            ),
            "loggers": (
                # Disable loggers
                ValueEntry(
                    HKLM,
                    r"SYSTEM\ControlSet001\Control\WMI\AutoLogger\AutoLogger-Diagtrack-Listener",
                    "Start",
                    REG_DWORD,
                    0,
                ),
                ValueEntry(
                    HKLM,
                    r"SYSTEM\CurrentControlSet\Control\WMI\AutoLogger\AutoLogger-Diagtrack-Listener",
                    "Start",
                    REG_DWORD,
                    0,
                ),
                ValueEntry(
                    HKLM,
                    r"SYSTEM\CurrentControlSet\Control\WMI\AutoLogger\SQMLogger",
                    "Start",
                    REG_DWORD,
                    0,
                ),
            ),
            "inventory_collector": (
                # Disable Inventory Collector
                ValueEntry(
                    HKLM,
                    r"SOFTWARE\Policies\Microsoft\Windows\AppCompat",
                    "DisableInventory",
                    REG_DWORD,
                    1,
                ),
            ),
        },
        "customer_experience_improvement_program": (
            # Disable Windows Customer Experience Improvement Program
            ValueEntry(
                HKLM,
                r"SOFTWARE\Policies\Microsoft\SQMClient\Windows",
                "CEIPEnable",
                REG_DWORD,
                0,
            ),
            ValueEntry(
                HKLM,
                r"SOFTWARE\Policies\Microsoft\SQMClient",
                "CorporateSQMURL",
                REG_SZ,
                "0.0.0.0",
            ),
        ),
        "windows_feedback": (
            # Disable Windows Feedback
            ValueEntry(
                HKCU, r"SOFTWARE\Microsoft\Siuf\Rules", "NumberOfSIUFInPeriod", REG_DWORD, 0
            ),
            ValueEntry(
                HKCU, r"SOFTWARE\Microsoft\Siuf\Rules", "PeriodInNanoSeconds", REG_DWORD, 0
            ),
            ValueEntry(
                HKLM,
                r"SOFTWARE\Policies\Microsoft\Windows\DataCollection",
                "DoNotShowFeedbackNotifications",
                REG_DWORD,
                1,
            ),
        ),
        "microsoft_help_feedback": (
            # Disable Microsoft Help Feedback
            ValueEntry(
                HKCU,
                r"SOFTWARE\Policies\Microsoft\Assistance\Client\1.0",
                "NoImplicitFeedback",
                REG_DWORD,
                1,
            ),
            ValueEntry(
                HKCU,
                r"SOFTWARE\Policies\Microsoft\Assistance\Client\1.0",
                "NoExplicitFeedback",
                REG_DWORD,
                1,
            ),
        ),
        "advertising_id": (
            # Disable Advertising ID
            ValueEntry(
                HKLM,
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\AdvertisingInfo",
                "Enabled",
                REG_DWORD,
                0,
            ),
            ValueEntry(
                HKCU,
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\AdvertisingInfo",
                "Enabled",
                REG_DWORD,
                0,
            ),
            ValueEntry(
                HKLM,
                r"SOFTWARE\Policies\Microsoft\Windows\AdvertisingInfo",
                "DisabledByGroupPolicy",
                REG_DWORD,
                1,
            ),
        ),
        "browser_access_to_local_language": (
            # Disable browser access to local language
            ValueEntry(
                HKCU,
                r"Control Panel\International\User Profile",
                "HttpAcceptLanguageOptOut",
                REG_DWORD,
                1,
            ),
        ),
    }
}


