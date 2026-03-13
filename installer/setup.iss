; Script de Inno Setup para Taller Felinormar
; Desarrollado por: Felipe Norberto Marcelino
; Copyright (c) 2026 Felipe Norberto Marcelino. Todos los derechos reservados.

#define MyAppName "Taller Felinormar"
#define MyAppVersion "2.0"
#define MyAppPublisher "Felipe Norberto Marcelino"
#define MyAppURL "https://github.com/FeliNormar/taller_felinormar"
#define MyAppExeName "iniciar_felinormar.bat"

[Setup]
; Información básica
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=..\LICENSE
InfoBeforeFile=installer_info.txt
OutputDir=output
OutputBaseFilename=TallerFelinormar_v2.0_Setup
SetupIconFile=icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
; Archivos de la aplicación
Source: "..\app\*"; DestDir: "{app}\app"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\templates\*"; DestDir: "{app}\templates"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\static\*"; DestDir: "{app}\static"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\docs\*"; DestDir: "{app}\docs"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\scripts\*"; DestDir: "{app}\scripts"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\wsgi.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\requirements.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\README.md"; DestDir: "{app}"; Flags: ignoreversion isreadme
Source: "..\LICENSE"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\Procfile"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\runtime.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\.env.example"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\.gitignore"; DestDir: "{app}"; Flags: ignoreversion
Source: "iniciar_felinormar.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "instalar_dependencias.bat"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\Documentación"; Filename: "{app}\README.md"
Name: "{group}\Licencia"; Filename: "{app}\LICENSE"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\instalar_dependencias.bat"; Description: "Instalar dependencias de Python"; Flags: postinstall runhidden
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
function InitializeSetup(): Boolean;
var
  ResultCode: Integer;
begin
  // Verificar si Python está instalado
  if not RegKeyExists(HKEY_LOCAL_MACHINE, 'SOFTWARE\Python\PythonCore\3.11') and
     not RegKeyExists(HKEY_LOCAL_MACHINE, 'SOFTWARE\Python\PythonCore\3.12') and
     not RegKeyExists(HKEY_CURRENT_USER, 'SOFTWARE\Python\PythonCore\3.11') and
     not RegKeyExists(HKEY_CURRENT_USER, 'SOFTWARE\Python\PythonCore\3.12') then
  begin
    if MsgBox('Python 3.11 o superior no está instalado en su sistema.' + #13#10 + 
              'Es necesario para ejecutar Taller Felinormar.' + #13#10#13#10 +
              '¿Desea abrir la página de descarga de Python?', 
              mbConfirmation, MB_YESNO) = IDYES then
    begin
      ShellExec('open', 'https://www.python.org/downloads/', '', '', SW_SHOW, ewNoWait, ResultCode);
    end;
    Result := False;
  end
  else
    Result := True;
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  ResultCode: Integer;
begin
  if CurStep = ssPostInstall then
  begin
    // Crear carpeta instance si no existe
    if not DirExists(ExpandConstant('{app}\instance')) then
      CreateDir(ExpandConstant('{app}\instance'));
  end;
end;
