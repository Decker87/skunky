set -e  # Exit immediately if a command exits with a non-zero status
set -o pipefail  # Exit if any command in a pipeline fails

# Create the tarball
tarball_name="skunky-0.0.1.tar.gz"
rm -f $tarball_name
tar --exclude -czvf $tarball_name -C "../python-project" "."

# Copy over the formula
brew cleanup --scrub skunky
cat formula.rb > /opt/homebrew/Library/Taps/decker87/homebrew-skunky/Formula/skunky.rb

# Try it!
brew cleanup --scrub skunky # Remove cached version
brew reinstall --build-from-source Decker87/skunky/skunky
# brew reinstall --debug --build-from-source Decker87/skunky/skunky