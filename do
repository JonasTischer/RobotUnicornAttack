SOURCE_DIR=app

function help() {

  clear
  echo "================= Usage ================="
  echo "install_requirements     : Install all the packages listed in *requirements*.txt files."
  echo "venv                   : Create Python venv, use it by running 'source ./venv/bin/activate'"
}

function init() {
  venv
}

function clean() {
  rm -rf .mypy_cache/
}

function venv() {
  python3 -m venv ./venv
}

# Install all the packages listed in *requirements*.txt files.
function install_requirements() {
  find . -name '*requirements*.txt' -exec python -m pip install -r {} \;
}


case $1 in
"help") help ;;
"clean") clean ;;
"install_requirements") install_requirements ;;
"venv") venv ;;
"init") init;;
*) help ;;
esac
