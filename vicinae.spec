# vicinae built from source for openSUSE Tumbleweed.
# Built automatically by GitHub Actions in julianrottenberg/vicinae-rpm.
# Source build is required: upstream's prebuilt binaries link Qt private-API
# symbols (Qt_6_PRIVATE_API) that openSUSE's Qt does not provide (it uses
# versioned tags like Qt_6.11.2_PRIVATE_API), so vicinae-server cannot start
# from the official tarball on Tumbleweed.
%global debug_package %{nil}

Name:           vicinae
Version:        0.29.0
Release:        1%{?dist}
Summary:        A focused launcher for your desktop — native, fast, extensible
License:        GPL-3.0-only
URL:            https://vicinae.com
Source0:        https://codeload.github.com/vicinaehq/vicinae/tar.gz/refs/tags/v%{version}.tar.gz#/vicinae-%{version}.tar.gz
ExclusiveArch:  x86_64

BuildRequires:  cmake ninja gcc15-c++ git nodejs npm pkg-config ccache
BuildRequires:  qt6-base-devel qt6-gui-private-devel qt6-declarative-devel
BuildRequires:  qt6-declarative-private-devel qt6-wayland-devel qt6-wayland-private-devel
BuildRequires:  qt6-svg-devel qt6-shadertools-devel qt6-linguist-devel
BuildRequires:  layer-shell-qt6 layer-shell-qt6-devel qtkeychain-qt6-devel
BuildRequires:  kf6-syntax-highlighting-devel
BuildRequires:  libqalculate-devel libicu-devel libopenssl-devel
BuildRequires:  wayland-devel wayland-protocols-devel
BuildRequires:  libxcb-devel libxkbcommon-devel
BuildRequires:  xcb-util-devel xcb-util-wm-devel xcb-util-keysyms-devel xcb-util-image-devel

%description
A focused launcher for your desktop — native, fast, extensible.
Compiled from upstream sources against openSUSE Tumbleweed libraries.

%prep
%autosetup -n vicinae-%{version}

%build
export CC=gcc-15 CXX=g++-15
# Tumbleweed relocates some headers into package-specific subdirs
# (/usr/include/libxkbcommon, /usr/include/wayland); pass them explicitly.
cmake -G Ninja -B build -S . \
  -DCMAKE_BUILD_TYPE=Release \
  -DLTO=ON \
  -DUSE_SYSTEM_PROTOBUF=OFF \
  -DUSE_SYSTEM_ABSEIL=OFF \
  -DUSE_SYSTEM_CMARK_GFM=OFF \
  "-DCMAKE_CXX_FLAGS=-I/usr/include/libxkbcommon -I/usr/include/wayland" \
  "-DCMAKE_C_FLAGS=-I/usr/include/libxkbcommon -I/usr/include/wayland"
cmake --build build --parallel %{?_smp_mflags}

%install
DESTDIR=%{buildroot} cmake --install build

# strip vendored numen devel artifacts (static lib, headers, cmake configs)
rm -rf %{buildroot}%{_includedir}/numen %{buildroot}%{_libdir}/libnumen.a %{buildroot}%{_libdir}/cmake

install -D -m 644 extra/vicinae.desktop %{buildroot}%{_datadir}/applications/vicinae.desktop
install -D -m 644 extra/vicinae-url-handler.desktop %{buildroot}%{_datadir}/applications/vicinae-url-handler.desktop
install -D -m 644 extra/vicinae.png %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/vicinae.png
install -D -m 644 extra/vicinae.service %{buildroot}%{_prefix}/lib/systemd/user/vicinae.service
install -D -m 644 extra/modules-load.d/vicinae.conf %{buildroot}%{_prefix}/lib/modules-load.d/vicinae.conf
mkdir -p %{buildroot}%{_datadir}/vicinae/themes
install -m 644 extra/themes/*.toml %{buildroot}%{_datadir}/vicinae/themes/

%files
%{_bindir}/vicinae
%{_libexecdir}/vicinae/
%{_datadir}/applications/vicinae*.desktop
%{_datadir}/icons/hicolor/512x512/apps/vicinae.png
%{_datadir}/vicinae/
%{_prefix}/lib/systemd/user/vicinae.service
%{_prefix}/lib/modules-load.d/vicinae.conf

%changelog
* Sat Sep 19 2026 julianrottenberg <julianrottenberg@gmail.com> - 0.29.0-1
- Initial source build for openSUSE Tumbleweed
