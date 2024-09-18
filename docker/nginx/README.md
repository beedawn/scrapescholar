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
docker restart <container_id>


After this, your site should be accessible via https

To renew the cert you can run the renew_cert.sh script

Additional Security Steps

Also while you are working with the infrastructure, it is advisable to disable the root account and set up a sudo user

For ubuntu this can be followed by following the steps here to create a sudo user:
https://www.digitalocean.com/community/tutorials/how-to-create-a-new-sudo-enabled-user-on-ubuntu

We will provide a short synopsis of this in the event the link no longer works, first connect to the server as root via ssh

then run the following script, ideally enter in a randomly generated or hard to guess username
```bash
adduser <username>
```

Then provide a complex randomly generated password and complete the remaining prompts if needed

then run
```bash
usermod -aG sudo <username>
```
Then switch to the account you just created
```bash
su <username>
```

You will be prompted for the user's password then test to ensure it has root access with
```bash
sudo ls -la /root
```

This command should work and list all files in root, if it does not you may need to check your linux distributions documentation on how to perform these steps.

Then you will need to configure an ssh key to connect to the server with the new account
some instructions are provided here:
https://www.cloudpanel.io/tutorial/set-up-ssh-keys-on-ubuntu-20-04/#:~:text=To%20enable%20SSH%20on%20Ubuntu,when%20the%20system%20boots%20up.&text=It%20shows%20the%20local%20computer,then%20press%20ENTER%20to%20continue.

We will provide a brief synopsis of the steps

Generate an ssh-key on your machine (MacOS/Linux) with the command
```bash
ssh-keygen
```
This will ask you where you'd like to save the file, and if you'd like a password associated with the key(recommended)

Then you will need to copy the key to the ~/.ssh/authorized_keys file on the virtual machine. If this file does not exist, you will need to create it, when logged into your new user account you can use
```bash
touch ~/.ssh/authorized_keys
```

Once this is created, then you can use the scp command to transfer the public key from your machine to the virtual machine with
```bash
scp -i /<path_to_root_ssh_key>/id_ed25519 -r /<path_to_where_you_saved_the_newly_generated_key>.pub root@<virtualmachine_ip>:/home/<new_username>/.ssh/
```

Once this is copied, you can then run this command, to append the key to the authorized keys file
```bash
cat <name_of_key>.pub >> authorized_keys
```
Then you will need to edit the sshd_config file:
```bash
sudo nano /etc/ssh/sshd_config
```
and find the line that has:
```
#PasswordAuthentication yes
```
remove the #, and change yes to no:
```
PasswordAuthentication no
```
then run
```bash
sudo systemctl restart ssh
```

Now open a separate terminal window to test the new user connection with
```bash
ssh -i /<path_to_private_key> <username>@<virtual_machine_ip>
```

This should work and let you sign in as the new user, in the event it does not, do not proceed past this step and troubleshoot this, otherwise if you continue, you will lock yourself out of the virtual machine.


The last step is to disable the login for the root user.
Some steps are provided here:
https://www.digitalocean.com/community/tutorials/how-to-disable-root-login-on-ubuntu-20-04

Run this command to edit the sshd_config file again
```bash
sudo nano  /etc/ssh/sshd_config
```

Find the line with:
```
PermitRootLogin yes
```
And change yes to no:
```
PermitRootLogin no
```

Save with ctrl+x and hit y and confirm

Then run: 
```bash
sudo systemctl restart ssh
```

Now if you try to connect via ssh with the root account and proper key, it should deny access to you. And you should only be able to login with the newly generated username and ssh key made in this guide.