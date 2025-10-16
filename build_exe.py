"""
Build script to create a standalone Windows executable
Run: python build_exe.py
"""

import sys
import os
import shutil
from pathlib import Path

# PyInstaller build spec
SPEC = """
# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules, collect_data_files
import sys
from pathlib import Path

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('ui', 'ui'), ('core', 'core')],
    hiddenimports=['PyQt6'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='WorkspaceOrganizer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico',
)
"""

def build():
    """Build the executable"""
    print("🚀 Building Workspace Organizer executable...")
    print()
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("❌ PyInstaller not found. Installing...")
        os.system(f"{sys.executable} -m pip install pyinstaller")
    
    # Run PyInstaller
    print("📦 Creating executable...")
    os.system(
        f"{sys.executable} -m PyInstaller "
        "--onefile "
        "--windowed "
        "--name WorkspaceOrganizer "
        "--add-data 'ui:ui' "
        "--add-data 'core:core' "
        "--icon=icon.ico "
        "main.py"
    )
    
    print()
    print("✅ Build complete!")
    print()
    print("📍 Your executable is located at:")
    print("   dist/WorkspaceOrganizer.exe")
    print()
    print("💡 Tips:")
    print("   - Copy WorkspaceOrganizer.exe to create a shortcut on your desktop")
    print("   - The app will create a .workspace_organizer folder in your home directory")
    print("   - All your notes and settings will be stored there")


if __name__ == "__main__":
    build()
