## Dev stuff

```zsh
cd python-project
source venv/bin/activate
pip install -r requirements.txt

# Generate resource stanzas for formula (with venv active)
pip install homebrew-pypi-poet
./generate-resource-stanzas.sh | pbcopy

```
