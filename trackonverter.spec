# -*- mode: python ; coding: utf-8 -*-
import platform

block_cipher = None

# Determine icon based on platform
if platform.system() == 'Windows':
    icon_file = 'icon.ico'
elif platform.system() == 'Darwin':
    icon_file = 'icon.icns'
else:
    icon_file = None

a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Platform-specific EXE configuration
if platform.system() == 'Windows':
    # Windows: Single-file executable
    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.zipfiles,
        a.datas,
        [],
        name='trackonverter',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        upx_exclude=[],
        runtime_tmpdir=None,
        console=True,
        disable_windowed_traceback=False,
        argv_emulation=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
        icon=icon_file,
    )
else:
    # macOS and Linux: Directory-based distribution
    exe = EXE(
        pyz,
        a.scripts,
        [],
        exclude_binaries=True,
        name='trackonverter',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        console=True,
        disable_windowed_traceback=False,
        argv_emulation=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
        icon=icon_file,
    )

# Create macOS App Bundle (only for macOS, since Windows now creates a single exe)
if platform.system() == 'Darwin':
    coll = COLLECT(
        exe,
        a.binaries,
        a.zipfiles,
        a.datas,
        strip=False,
        upx=True,
        upx_exclude=[],
        name='trackonverter',
    )
    
    app = BUNDLE(
        coll,
        name='Trackonverter.app',
        icon='icon.icns',
        bundle_identifier='com.trackonverter.app',
        version='1.0.0',
        info_plist={
            'NSHighResolutionCapable': 'True',
            'CFBundleShortVersionString': '1.0.0',
            'CFBundleVersion': '1.0.0',
            'CFBundleExecutable': 'trackonverter',
            'CFBundleName': 'Trackonverter',
            'CFBundleDisplayName': 'Trackonverter',
            'CFBundleIdentifier': 'com.trackonverter.app',
            'CFBundlePackageType': 'APPL',
            'LSApplicationCategoryType': 'public.app-category.utilities',
            'LSBackgroundOnly': False,
        },
    )