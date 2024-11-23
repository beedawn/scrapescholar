@echo off
setlocal enabledelayedexpansion

set filepath=.env
set dockerfilepath=.dockerenv
set next_js_env=.next_env


echo Welcome to the scripted setup
echo Setting up backend env file


set /p sciencedirect_apikey=Enter Science Direct API Key, the key can be obtained here: https://dev.elsevier.com/ :
echo SCIENCEDIRECT_APIKEY=%sciencedirect_apikey% > "%filepath%"
echo SCIENCEDIRECT_APIKEY=%sciencedirect_apikey% > "%dockerfilepath%"

set /p scopus_inst_response=Do you have a scopus institutional key obtained from scopus support? (If you don't know what this is the answer is N) Y/N?:
if /i "%scopus_inst_response%"=="Y" (
    set /p scopus_inst_key=Enter Scopus institutional key:
    echo SCOPUS_INSTTOKEN=%scopus_inst_key% >> "%filepath%"
    echo SCOPUS_INSTTOKEN=%scopus_inst_key% >> "%dockerfilepath%"
)

set /p scopus_apikey=Enter Scopus API Key, the key can be found at https://dev.elsevier.com/ :
echo SCOPUS_APIKEY=%scopus_apikey% >> "%filepath%"
echo SCOPUS_APIKEY=%scopus_apikey% >> "%dockerfilepath%"


set /p postgres_user=Enter postgres username:
echo POSTGRES_USER=%postgres_user% >> "%filepath%"
echo POSTGRES_USER=%postgres_user% >> "%dockerfilepath%"

set /p postgres_pass=Enter postgres password:
echo POSTGRES_PASSWORD=%postgres_pass% >> "%filepath%"
echo POSTGRES_PASSWORD=%postgres_pass% >> "%dockerfilepath%"

set /p postgres_db=Enter postgres db name:
echo POSTGRES_DB=%postgres_db% >> "%filepath%"
echo POSTGRES_DB=%postgres_db% >> "%dockerfilepath%"

set /p postgres_ip=Enter postgres server IP:
echo POSTGRES_SERVER=%postgres_ip% >> "%filepath%"
echo POSTGRES_SERVER=%postgres_ip% >> "%dockerfilepath%"

set /p postgres_port=Enter postgres server Port:
echo POSTGRES_PORT=%postgres_port% >> "%filepath%"
echo POSTGRES_PORT=%postgres_port% >> "%dockerfilepath%"

echo DATABASE_URL=postgresql://%postgres_user%:%postgres_pass%@db:%postgres_port%/%postgres_db% >> "%dockerfilepath%"

set /p secret_key=Enter Secret Key:
echo SECRET_KEY=%secret_key% >> "%filepath%"
echo SECRET_KEY=%secret_key% >> "%dockerfilepath%"

set /p encryption_key=Enter Encryption Key:
echo ENCRYPTION_KEY=%encryption_key% >> "%filepath%"
echo ENCRYPTION_KEY=%encryption_key% >> "%dockerfilepath%"

set /p thesaurus_apikey=Enter Merriam Webster Collegiate Thesaurus API Key, can be found here https://dictionaryapi.com/products/api-collegiate-thesaurus :
echo THESAURUS_APIKEY=%thesaurus_apikey% >> "%filepath%"
echo THESAURUS_APIKEY=%thesaurus_apikey% >> "%dockerfilepath%"

set /p admin_user=Enter initial admin user:
echo TEST_USER=%admin_user% >> "%filepath%"
echo TEST_USER=%admin_user% >> "%dockerfilepath%"

set /p admin_pass=Enter initial admin password:
echo TEST_PASSWORD=%admin_pass% >> "%filepath%"
echo TEST_PASSWORD=%admin_pass% >> "%dockerfilepath%"

set /p host_ip=Enter IP/domain the application will be served from:
echo HOST_IP=%host_ip% >> "%filepath%"
echo HOST_IP=%host_ip% >> "%dockerfilepath%"
echo NEXT_PUBLIC_HOST_IP=%host_ip% >> "%next_js_env%"

echo ENVIRONMENT=PRODUCTION >> "%filepath%"
echo ENVIRONMENT=PRODUCTION >> "%dockerfilepath%"
echo NEXT_PUBLIC_ENVIRONMENT=PRODUCTION >> "%next_js_env%"


if "%host_ip%"=="localhost" (
    echo Running cert gen
    call .\cert_install\cert_gen.bat
) else (
    echo localhost not detected as IP, if serving locally, rerun script with localhost as the IP/domain the application will be served from.
    echo If serving publicly, go to nginx directory, run docker compose up -d and then run ssl_generation_run_from_virtualmachine.bat
)

endlocal
pause
