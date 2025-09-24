# -*- mode: python ; coding: utf-8 -*-
import platform

block_cipher = None

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
)

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

# Create macOS App Bundle
if platform.system() == 'Darwin':
    app = BUNDLE(
        coll,
        name='Trackonverter.app',
        icon=None,
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