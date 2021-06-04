set -euo pipefail
echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin docker.pkg.github.com
