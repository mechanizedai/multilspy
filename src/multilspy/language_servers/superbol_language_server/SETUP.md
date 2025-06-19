bash -c "sh <(curl -fsSL https://raw.githubusercontent.com/ocaml/opam/master/shell/install.sh)"

opam init

opam switch create superbol-studio 4.14.1

git clone https://github.com/OCamlPro/superbol-studio-oss.git

cd superbol-studio-oss

opam install drom -y

eval $(opam env)

drom install --switch superbol-studio -y

opam exec --switch superbol-studio -- superbol-free lsp --version