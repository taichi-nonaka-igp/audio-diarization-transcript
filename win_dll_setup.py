"""Windows: register FFmpeg shared DLL directories before torchcodec/pyannote load."""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path


def _candidate_ffmpeg_bins() -> list[Path]:
    candidates: list[Path] = []

    env_bin = os.environ.get("FFMPEG_BIN")
    if env_bin:
        candidates.append(Path(env_bin))

    ffmpeg_exe = shutil.which("ffmpeg")
    if ffmpeg_exe:
        candidates.append(Path(ffmpeg_exe).parent)

    local_app_data = os.environ.get("LOCALAPPDATA")
    if local_app_data:
        winget_packages = Path(local_app_data) / "Microsoft" / "WinGet" / "Packages"
        if winget_packages.is_dir():
            for package_dir in winget_packages.glob("BtbN.FFmpeg.GPL.Shared*"):
                for bin_dir in package_dir.glob("*/bin"):
                    if (bin_dir / "avcodec-61.dll").exists() or (
                        bin_dir / "avcodec-60.dll"
                    ).exists():
                        candidates.append(bin_dir)

    for fixed in (Path(r"C:\ffmpeg\bin"), Path(r"C:\ffmpeg\shared\bin")):
        candidates.append(fixed)

    unique: list[Path] = []
    seen: set[Path] = set()
    for path in candidates:
        resolved = path.resolve()
        if resolved not in seen:
            seen.add(resolved)
            unique.append(resolved)
    return unique


def configure_windows_dll_paths() -> Path | None:
    """Add FFmpeg shared DLL directory for torchcodec on Windows."""
    if sys.platform != "win32":
        return None

    for bin_dir in _candidate_ffmpeg_bins():
        if not bin_dir.is_dir():
            continue
        has_ffmpeg = (bin_dir / "ffmpeg.exe").exists() or shutil.which(
            "ffmpeg", path=str(bin_dir)
        )
        has_codec_dll = any(bin_dir.glob("avcodec-*.dll"))
        if not has_ffmpeg or not has_codec_dll:
            continue
        try:
            os.add_dll_directory(str(bin_dir))
            return bin_dir
        except OSError:
            continue

    return None


configure_windows_dll_paths()
