@echo off
setlocal enabledelayedexpansion

docker ps -q -f name=nginx > nul
if %ERRORLEVEL% neq 0 (
    echo Nginx is not running, please run docker compose up -d from the nginx directory and try again.
    exit /b 1
)

set /p server_name=Enter domain name (e.g., google.com, no www): 

docker-compose run --rm certbot certonly --webroot --webroot-path /var/www/certbot -d %server_name% -d www.%server_name%

if %ERRORLEVEL% equ 0 (
    echo Dry run successful. Proceeding to obtain the certificate.
    docker-compose run --rm certbot certonly --webroot --webroot-path /var/www/certbot -d %server_name%
) else (
    echo Dry run failed. Please check the logs for more details.
)

rem End script
pause
endlocal
