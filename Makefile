include .env

store_apply:
	cd src/feature_store && feast apply
