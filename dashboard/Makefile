requirements:
	echo "Exporting Python project dependencies"
	poetry export -f requirements.txt --output requirements.txt --without-hashes

dashboard:
	poetry run streamlit run main.py --server.runOnSave true