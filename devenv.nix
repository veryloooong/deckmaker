{ pkgs, ... }:

{
  # (AI) Core CLI utilities and native build tools required for packaging (e.g. objdump for PyInstaller)
  packages = [
    pkgs.binutils
    pkgs.git
  ];

  # (AI) Python environment configuration with uv support
  languages.python = {
    enable = true;
    uv.enable = true;
  };

  # (AI) Environment activation message
  enterShell = ''
    echo "Deckmaker dev shell ready."
  '';
}
