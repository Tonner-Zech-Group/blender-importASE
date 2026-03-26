#!/usr/bin/env bash
# Bootstrap script for the self-hosted GitHub Actions runner.
# Installs all required Blender versions and the blender wrapper into /usr/local/bin.
# Run once on the runner machine, then re-run when new Blender versions are needed.
#
# Usage:
#   sudo bash scripts/setup_runner.sh

set -euo pipefail

INSTALL_ROOT="/opt/blender"
WRAPPER="/usr/local/bin/blender"

declare -A BLENDER_VERSIONS=(
    ["4.4.3"]="https://ftp.halifax.rwth-aachen.de/blender/release/Blender4.4/blender-4.4.3-linux-x64.tar.xz"
    ["4.5.8-lts"]="https://www.blender.org/download/release/Blender4.5/blender-4.5.8-linux-x64.tar.xz"
)

echo "==> Installing runtime dependencies"
apt-get update -qq
apt-get install -y --no-install-recommends \
    curl xz-utils \
    libxrender1 libxxf86vm1 libxfixes3 libxi6 \
    libxkbcommon0 libsm6 libgl1 libglu1-mesa

echo "==> Creating install root at ${INSTALL_ROOT}"
mkdir -p "${INSTALL_ROOT}"

for VERSION in "${!BLENDER_VERSIONS[@]}"; do
    URL="${BLENDER_VERSIONS[$VERSION]}"
    DEST="${INSTALL_ROOT}/${VERSION}"

    if [[ -x "${DEST}/blender" ]]; then
        echo "==> Blender ${VERSION} already installed, skipping"
        continue
    fi

    echo "==> Downloading Blender ${VERSION}"
    ARCHIVE="/tmp/blender-${VERSION}-linux-x64.tar.xz"
    curl -L "${URL}" -o "${ARCHIVE}"

    echo "==> Extracting Blender ${VERSION}"
    mkdir -p "${DEST}"
    tar -xf "${ARCHIVE}" --strip-components=1 -C "${DEST}"
    rm "${ARCHIVE}"

    echo "==> Blender ${VERSION} installed at ${DEST}"
done

# Set "current" symlink to the project's minimum required version
ln -sfn "${INSTALL_ROOT}/4.4.3" "${INSTALL_ROOT}/current"
echo "==> 'current' symlink -> 4.4.3"

echo "==> Writing blender wrapper to ${WRAPPER}"
cat > "${WRAPPER}" << 'WRAPPER_SCRIPT'
#!/usr/bin/env bash
# Multi-version Blender launcher.
# Reads .blender-version from the git project root, falls back to "current" symlink.
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
VERSION_FILE="${REPO_ROOT}/.blender-version"

if [[ -f "$VERSION_FILE" ]]; then
    VERSION=$(tr -d '[:space:]' < "$VERSION_FILE")
else
    VERSION="current"
fi

BLENDER_BIN="/opt/blender/${VERSION}/blender"

if [[ ! -x "$BLENDER_BIN" ]]; then
    echo "blender-launcher: no executable found at ${BLENDER_BIN}" >&2
    echo "Available versions:" >&2
    ls /opt/blender/ >&2
    exit 1
fi

exec "$BLENDER_BIN" "$@"
WRAPPER_SCRIPT

chmod +x "${WRAPPER}"
echo "==> Wrapper installed at ${WRAPPER}"

echo ""
echo "==> Done. Installed versions:"
for VERSION in "${!BLENDER_VERSIONS[@]}"; do
    echo "    ${VERSION}  ->  ${INSTALL_ROOT}/${VERSION}/blender"
done
echo ""
echo "Test with: blender --version"
