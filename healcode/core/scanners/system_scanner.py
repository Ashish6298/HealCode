"""
HealCode System Scanner
Scans host system diagnostics, hardware details, memory, disk, network, and configuration.
"""

import os
import sys
import platform
import socket
import shutil
import time
import locale
import subprocess
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

from healcode.core.interfaces import IScanner
from healcode.config.models import ProjectConfig
from healcode.utils.os_detector import get_os_info

class SystemScanner(IScanner):
    @property
    def name(self) -> str:
        return "system-scanner"

    @property
    def is_global(self) -> bool:
        return True

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def description(self) -> str:
        return "Diagnostics scanner for host system, memory, CPU, disk, network, and environment details."

    def __init__(self) -> None:
        self._findings: Optional[List[Dict[str, Any]]] = None

    def initialize(self, config: ProjectConfig) -> None:
        pass

    def scan(self, target_path: str) -> List[Dict[str, Any]]:
        if self._findings is not None:
            return self._findings

        # System scanner runs globally on the host rather than per-file.
        # We only run it once when targeted. We'll return findings as empty list or status if no issues,
        # but the diagnostic info is gathered and placed into metadata.
        # Since this scanner is executing, we'll return any environment warnings.
        findings: List[Dict[str, Any]] = []

        sys_info = self.collect_system_info()
        
        # Check Memory usage threshold
        mem = sys_info.get("memory", {})
        percent_used = mem.get("percent_used", 0)
        if percent_used > 90:
            findings.append({
                "id": "SYS-MEM-HIGH",
                "scanner": self.name,
                "file": "system",
                "line": 0,
                "severity": "WARN",
                "message": f"High memory usage detected: {percent_used}%",
                "fix_suggested": "Close memory-heavy applications or increase RAM."
            })

        # Check Disk usage threshold
        for disk in sys_info.get("disks", []):
            pct = disk.get("percent_used", 0)
            if pct > 90:
                findings.append({
                    "id": "SYS-DISK-HIGH",
                    "scanner": self.name,
                    "file": f"disk:{disk.get('mount', '')}",
                    "line": 0,
                    "severity": "WARN",
                    "message": f"High disk usage on {disk.get('mount')}: {pct}%",
                    "fix_suggested": "Clean up temporary files or free up disk space."
                })

        # Check Internet connectivity
        if not sys_info.get("network", {}).get("internet_connected", False):
            findings.append({
                "id": "SYS-NET-OFFLINE",
                "scanner": self.name,
                "file": "network",
                "line": 0,
                "severity": "ERROR",
                "message": "No internet connection detected.",
                "fix_suggested": "Verify your network interface card status and internet gateway connection."
            })

        self._findings = findings
        return findings

    def collect_system_info(self) -> Dict[str, Any]:
        os_info = get_os_info()
        
        info = {
            "os": os_info.to_dict(),
            "kernel": platform.release(),
            "hostname": socket.gethostname(),
            "user": os.getlogin() if hasattr(os, "getlogin") else os.environ.get("USERNAME", os.environ.get("USER", "unknown")),
            "timezone": str(datetime.now().astimezone().tzinfo),
            "locale": (locale.getlocale()[0] or "unknown") if hasattr(locale, "getlocale") else "unknown",
            "uptime": self._get_uptime(),
            "virtualization": self._detect_virtualization(os_info),
            "cpu": self._get_cpu_info(os_info),
            "memory": self._get_memory_info(os_info),
            "disks": self._get_disk_info(),
            "network": self._get_network_info(),
            "shell": self._detect_shell()
        }
        return info

    def _get_uptime(self) -> float:
        """Returns uptime in seconds."""
        try:
            if sys.platform == "win32":
                # Use ctypes to query GetTickCount64
                import ctypes
                lib = ctypes.windll.kernel32
                tick = lib.GetTickCount64()
                return tick / 1000.0
            else:
                with open("/proc/uptime", "r", encoding="utf-8") as f:
                    return float(f.read().split()[0])
        except Exception:
            return 0.0

    def _detect_virtualization(self, os_info: Any) -> str:
        if os_info.is_wsl:
            return "WSL"
        # Simple detection heuristics
        try:
            if sys.platform == "win32":
                # Check systeminfo manufacturer/model via wmic or systeminfo
                out = subprocess.check_output("wmic computersystem get model", shell=True, stderr=subprocess.DEVNULL).decode().lower()
                for v in ["virtualbox", "vmware", "hyper-v", "kvm", "qemu"]:
                    if v in out:
                        return v.upper()
            else:
                # Check dmesg or systemd-detect-virt
                try:
                    out = subprocess.check_output("systemd-detect-virt", shell=True, stderr=subprocess.DEVNULL).decode().strip().lower()
                    if out and out != "none":
                        return out.upper()
                except Exception:
                    pass
        except Exception:
            pass
        return "PHYSICAL"

    def _get_cpu_info(self, os_info: Any) -> Dict[str, Any]:
        info = {
            "model": platform.processor() or "unknown",
            "cores_physical": os.cpu_count() or 1,
            "cores_logical": os.cpu_count() or 1,
            "frequency_mhz": 0.0
        }
        
        # Read friendly CPU name / frequency on Windows / Linux
        try:
            if os_info.is_windows:
                import winreg
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\CentralProcessor\0")
                model, _ = winreg.QueryValueEx(key, "ProcessorNameString")
                mhz, _ = winreg.QueryValueEx(key, "~MHz")
                info["model"] = str(model).strip()
                info["frequency_mhz"] = float(mhz)
            elif os_info.is_linux:
                with open("/proc/cpuinfo", "r", encoding="utf-8") as f:
                    for line in f:
                        if "model name" in line:
                            info["model"] = line.split(":")[1].strip()
                        elif "cpu MHz" in line:
                            info["frequency_mhz"] = float(line.split(":")[1].strip())
        except Exception:
            pass
        return info

    def _get_memory_info(self, os_info: Any) -> Dict[str, Any]:
        info = {"total": 0, "available": 0, "used": 0, "percent_used": 0.0}
        try:
            if os_info.is_windows:
                import ctypes
                class MEMORYSTATUSEX(ctypes.Structure):
                    _fields_ = [
                        ("dwLength", ctypes.c_ulong),
                        ("dwMemoryLoad", ctypes.c_ulong),
                        ("ullTotalPhys", ctypes.c_ulonglong),
                        ("ullAvailPhys", ctypes.c_ulonglong),
                        ("ullTotalPageFile", ctypes.c_ulonglong),
                        ("ullAvailPageFile", ctypes.c_ulonglong),
                        ("ullTotalVirtual", ctypes.c_ulonglong),
                        ("ullAvailVirtual", ctypes.c_ulonglong),
                        ("ullAvailExtendedVirtual", ctypes.c_ulonglong)
                    ]
                stat = MEMORYSTATUSEX()
                stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
                ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
                info["total"] = stat.ullTotalPhys
                info["available"] = stat.ullAvailPhys
                info["used"] = stat.ullTotalPhys - stat.ullAvailPhys
                info["percent_used"] = float(stat.dwMemoryLoad)
            elif os_info.is_linux:
                meminfo = {}
                with open("/proc/meminfo", "r", encoding="utf-8") as f:
                    for line in f:
                        parts = line.split(":")
                        if len(parts) == 2:
                            meminfo[parts[0].strip()] = int(parts[1].split()[0]) * 1024
                total = meminfo.get("MemTotal", 0)
                free = meminfo.get("MemFree", 0)
                cached = meminfo.get("Cached", 0)
                buffers = meminfo.get("Buffers", 0)
                available = free + cached + buffers
                info["total"] = total
                info["available"] = available
                info["used"] = total - available
                info["percent_used"] = round(((total - available) / total) * 100, 2) if total > 0 else 0.0
            else:
                # Fallback via shutil disk/memory approximation or default
                info["total"] = 8 * 1024 * 1024 * 1024  # 8GB placeholder
        except Exception:
            pass
        return info

    def _get_disk_info(self) -> List[Dict[str, Any]]:
        disks = []
        try:
            # Check default system disk
            path = "C:\\" if sys.platform == "win32" else "/"
            usage = shutil.disk_usage(path)
            disks.append({
                "mount": path,
                "total": usage.total,
                "available": usage.free,
                "used": usage.used,
                "percent_used": round((usage.used / usage.total) * 100, 2) if usage.total > 0 else 0.0,
                "fstype": "NTFS" if sys.platform == "win32" else "ext4"
            })
        except Exception:
            pass
        return disks

    def _get_network_info(self) -> Dict[str, Any]:
        net: Dict[str, Any] = {
            "interfaces": [],
            "internet_connected": False,
            "dns_servers": []
        }
        try:
            # Check basic internet connectivity
            socket.setdefaulttimeout(2)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("8.8.8.8", 53))
            net["internet_connected"] = True
            s.close()
        except Exception:
            pass
        
        # Get active IP address
        try:
            hostname = socket.gethostname()
            ip_addr = socket.gethostbyname(hostname)
            net["interfaces"].append({"name": "primary", "ip": ip_addr})
        except Exception:
            pass
            
        return net

    def _detect_shell(self) -> str:
        # Detect active parent shell
        parent_process_env = os.environ.get("SHELL", "")
        if parent_process_env:
            return os.path.basename(parent_process_env)
        if sys.platform == "win32":
            if "PSModulePath" in os.environ:
                return "powershell"
            return "cmd"
        return "sh"
