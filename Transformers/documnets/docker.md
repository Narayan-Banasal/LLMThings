### Docker things

docker stop $(docker ps -q)
docker rm $(docker ps -aq)
docker rmi $(docker images -q)


Setting of certificate locally for Minikube
1. minikube start --mount --mount-string="/Users/narayan.bansal1/Downloads:/mnt/certificates"
2. minikube ssh
3. sudo cp /mnt/certificates/certi.crt /usr/local/share/ca-certificates
4. sudo update-ca-certificates



kubectl delete deployments.apps --all
kubectl delete services --all
kubectl delete persistentvolumeclaims --all 


// to go into the Minikube’s docker environment for the current shell
eval $(minikube docker-env)


// to run the prometheus after installing from brew and adding the configuration file  prometheus --config.file=/Users/narayan.bansal1/prometheus/prometheus.yml

Configuration file:  global:
  scrape_interval: 2s

scrape_configs:
  - job_name: 'spring-boot'
    metrics_path: '/actuator/prometheus'
    static_configs:
      - targets: ['localhost:8080']