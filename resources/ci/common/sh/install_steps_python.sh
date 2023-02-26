python --version
python -m pip install --upgrade pip
python -m pip install -r "./resources/app/manifests/pip_requirements.txt"
pip install -r "./resources/app/manifests/pip_requirements.txt"

# Install   # Checks for jsonschema, pyjson5
# Reset     # No modules
# Cleanup   # No modules
python ./resources/ci/common/reset.py

# Re-source           # Checks for jsonschema, pyjson5
# Validate            # Uses jsonschema, pyjson5
python ./resources/ci/common/validate.py
# Re-source Main      # Uses pyjson5
python ./resources/ci/common/resrc_new.py
# Re-source Functions # No modules
python ./resources/ci/common/resrc_funcs.py
# Validate            # Uses jsonschema, pyjson5
python ./resources/ci/common/validate.py
