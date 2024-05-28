APP = parking-devops-api

test:
	@bandit -r . -x '/venv/','/tests/'
	@black .
	@flake8 . --exclude venv
	@pytest -v --disable-warnings

compose:
	@docker compose build
	@docker compose up

setup-dev:
	@kind create cluster --config kubernetes/config/config.yaml
	@kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
	@kubectl wait --namespace ingress-nginx \
		--for=condition=ready pod \
		--selector=app.kubernetes.io/component=controller \
		--timeout=270s
	@helm upgrade \
		--install \
		--set image.tag=7.0.8 \
		--set auth.rootPassword="root" \
		my-release kubernetes/charts/mongodb
	@kubectl wait \
		--for=condition=ready pod \
		--selector=app.kubernetes.io/component=mongodb \
		--timeout=270s
	@helm repo add sealed-secrets https://bitnami-labs.github.io/sealed-secrets
	@helm upgrade \
		--install sealed-secrets \
		-n kube-system \
		--set-string fullnameOverride=sealed-secrets-controller \
		sealed-secrets/sealed-secrets
	@kubectl wait \
		--for=condition=ready pod \
		--selector=app.kubernetes.io/instance=sealed-secrets \
		--timeout=270s \
		-n kube-system

teardown-dev:
	@kind delete clusters kind

deploy-dev:
	@docker build -t $(APP):latest .
	@kind load docker-image $(APP):latest
	@kubectl apply -f kubernetes/manifests
	@kubectl rollout restart deploy parking-devops-api

dev: setup-dev deploy-dev
