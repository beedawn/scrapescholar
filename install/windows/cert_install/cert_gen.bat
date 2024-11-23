@echo off
setlocal enabledelayedexpansion

SET OPENSSL_VERSION=Win64OpenSSL-3_0_0
SET DOWNLOAD_URL=https://slproweb.com/download/Win64OpenSSL_Light-3_4_0.exe
SET INSTALL_DIR=C:\Program Files\OpenSSL
SET OPENSSL_BIN=%INSTALL_DIR%\bin
if exist "%INSTALL_DIR%\bin\openssl.exe" (
    echo OpenSSL is installed.
    
    set OPEN_SSL_EXE="%INSTALL_DIR%\bin\openssl.exe"
    "%OPEN_SSL_EXE%" version
    goto InstallCompleted
)

echo Downloading OpenSSL installer...this will take a while, go grab a coffee.
powershell -Command "Invoke-WebRequest -Uri %DOWNLOAD_URL% -OutFile OpenSSL-installer.exe"

echo Running installer...
start /wait OpenSSL-installer.exe /silent /dir="%INSTALL_DIR%"

@REM echo Adding OpenSSL to the PATH environment variable...
@REM setx PATH "%PATH%;%INSTALL_DIR%\bin"

@REM set PATH=%PATH%;%OPENSSL_BIN%

echo Installation complete. Verifying OpenSSL installation...
set OPEN_SSL_EXE=%INSTALL_DIR%\bin\openssl.exe
"%OPEN_SSL_EXE%" version

echo OpenSSL installed and configured successfully.
set OPEN_SSL_EXE="%INSTALL_DIR%\bin\openssl.exe"
del /f /q OpenSSL-installer.exe

:InstallCompleted
set server_name=localhost

set SSL_DIR=certs\%server_name%

set KEY_FILE=%SSL_DIR%\privkey.pem
set CRT_FILE=%SSL_DIR%\fullchain.pem

if not exist "%SSL_DIR%" (
    mkdir "%SSL_DIR%"
)

echo Generating private key...
%OPEN_SSL_EXE% genpkey -algorithm RSA -out "%KEY_FILE%"
if %errorlevel% neq 0 (
    echo Error generating private key.
    exit /b 1
)

echo Generating CSR...
%OPEN_SSL_EXE% req -new -key "%KEY_FILE%" -out "%SSL_DIR%\localhost.csr" -subj "/C=US/ST=Pennsylvania/L=Pittsburgh/O=ScrapeScholar/CN=%server_name%"
if %errorlevel% neq 0 (
    echo Error generating CSR.
    exit /b 1
)

echo Generating self-signed certificate...
%OPEN_SSL_EXE% x509 -req -in "%SSL_DIR%\localhost.csr" -signkey "%KEY_FILE%" -out "%CRT_FILE%" -days 365
if %errorlevel% neq 0 (
    echo Error generating certificate.
    exit /b 1
)

echo Self-signed certificate and private key generated successfully!
echo Files generated:
echo   Private Key: %KEY_FILE%
echo   Certificate: %CRT_FILE%

echo Moving certificates to Nginx directory...
mkdir ..\..\..\scrapescholar_docker\nginx_nextjs\certbot\conf\live
mkdir ..\..\..\scrapescholar_docker\nginx_nextjs\certbot\conf\live\%server_name%
move "%SSL_DIR%\fullchain.pem" ..\..\..\scrapescholar_docker\nginx_nextjs\certbot\conf\live\%server_name%\fullchain.pem
move "%SSL_DIR%\privkey.pem" ..\..\..\scrapescholar_docker\nginx_nextjs\certbot\conf\live\%server_name%\privkey.pem

rd /s /q certs

endlocal
pause
