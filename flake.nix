{

  description = "Flake shell";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-parts.url = "github:hercules-ci/flake-parts";
  };

  outputs =
    inputs@{ flake-parts, nixpkgs, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      systems = nixpkgs.lib.platforms.all;

      perSystem =
        { pkgs, ... }:
        {
          devShells.default = pkgs.mkShell {
            packages = with pkgs; [
              mariadb
              mariadb.client
              libmysqlclient
              postgresql
              libpq.dev
              pkg-config
              python312Packages.venvShellHook
            ];
            venvDir = ".venv";
            env = {
              PYTHONPATH = "/Users/gen/Projects/optuna/";
            };
          };

          packages = with pkgs.python312Packages; rec {
            optuna = buildPythonPackage {
              name = "optuna";
              src = ./.;
              format = "pyproject";

              buildInputs = [
                setuptools
              ];

              propagatedBuildInputs = [
                alembic
                colorlog
                numpy
                packaging
                sqlalchemy
                tqdm
                pyyaml

                pytest
              ];
            };

            optuna-doc = pkgs.stdenv.mkDerivation {
              name = "optuna-doc";
              src = ./.;
              buildInputs = [
                pkgs.optipng
                pkgs.graphviz

                (pkgs.python312.withPackages (
                  ps: with ps; [
                    optuna

                    sphinx
                    (pkgs.python312Packages.buildPythonPackage {
                      name = "sphinx-gallary";
                      # https://github.com/sphinx-gallery/sphinx-gallery/commit/07479c9e2c84029343317a1d864ca02991334c29
                      src = pkgs.fetchFromGitHub {
                        owner = "sphinx-gallery";
                        repo = "sphinx-gallery";
                        rev = "07479c9e2c84029343317a1d864ca02991334c29";
                        sha256 = "sha256-v0Ya0TVuCCdDv/3nnIO7QmUCUq1Q83oyCmAFl0gVBVE=";
                      };
                      format = "pyproject";
                      buildInputs = [
                        setuptools
                        setuptools_scm
                      ];
                      propagatedBuildInputs = [
                        pillow
                        sphinx
                      ];
                    })

                    ase
                    cmaes
                    fvcore
                    kaleido
                    lightgbm
                    matplotlib
                    pandas
                    pillow
                    plotly
                    scikit-learn
                    sphinx-copybutton
                    sphinx-notfound-page

                    sphinx_rtd_theme
                    torch
                    torchvision
                  ]
                ))
              ];

              buildPhase = ''
                cd docs
                python3 -c "import kaleido"
                make SPHINXOPTS="-W --keep-going -D plot_gallery=0" html
              '';

              installPhase = ''
                mkdir -p $out/share/doc/optuna
                cp -r ./build/html/* $out/share/doc/optuna/
              '';
            };
          };
        };

    };
}
