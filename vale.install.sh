#!/bin/bash

cd $1

mkdir styles

curl https://install.goreleaser.com/github.com/ValeLint/vale.sh | bash

curl -L -O https://github.com/errata-ai/proselint/releases/latest/download/proselint.zip
unzip -d styles proselint.zip
rm proselint.zip

curl -L -O https://github.com/errata-ai/write-good/releases/latest/download/write-good.zip
unzip -d styles write-good.zip
rm write-good.zip

curl -L -O https://github.com/errata-ai/Joblint/releases/latest/download/Joblint.zip
unzip -d styles Joblint.zip
rm Joblint.zip

cat > .vale.ini <<EOF
StylesPath = styles

[*.md]
BasedOnStyles = proselint, write-good, Joblint
EOF
