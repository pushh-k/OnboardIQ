# install:
# 	python3 -m venv .venv
# 	source .venv/bin/activate && pip install -r requirements.txt

# test:
# 	source .venv/bin/activate && pytest -q

# run-dashboard:
# 	source .venv/bin/activate && streamlit run src/onboardiq/dashboard/app.py
install:
	python3 -m venv .venv
	source .venv/bin/activate && pip install -r requirements.txt

test:
	source .venv/bin/activate && pytest -q

run-dashboard:
	source .venv/bin/activate && streamlit run src/onboardiq/dashboard/app.py

