echo 'please create testenv file with your environment variables like passwords and users'
sudo podman build --tag test .
sudo podman run --env-file ./testenv test