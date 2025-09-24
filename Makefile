format:
	black .
	isort .
	docformatter --in-place --recursive --wrap-summaries=88 --wrap-descriptions=88 app
	
lint:
	flake8 .