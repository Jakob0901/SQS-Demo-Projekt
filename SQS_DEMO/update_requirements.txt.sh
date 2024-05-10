#!/bin/bash

source .venv/bin/activate

pip freeze | grep -f <(pipdeptree --packages-only) > requirements.txt

deactivate
