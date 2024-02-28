


create environment: python3 -m venv venv
activate: source venv/bin/activate
persist dependencies: pip freeze > requirements.txt
install all dependencies: pip install -r requirements.txt
install dependency manually: pip install <name>
upgrade dependency: python3.9 -m pip install --upgrade <name>