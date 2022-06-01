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

clean:
	find . -type d \( -path ./front -o -path ./.venv \) -prune -o -name '*.pyc' -exec rm -f {} +
	find . -type d \( -path ./front -o -path ./.venv \) -prune -o -name '*.pyo' -exec rm -f {} +
	find . -type d \( -path ./front -o -path ./.venv \) -prune -o -name '*~' -exec rm -f  {} +
	find . -type d \( -path ./front -o -path ./.venv \) -prune -o -name 'README.md.*' -exec rm -f  {} +

readme-toc:
	# https://github.com/ekalinin/github-markdown-toc
	find . \
		! -path './.venv/*' \
		-iname README.md \
		-exec gh-md-toc --insert {} \;
