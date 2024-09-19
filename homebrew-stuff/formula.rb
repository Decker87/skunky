class Skunky < Formula
  include Language::Python::Virtualenv

  desc "Find your google drive files easily from the command line."
  homepage "https://www.example.com"
  url "file:///Users/adam/workspace/Decker87/skunky/homebrew-stuff/skunky-0.0.1.tar.gz"

  depends_on "python@3.12"

  def install
    virtualenv_install_with_resources
  end

  test do
    assert_match(1, 1)
  end
end
