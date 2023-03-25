@echo off
py --version
py -m pip install --upgrade pip
py -m pip install -r "./resources/app/manifests/pip_requirements.txt"
pip install -r "./resources/app/manifests/pip_requirements.txt"

@REM # Install   # Checks for jsonschema, pyjson5
@REM # Reset     # No modules
@REM # Cleanup   # No modules
py ./resources/ci/common/reset.py

@REM # Re-source           # Checks for jsonschema, pyjson5
@REM # Validate            # Uses jsonschema, pyjson5
py ./resources/ci/common/validate.py
@REM # Re-source Main      # Uses pyjson5
py ./resources/ci/common/resrc_new.py
@REM # Re-source Functions # No modules
py ./resources/ci/common/resrc_funcs.py
@REM # Validate            # Uses jsonschema, pyjson5
py ./resources/ci/common/validate.py
