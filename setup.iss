[Setup]
; this code was used to make the program installer. The comments will be in Portuguese because we at Leopardus Team are Brazilians.
AppName=Jasper Retro Converter
AppVersion=3.0
DefaultDirName={commonpf}\Jasper Retro Converter
DefaultGroupName=Jasper Retro Converter
OutputDir=.\Output
OutputBaseFilename=Jaspersetup
Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin


[Files]
; Adiciona o executável gerado pelo PyInstaller
Source: "jasper.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "icon.png"; DestDir: "{app}"; Flags: ignoreversion
Source: "jrc.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Cria um atalho no menu iniciar
Name: "{group}\Jasper Retro Converter"; Filename: "{app}\jasper.exe"

[Run]
; Define o executável a ser executado após a instalação
Filename: "{app}\jasper.exe"; Description: "Iniciar Jasper Retro Converter"; Flags: nowait postinstall skipifsilent

[Registry]
; Associa o ícone aos arquivos .jrc
Root: HKCR; Subkey: ".jrc"; ValueType: string; ValueData: "Jasper Retro Converter"
Root: HKCR; Subkey: "Jasper Retro Converter"; ValueType: string; ValueData: "Arquivo de estilos do Jasper Retro Converter"
Root: HKCR; Subkey: "Jasper Retro Converter\DefaultIcon"; ValueType: string; ValueData: "{app}\jrc.ico"
Root: HKCR; Subkey: "Jasper Retro Converter\shell\open\command"; ValueType: string; ValueData: """{app}\jasper.exe"" ""%1"""
