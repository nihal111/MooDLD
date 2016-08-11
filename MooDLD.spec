# -*- mode: python -*-

block_cipher = None


a = Analysis(['MooDLD.py'],
             pathex=['c:\\Python27'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

a.datas += [('moodle.ico', 'C:\\Python27\\moodle.ico', 'DATA')]
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='MooDLD',
          debug=False,
          strip=False,
          upx=True,
          console=False,
          icon='moodle.ico' )
