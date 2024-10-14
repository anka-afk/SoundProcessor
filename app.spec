# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules, collect_dynamic_libs

block_cipher = None

# 收集所有必要的数据文件
datas = []
datas += collect_data_files('vosk')
datas += [('assets', 'assets')]
datas += [('vosk-model-small-cn-0.22', 'vosk-model-small-cn-0.22')]  # Vosk 模型文件夹

# 收集所有必要的隐藏导入
hiddenimports = []
hiddenimports += collect_submodules('vosk')
hiddenimports += ['pyqtgraph.graphicsItems.ViewBox.axisCtrlTemplate_pyqt6',
                  'pyqtgraph.graphicsItems.PlotItem.plotConfigTemplate_pyqt6',
                  'pyqtgraph.imageview.ImageViewTemplate_pyqt6']

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
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

binaries = []
binaries += collect_dynamic_libs('PyQt6')

exe = EXE(
    pyz,
    a.scripts,
    a.binaries + binaries,
    a.zipfiles,
    a.datas,
    [],
    name='语音分析识别系统',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico',
)
