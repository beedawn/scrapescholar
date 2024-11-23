@echo off
setlocal enabledelayedexpansion

set server_name=localhost

set SSL_DIR=certs\%server_name%

set KEY_FILE=%SSL_DIR%\privkey.pem
set CRT_FILE=%SSL_DIR%\fullchain.pem

if not exist "%SSL_DIR%" (
    mkdir "%SSL_DIR%"
)

echo Generating private key...
openssl genpkey -algorithm RSA -out "%KEY_FILE%"
if %errorlevel% neq 0 (
    echo Error generating private key.
    exit /b 1
)

echo Generating CSR...
openssl req -new -key "%KEY_FILE%" -out "%SSL_DIR%\localhost.csr" -subj "/C=US/ST=Pennsylvania/L=Pittsburgh/O=ScrapeScholar/CN=%server_name%"
if %errorlevel% neq 0 (
    echo Error generating CSR.
    exit /b 1
)

echo Generating self-signed certificate...
openssl x509 -req -in "%SSL_DIR%\localhost.csr" -signkey "%KEY_FILE%" -out "%CRT_FILE%" -days 365
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
