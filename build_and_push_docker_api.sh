docker image build . -t bearing_pyventive:1.0.0
docker login --username yann112
# docker image list
docker tag 6facf0c791ae yann112/bearing_pyventive:1.0.0
docker push yann112/bearing_pyventive:1.0.0
# docker-compose -f docker-compose.yml up