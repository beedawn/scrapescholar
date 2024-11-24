# Database Backup Script

This script generates a backup of a PostgreSQL database running in a Docker container, saves the backup locally, and removes the temporary backup file from the container.

## Script Usage

Run the script with the required parameters or allow the script to prompt for them interactively.

### Parameters

| Parameter          | Description                                                                                 | Required | Example                                      |
|--------------------|---------------------------------------------------------------------------------------------|----------|----------------------------------------------|
| `ContainerName`    | The name of the Docker container running the database.                                       | Yes      | `container_scrapescholardb`                 |
| `DBUser`           | The username for the PostgreSQL database.                                                   | Yes      | `student`                                    |
| `DBName`           | The name of the PostgreSQL database to back up.                                             | Yes      | `scrapescholartestdb`                        |
| `DBPassword`       | The password for the PostgreSQL database user.                                              | Yes      | `student`                                    |
| `LocalBackupPath`  | The local file path where the database backup should be saved.                              | Yes      | `C:\Backups\db_backup.sql`                   |

### Example with params

```powershell
.\GenerateAndCopyDBBackup.ps1 -ContainerName "container_scrapescholardb" -DBUser "student" -DBName "scrapescholartestdb" -DBPassword "student" -LocalBackupPath "C:\Backups\db_backup.sql"