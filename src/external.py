import ctypes
from ctypes.wintypes import *
from consts import *
import psutil


class ModuleEntry32(ctypes.Structure):
       _fields_ = [ ( 'dwSize' , DWORD ) ,
                ( 'th32ModuleID' , DWORD ),
                ( 'th32ProcessID' , DWORD ),
                ( 'GlblcntUsage' , DWORD ),
                ( 'ProccntUsage' , DWORD ) ,
                ( 'modBaseAddr' , ctypes.POINTER(ctypes.c_ulong)) ,
                ( 'modBaseSize' , DWORD ) ,
                ( 'hModule' , HMODULE ) ,
                ( 'szModule' , ctypes.c_char * 256 ),
                ( 'szExePath' , ctypes.c_char * 260 ) ]


class External:
    def __init__(self, procName) -> None:
        self.procName = procName
        self.pid = self.GetProcessIdByName()
        self.kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

        if self.pid != 0:
            self.hProcess = self.kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, self.pid)


    def GetProcessIdByName(self) -> int:
        PID = 0
        for proc in psutil.process_iter():
            if self.procName in proc.name():
                PID = proc.pid
                break

        return PID
    

    def GetModuleBaseAddress(self, PID, ModuleName) -> int:
        BaseAddess = None
        hSnap = self.kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPMODULE | TH32CS_SNAPMODULE32, PID)
        ModuleEntry = ModuleEntry32()
        ModuleEntry.dwSize = ctypes.sizeof(ModuleEntry32)
        base = None

        if self.kernel32.Module32First(hSnap, ctypes.byref(ModuleEntry)):
            if ModuleEntry.szModule.decode("utf-8") == ModuleName:
                BaseAddess = int(hex(ctypes.addressof(ModuleEntry.modBaseAddr.contents)), 16)
        
        while self.kernel32.Module32Next(hSnap, ctypes.byref(ModuleEntry)):
            if ModuleEntry.szModule.decode("utf-8") == ModuleName:
                BaseAddess = int(hex(ctypes.addressof(ModuleEntry.modBaseAddr.contents)), 16)
                break

        self.kernel32.CloseHandle(hSnap)

        if BaseAddess == None:
            raise Exception("Module not found.")

        return BaseAddess
    

    def WriteProcessMemoryEx(self, address, value) -> None:
        self.kernel32.WriteProcessMemory(self.hProcess, LPVOID(address), ctypes.byref(value), ctypes.sizeof(value), 0)
    

    def ReadProcessMemoryEx(self, address, buffer) -> None:
        self.kernel32.ReadProcessMemory(self.hProcess, LPVOID(address), ctypes.byref(buffer), ctypes.sizeof(buffer), 0)

    
    def GetPointerAddress(self, baseAddress, offsets) -> int:
        address = baseAddress

        for offset in offsets:
            value = ctypes.c_int()
            self.ReadProcessMemoryEx(address, value)
            address = value.value + offset

        return address


    