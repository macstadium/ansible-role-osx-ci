# Ansible Role: OSX-CI

![GPL-3.0 licensed][badge-license]
[![Build Status](https://travis-ci.org/macstadium/ansible-role-osx-ci.svg?branch=master)](https://travis-ci.org/macstadium/ansible-role-osx-ci)

Installs and configures software tools needed for building & deploying OSX/iOS applications.
The configured Mac machine can be used as a Jenkins agent.

The role creates a `ci user` that can be used to run builds on the Mac machine. It configures the user to be able to log remotely via ssh.
It also installs:

* [Homebrew][homebrew]
* [Node.js 10 LTS][node10]
* [Java 8][java8] - Jenkins requirement. By installing Java 8, the OSX machine can be easily become a Jenkins agent.
* [fastlane][fastlane]
* [CocoaPods][cocoapods]

## Requirements

The role expects Xcode Command Line Tools to be installed on the target machine. You can find all available versions in the [Apple Downloads Page][apple-downloads].
You can also install the Xcode Command Line Tools via terminal using:

    xcode-select --install

Note that this command requires user input, so you cannot execute it remotely (via ssh).

Because the role needs to set up an authorized ssh key for the ci user that enables remote login, a public ssh key needs to be pre-generated and provided to the role.
The ssh public key needs to be on the machine that `executes` the role.

## Role Variables

Role variables and their default values are listed below.
You can find all default variables in [`defaults/main.yml`](defaults/main.yml)

    ci_user: ci_user
    ci_user_uid: 5013
    ci_user_group: ci_user

The `ci user` name, uid and group to be created.

    ci_user_public_key_location:

The location of the ssh public key that will be added to the authorized keys for the `ci user`. This will allow remote login with ssh with that user.

    ci_user_default_keychain: login.keychain
    ci_user_default_keychain_password:

The name and the password of the default keychain to be created for the `ci user`.

    cask_packages: ['java8']

The [brew cask][brew-cask] packages to be installed.

    ruby_gems: ['fastlane']

The [ruby gems][ruby-gems] to be installed globally.

    homebrew_packages:

A list of extra `brew` packages to be installed

## Dependencies

None.

## Example Playbook

    - hosts: localhost
      vars:
        homebrew_packages: ['git']
        ci_user_public_key_location: '/path/to/public_key'
        ci_user_default_keychain_password: 'keychain_pass'
      roles:
        - osx-ci

## License

[GPL-3.0][link-license]

## Author Information

This role was created in 2019 by [MacStadium, Inc][macstadium].

#### Maintainer(s)

- [Ivan Spasov](https://github.com/ispasov)

[macstadium]: https://www.macstadium.com/
[homebrew]: https://brew.sh/
[node10]: https://nodejs.org/en/blog/release/v10.13.0/
[java8]: https://www.oracle.com/technetwork/java/javase/overview/java8-2100321.html
[fastlane]: https://fastlane.tools/
[cocoapods]: https://cocoapods.org/
[brew-cask]: https://github.com/Homebrew/homebrew-cask
[ruby-gems]: https://rubygems.org/
[badge-license]: https://img.shields.io/badge/License-GPL3-green.svg
[link-license]: https://raw.githubusercontent.com/macstadium/ansible-role-osx-ci/master/LICENSE
[apple-downloads]: https://developer.apple.com/download/more/