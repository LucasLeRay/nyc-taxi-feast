include .env
export $(shell sed 's/=.*//' .env)

store_apply:
	cd src/feature_store && feast apply
