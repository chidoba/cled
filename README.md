![Docker Build Status](https://img.shields.io/docker/build/chidoba/cled)

# cled

cled is a service that allows you to change leds connected to a raspberry pi and print to thermal printers connected to it.

### Running the container

```shell
docker run \
  --privileged \
  --network=host \
  --restart=always \
  --name cled -d \
  -e VENDOR_ID=0x0416 \
  -e DEVICE_ID=0x5011 \
  -e ENDPOINT=1 \
  chidoba/cled
```