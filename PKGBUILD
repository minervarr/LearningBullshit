# Maintainer: you
# Local PKGBUILD — no AUR needed.
# Usage:
#   cd ~/LearningBullshit
#   makepkg -si
#
# To rebuild from scratch: makepkg -si --noextract (skips re-clone)

pkgname=neuwld
pkgver=0.0
pkgrel=1
pkgdesc='A Wayland drawing library (fork of wld) — less primitive primitive drawing'
arch=('x86_64' 'aarch64')
url='https://git.sr.ht/~shrub900/neuwld'
license=('MIT')

depends=(
  'fontconfig'
  'pixman'
  'freetype2'
  'libdrm'
  'wayland'
)
makedepends=(
  'meson'
  'ninja'
  'pkg-config'
  'wayland'   # provides wayland-scanner
)

# Pull fresh from upstream each time.
# To use the already-cloned submodule instead, replace the source line with:
#   source=()
# and point _src to your local path in build().
source=("git+https://git.sr.ht/~shrub900/neuwld")
sha256sums=('SKIP')

pkgver() {
  cd "$pkgname"
  printf "0.0.r%s.%s" "$(git rev-list --count HEAD)" "$(git rev-parse --short HEAD)"
}

build() {
  # Edit these to match your GPU.  Set drm_intel=false if you have NVIDIA/AMD.
  arch-meson "$pkgname" build \
    -D enable_debug=false \
    -D drm_intel=true    \
    -D drm_nouveau=false

  ninja -C build
}

package() {
  DESTDIR="$pkgdir" ninja -C build install

  install -Dm644 "$pkgname/COPYING" \
    "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
}
