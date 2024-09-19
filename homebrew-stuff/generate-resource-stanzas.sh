set -e  # Exit immediately if a command exits with a non-zero status
set -o pipefail  # Exit if any command in a pipeline fails

# Figure out the right args to poet, like:
# poet -r package1 -a package2 -a package3
poet_args=""
first_iteration=true

for package in `cat ../python-project/requirements.txt`; do
  if [ "$first_iteration" = true ]; then
    poet_args="-r ${package}"
    first_iteration=false
  else
    poet_args="${poet_args} -a ${package}"
  fi
done

poet_path="../python-project/venv/bin/poet"
echo "# CMD: $poet_path $poet_args" 1>&2
$poet_path $poet_args
