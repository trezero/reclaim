"""Drive scanner for detecting and analyzing storage devices."""

import psutil
from pathlib import Path
from typing import List, Dict, Any
from app.models import Drive, DriveStatus, SpaceConsumer, ConsumerType
import os


class DriveScanner:
    """Scans and analyzes drive information."""

    @staticmethod
    def get_all_drives() -> List[Drive]:
        """Get information about all NTFS drives."""
        drives = []

        for partition in psutil.disk_partitions():
            # Only process NTFS drives on Windows
            if partition.fstype != "NTFS":
                continue

            try:
                usage = psutil.disk_usage(partition.mountpoint)
                letter = partition.device.replace(":\\", "").replace(":", "")

                percent_used = (usage.used / usage.total) * 100

                # Determine status
                if percent_used > 80:
                    status = DriveStatus.CRITICAL
                elif percent_used > 50:
                    status = DriveStatus.WARNING
                else:
                    status = DriveStatus.HEALTHY

                drive = Drive(
                    letter=letter,
                    total_bytes=usage.total,
                    used_bytes=usage.used,
                    free_bytes=usage.free,
                    percent_used=round(percent_used, 2),
                    status=status,
                    filesystem=partition.fstype
                )
                drives.append(drive)
            except PermissionError:
                continue

        return drives

    @staticmethod
    def get_directory_size(path: Path) -> int:
        """Calculate total size of a directory."""
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(path):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    try:
                        total_size += os.path.getsize(filepath)
                    except (OSError, FileNotFoundError):
                        continue
        except (PermissionError, OSError):
            pass
        return total_size

    @staticmethod
    def identify_space_consumers() -> List[SpaceConsumer]:
        """Identify top space consumers across the system."""
        consumers = []
        home = Path.home()

        # Docker Desktop
        docker_path = home / "AppData" / "Local" / "Docker Desktop"
        if docker_path.exists():
            size = DriveScanner.get_directory_size(docker_path)
            if size > 0:
                consumers.append(SpaceConsumer(
                    name="Docker Desktop",
                    path=str(docker_path),
                    size_bytes=size,
                    type=ConsumerType.DOCKER,
                    last_modified=None
                ))

        # WSL distributions
        wsl_base = Path("C:\\Users") / os.getenv("USERNAME", "winadmin") / "AppData" / "Local" / "Packages"
        if wsl_base.exists():
            for item in wsl_base.iterdir():
                if "CanonicalGroupLimited" in item.name or "Ubuntu" in item.name:
                    size = DriveScanner.get_directory_size(item)
                    if size > 1_000_000_000:  # > 1GB
                        consumers.append(SpaceConsumer(
                            name=f"WSL - {item.name[:30]}",
                            path=str(item),
                            size_bytes=size,
                            type=ConsumerType.WSL,
                            last_modified=None
                        ))

        # Downloads folder
        downloads_path = home / "Downloads"
        if downloads_path.exists():
            size = DriveScanner.get_directory_size(downloads_path)
            if size > 0:
                consumers.append(SpaceConsumer(
                    name="Downloads",
                    path=str(downloads_path),
                    size_bytes=size,
                    type=ConsumerType.DOWNLOADS,
                    last_modified=None
                ))

        # Temp files
        temp_paths = [
            Path("C:\\Windows\\Temp"),
            home / "AppData" / "Local" / "Temp"
        ]
        for temp_path in temp_paths:
            if temp_path.exists():
                size = DriveScanner.get_directory_size(temp_path)
                if size > 0:
                    consumers.append(SpaceConsumer(
                        name=f"Temp - {temp_path.name}",
                        path=str(temp_path),
                        size_bytes=size,
                        type=ConsumerType.TEMP,
                        last_modified=None
                    ))

        # Browser caches
        cache_paths = {
            "Chrome Cache": home / "AppData" / "Local" / "Google" / "Chrome" / "User Data" / "Default" / "Cache",
            "Edge Cache": home / "AppData" / "Local" / "Microsoft" / "Edge" / "User Data" / "Default" / "Cache",
        }

        for name, cache_path in cache_paths.items():
            if cache_path.exists():
                size = DriveScanner.get_directory_size(cache_path)
                if size > 0:
                    consumers.append(SpaceConsumer(
                        name=name,
                        path=str(cache_path),
                        size_bytes=size,
                        type=ConsumerType.CACHE,
                        last_modified=None
                    ))

        # Sort by size descending and return top 10
        consumers.sort(key=lambda x: x.size_bytes, reverse=True)
        return consumers[:10]
