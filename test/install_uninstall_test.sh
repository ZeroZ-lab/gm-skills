#!/bin/sh

set -eu

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)

fail() {
  printf '%s\n' "$1" >&2
  exit 1
}

assert_contains() {
  haystack=$1
  needle=$2
  message=$3

  printf '%s' "$haystack" | grep -F "$needle" >/dev/null || fail "$message"
}

[ -x "$repo_root/install.sh" ] || fail "install.sh is missing or not executable"
[ -x "$repo_root/uninstall.sh" ] || fail "uninstall.sh is missing or not executable"

tmp_dir=$(mktemp -d)
trap 'rm -rf "$tmp_dir"' EXIT INT TERM

fixture_repo="$tmp_dir/repo"
fixture_home="$tmp_dir/home"
mkdir -p "$fixture_repo/skills/alpha" "$fixture_repo/skills/beta" "$fixture_home"
cp "$repo_root/install.sh" "$fixture_repo/install.sh"
cp "$repo_root/uninstall.sh" "$fixture_repo/uninstall.sh"
chmod +x "$fixture_repo/install.sh" "$fixture_repo/uninstall.sh"

install_output=$(HOME="$fixture_home" "$fixture_repo/install.sh" 2>&1)

target_dir="$fixture_home/.claude/skills"
[ -d "$target_dir" ] || fail "install did not create target directory"
assert_contains "$install_output" "[install] creating target directory: $target_dir" "install should log target directory creation"
assert_contains "$install_output" "[install] linked alpha -> $fixture_repo/skills/alpha" "install should log alpha link creation"
assert_contains "$install_output" "[install] linked beta -> $fixture_repo/skills/beta" "install should log beta link creation"

for skill in alpha beta; do
  link_path="$target_dir/$skill"
  expected_path="$fixture_repo/skills/$skill"

  [ -L "$link_path" ] || fail "expected $link_path to be a symlink"
  actual_path=$(readlink "$link_path")
  [ "$actual_path" = "$expected_path" ] || fail "expected $link_path -> $expected_path, got $actual_path"
done

# Idempotency: a second install should preserve the same links.
install_output=$(HOME="$fixture_home" "$fixture_repo/install.sh" 2>&1)
assert_contains "$install_output" "[install] target directory already exists: $target_dir" "install should log existing target directory"
assert_contains "$install_output" "[install] already linked: $target_dir/alpha" "install should log alpha skip"
assert_contains "$install_output" "[install] already linked: $target_dir/beta" "install should log beta skip"

for skill in alpha beta; do
  link_path="$target_dir/$skill"
  expected_path="$fixture_repo/skills/$skill"
  actual_path=$(readlink "$link_path")
  [ "$actual_path" = "$expected_path" ] || fail "second install changed $link_path"
done

# Install should fail with a clear conflict error.
rm "$target_dir/alpha"
mkdir "$target_dir/alpha"
set +e
conflict_output=$(HOME="$fixture_home" "$fixture_repo/install.sh" 2>&1)
conflict_status=$?
set -e
[ "$conflict_status" -ne 0 ] || fail "install should fail on conflicting path"
assert_contains "$conflict_output" "[install] error: existing path blocks symlink: $target_dir/alpha" "install should report conflicting path"
rm -rf "$target_dir/alpha"
ln -s "$fixture_repo/skills/alpha" "$target_dir/alpha"

# Uninstall should remove only links that point to this repo.
ln -s "$tmp_dir/elsewhere" "$target_dir/external"
uninstall_output=$(HOME="$fixture_home" "$fixture_repo/uninstall.sh" 2>&1)
assert_contains "$uninstall_output" "[uninstall] removed link: $target_dir/alpha" "uninstall should log alpha removal"
assert_contains "$uninstall_output" "[uninstall] removed link: $target_dir/beta" "uninstall should log beta removal"
assert_contains "$uninstall_output" "[uninstall] skipped unrelated link: $target_dir/external" "uninstall should log unrelated link skip"

for skill in alpha beta; do
  [ ! -e "$target_dir/$skill" ] || fail "uninstall did not remove $target_dir/$skill"
done

[ -L "$target_dir/external" ] || fail "uninstall removed unrelated symlink"

empty_home="$tmp_dir/empty-home"
mkdir -p "$empty_home"
uninstall_output=$(HOME="$empty_home" "$fixture_repo/uninstall.sh" 2>&1)
assert_contains "$uninstall_output" "[uninstall] target directory does not exist: $empty_home/.claude/skills" "uninstall should log missing target directory"
