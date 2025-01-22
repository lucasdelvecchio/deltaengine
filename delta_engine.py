import time
import ctypes
import platform
from datetime import datetime, timedelta

class DeltaEngine:
    def __init__(self):
        self.start_time = datetime.now()
        self.os_platform = platform.system()

    def synchronize_system_clock(self):
        if self.os_platform != 'Windows':
            raise NotImplementedError("System clock synchronization is only supported on Windows platforms.")
        # This is a placeholder for actual synchronization logic
        print("Synchronizing system clock...")
        time.sleep(1)  # Simulate some processing time
        print("System clock synchronized successfully.")

    def get_current_time(self):
        return datetime.now()

    def set_system_time(self, new_time: datetime):
        if self.os_platform != 'Windows':
            raise NotImplementedError("Setting system time is only supported on Windows platforms.")
        # Adjust the time using Windows API
        print(f"Setting system time to: {new_time}")
        try:
            self._win_set_system_time(new_time)
            print("System time set successfully.")
        except Exception as e:
            print(f"Failed to set system time: {e}")

    def _win_set_system_time(self, new_time: datetime):
        # Prepare the SYSTEMTIME structure
        class SYSTEMTIME(ctypes.Structure):
            _fields_ = [("wYear", ctypes.c_ushort),
                        ("wMonth", ctypes.c_ushort),
                        ("wDayOfWeek", ctypes.c_ushort),
                        ("wDay", ctypes.c_ushort),
                        ("wHour", ctypes.c_ushort),
                        ("wMinute", ctypes.c_ushort),
                        ("wSecond", ctypes.c_ushort),
                        ("wMilliseconds", ctypes.c_ushort)]

        systime = SYSTEMTIME()
        systime.wYear = new_time.year
        systime.wMonth = new_time.month
        systime.wDay = new_time.day
        systime.wHour = new_time.hour
        systime.wMinute = new_time.minute
        systime.wSecond = new_time.second
        systime.wMilliseconds = new_time.microsecond // 1000

        # Call Windows API to set the system time
        if not ctypes.windll.kernel32.SetSystemTime(ctypes.byref(systime)):
            raise ctypes.WinError()

    def add_seconds(self, seconds: int):
        current_time = self.get_current_time()
        new_time = current_time + timedelta(seconds=seconds)
        self.set_system_time(new_time)

    def time_elapsed_since_start(self):
        return datetime.now() - self.start_time

if __name__ == "__main__":
    engine = DeltaEngine()
    print("Current Time:", engine.get_current_time())
    engine.synchronize_system_clock()
    engine.add_seconds(120)  # Add 120 seconds to the current time
    print("Time Elapsed Since Start:", engine.time_elapsed_since_start())