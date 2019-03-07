#!/usr/bin/python

import subprocess

from ansible.module_utils.basic import *

DOCUMENTATION = r'''
module: keychain
short_description: Create and set default keychain for a user
description:
    - Create and set default keychain for a user
options:
    name:
        description:
            - The keychain to be created or set as default
        type: str
        required: True
    password:
        description:
            - The keychain password
        type: str
        required: True
    default:
        description:
            - Set the keychain as default
        type: bool
        default: True
    state:
        description:
            - Whether the keychain should be present or absent, taking action if the state is different from what is stated.
        type: str
        choices: [ present, absent ]
        default: present
author:
- Ivan Spasov (@ispasov)
'''

EXAMPLES = r'''
- name: Set default keychain with password
  keychain:
    name: user_keychain
    password: secret
    state: present
- name: Remove keychain
  keychain:
    name: user_keychain
    state: absent
'''

def set_default_keychain(module, keychain):
    run_security(module, 'default-keychain', '-s', keychain)

def ensure_keychain_added_to_list(module, keychain):
    # There is a bug in OSX where create-keychain does not always adds the keychain to the
    # searchable list. This way we force the keychain to be added
    run_security(module, 'list-keychains', '-d', 'user', '-s', keychain)

def run_security(module, *args):
    cmd = ['security'] + list(args)
    return module.run_command(cmd)

def get_keychain_name(keychain_path):
    return keychain_path.replace('"', '').split("/")[-1]

def keychain_to_db(keychain):
    return "{}-db".format(keychain)

def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type='str', required=True),
            password=dict(type='str', required=True, no_log=True),
            default=dict(type='bool', default=True),
            state=dict(default='present', choices=['present', 'absent']),
        ),
        supports_check_mode=False,
    )

    name = module.params['name']
    password = module.params['password']
    default = module.params['default']
    state = module.params['state']

    keychain_list_output = run_security(module, 'list-keychains')[1]
    keychain_list = [get_keychain_name(keychain) for keychain in keychain_list_output.splitlines()]
    keychain_present = keychain_to_db(name) in keychain_list

    changed = False

    if not keychain_present and state == 'present':
        run_security(module, 'create-keychain', '-p', password, name)
        ensure_keychain_added_to_list(module, name)
        set_default_keychain(module, name)
        changed = True

    if keychain_present and state == 'present':
        default_keychain_output = run_security(module, 'default-keychain')[1]
        default_keychain = get_keychain_name(default_keychain_output.splitlines()[0])
        if default_keychain != keychain_to_db(name):
            set_default_keychain(module, name)
            changed = True

    if keychain_present and state == 'absent':
        run_security(module, 'delete-keychain', name)
        changed = True

    module.exit_json(changed=changed)

if __name__ == '__main__':
    main()