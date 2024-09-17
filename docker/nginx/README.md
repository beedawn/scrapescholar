To configure this docker container, you need to set the domain name in docker-compose.yml on line 19.

Then copy these files to your virtual machine.

Once this is done navigate to the nginx folder, and run 
```bash
docker compose up -d
```

Then 
```bash
chmod +x ssl_generation_run_from_virtualmachine.sh
```

This script checks if the nginx docker container is running, and then gets certificates and stores them in the certbot/conf folder

After completion of this script, restart the nginx server which will trigger the start_nginx.sh script which has two different nginx templates configured to run depending on if certs are located in that folder for that domain.

After this, your site should be accessible via https