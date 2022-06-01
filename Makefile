.PHONY: pretty update-maipy-image


pretty:
	isort
	black .

update-maipy-image:
	kubectl delete --ignore-not-found -f ./deployments/consumer.yml && \
	kubectl delete --ignore-not-found -f ./deployments/publisher-cron.yml && \
	minikube image unload registry.melior.ai/maipy:0.3.6 && \
	bash ./scripts/build-docker.sh 0.3.6 && \
	minikube image load registry.melior.ai/maipy:0.3.6 && \
	kubectl apply -f ./deployments/consumer.yml && \
	kubectl apply -f ./deployments/publisher-cron.yml
