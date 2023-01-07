minikube start
minikube addons enable ingress
# kubectl get deployment
# kubectl get pod
# kubectl get service
# kubectl get ingress
kubectl create -f kubes_api_deployment.yml
kubectl create -f kubes_service.yml
kubectl create -f kubes_ingress.yml
# ssh -i "data_enginering_machine.pem" ubuntu@63.34.169.16 -fNL 8000:192.168.49.2:80
# kubectl rollout restart deployment bearing-pyventive-deployment
# kubectl create secret generic my-secret --from-literal db-pass=datascientest1234