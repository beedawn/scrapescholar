param (
    [string]$ContainerName,  # Name of the Docker container
    [string]$DBUser,         # Database user
    [string]$DBName,         # Database name
    [string]$DBPassword,     # Database password
    [string]$LocalBackupPath # Local path to save the backup file
)

# Prompt for missing parameters
if (-not $ContainerName) {
    $ContainerName = Read-Host "Enter the Docker container name (e.g., container_scrapescholardb)"
}
if (-not $DBUser) {
    $DBUser = Read-Host "Enter the database user (e.g., student)"
}
if (-not $DBName) {
    $DBName = Read-Host "Enter the database name (e.g., scrapescholartestdb)"
}
if (-not $DBPassword) {
    $DBPassword = Read-Host -Prompt "Enter the database password (e.g., student)" -AsSecureString
    $DBPassword = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($DBPassword))
}
if (-not $LocalBackupPath) {
    $LocalBackupPath = Read-Host "Enter the local path to save the backup file (e.g., C:\Backups\db_backup.sql)"
}

# Generate a temporary backup file name inside the container
$BackupFileName = "/tmp/db_backup.sql"

# Step 1: Generate the backup inside the Docker container
Write-Host "Generating database backup in the container $ContainerName..."
$EnvVars = @{"PGPASSWORD" = $DBPassword}
docker exec -e PGPASSWORD=$DBPassword $ContainerName pg_dump -U $DBUser -Fp $DBName -f $BackupFileName

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to generate the database backup." -ForegroundColor Red
    exit 1
}

Write-Host "Database backup generated in container at $BackupFileName."

# Step 2: Copy the backup file from the container to the local machine
Write-Host "Copying the backup file from the container to $LocalBackupPath..."
docker cp "$ContainerName:$BackupFileName" $LocalBackupPath

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to copy the backup file from the container." -ForegroundColor Red
    exit 1
}

Write-Host "Backup file copied to $LocalBackupPath successfully." -ForegroundColor Green

# Step 3: Clean up the temporary backup file inside the container
Write-Host "Removing temporary backup file from the container..."
docker exec $ContainerName rm $BackupFileName

if ($LASTEXITCODE -ne 0) {
    Write-Host "Warning: Failed to remove the temporary backup file from the container." -ForegroundColor Yellow
} else {
    Write-Host "Temporary backup file removed from the container."
}

# Completion message
Write-Host "Database backup process completed successfully!" -ForegroundColor Green