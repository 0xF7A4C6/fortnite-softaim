.PHONY: all clean install labelise

clear:
	cls||clear

run: clear
	cd ../src/ && pyclean .

install: clear
	pip install -r requirements.txt
	cd ../src/ && python main.py init

labelise: clear
	cd ../src/ && python main.py labelise