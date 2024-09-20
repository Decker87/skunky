set -e  # Exit immediately if a command exits with a non-zero status
# set -o pipefail  # Exit if any command in a pipeline fails

# Create the tarball
tarball_name="skunky-0.0.1.tar.gz"

# Remove this if it exists
if [ -f $tarball_name ]; then
  rm $tarball_name
fi
tar --exclude "venv" -czvf $tarball_name -C "../python-project" "."
shasum -a 256 $tarball_name

# Copy over the formula
cat formula.rb > /opt/homebrew/Library/Taps/decker87/homebrew-skunky/Formula/skunky.rb

# Try it!
brew cleanup --scrub skunky # Remove cached version

# If there's any file in this directory that matches the tarball name, remove it
find /Users/adam/Library/Caches/Homebrew/downloads/ -name "*$tarball_name" -exec rm -f {} \;
# ls /Users/adam/Library/Caches/Homebrew/downloads/ | grep -F "$tarball_name" | xargs rm # Above command doesn't always work
brew reinstall --build-from-source Decker87/skunky/skunky
# brew reinstall --debug --build-from-source Decker87/skunky/skunky
