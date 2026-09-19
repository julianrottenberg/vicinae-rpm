#!/bin/bash
# build-rpm.sh — runs inside an opensuse/tumbleweed container (GitHub Actions).
# Builds vicinae $VICINAE_VERSION from source and produces an RPM in /out/rpms.
set -euo pipefail

: "${VICINAE_VERSION:?set VICINAE_VERSION (e.g. 0.29.0)}"

zypper -n ref -f
zypper -n in -y --no-recommends \
  cmake ninja gcc15-c++ git rpm-build curl nodejs npm ccache pkg-config \
  qt6-base-devel qt6-gui-private-devel qt6-declarative-devel \
  qt6-declarative-private-devel qt6-wayland-devel qt6-wayland-private-devel \
  qt6-svg-devel qt6-shadertools-devel qt6-linguist-devel \
  layer-shell-qt6 layer-shell-qt6-devel qtkeychain-qt6-devel \
  kf6-syntax-highlighting-devel \
  libqalculate-devel libicu-devel libopenssl-devel \
  wayland-devel wayland-protocols-devel \
  libxcb-devel libxkbcommon-devel xcb-util-devel xcb-util-wm-devel xcb-util-keysyms-devel xcb-util-image-devel

export CC=gcc-15 CXX=g++-15

mkdir -p ~/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
curl -fsSL -o ~/rpmbuild/SOURCES/vicinae-${VICINAE_VERSION}.tar.gz \
  "https://codeload.github.com/vicinaehq/vicinae/tar.gz/refs/tags/v${VICINAE_VERSION}"

cp /out/vicinae.spec ~/rpmbuild/SPECS/
sed -i "s/^Version:.*/Version:        ${VICINAE_VERSION}/" ~/rpmbuild/SPECS/vicinae.spec

rpmbuild -bb ~/rpmbuild/SPECS/vicinae.spec

mkdir -p /out/rpms
cp ~/rpmbuild/RPMS/x86_64/vicinae-*.rpm /out/rpms/
echo "RPM_BUILD_OK"
