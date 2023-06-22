#sudo docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7 -t solarmonitor .

sudo apt install -y podman buildah qemu-user-static
podman build --log-level debug --platform linux/arm64/v8 --platform linux/amd64 --manifest ghcr.io/robertdiers/solar-monitor:0.1 .
podman manifest inspect ghcr.io/robertdiers/solar-monitor:0.1
podman images
podman manifest push ghcr.io/robertdiers/solar-monitor:0.1 ghcr.io/robertdiers/solar-monitor:0.1