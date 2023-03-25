echo 'please create testenv file with your environment variables like passwords and users'
sudo docker build --tag test .
sudo docker run --env-file ./testenv test