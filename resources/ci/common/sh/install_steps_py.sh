py --version
py -m pip install --upgrade pip
py -m pip install -r "./resources/app/manifests/pip_requirements.txt"
pip install -r "./resources/app/manifests/pip_requirements.txt"

# Install   # Checks for jsonschema, pyjson5
# Reset     # No modules
# Cleanup   # No modules
py ./resources/ci/common/reset.py

# Re-source           # Checks for jsonschema, pyjson5
# Validate            # Uses jsonschema, pyjson5
py ./resources/ci/common/validate.py
# Re-source Main      # Uses pyjson5
py ./resources/ci/common/resrc_new.py
# Re-source Functions # No modules
py ./resources/ci/common/resrc_funcs.py
# Validate            # Uses jsonschema, pyjson5
py ./resources/ci/common/validate.py
