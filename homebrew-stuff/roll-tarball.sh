set -e  # Exit immediately if a command exits with a non-zero status
set -o pipefail  # Exit if any command in a pipeline fails

# Create the tarball
tarball_name="skunky-0.0.1.tar.gz"
rm -f $tarball_name
tar --exclude "venv" -czvf $tarball_name -C "../python-project" "."
shasum -a 256 $tarball_name

# Copy over the formula
cat formula.rb > /opt/homebrew/Library/Taps/decker87/homebrew-skunky/Formula/skunky.rb

# Try it!
brew cleanup --scrub skunky # Remove cached version
rm /Users/adam/Library/Caches/Homebrew/downloads/*skunky-0.0.1.tar.gz # Above command doesn't always work
brew reinstall --build-from-source Decker87/skunky/skunky
# brew reinstall --debug --build-from-source Decker87/skunky/skunky
