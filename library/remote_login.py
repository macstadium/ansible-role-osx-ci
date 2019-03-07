#!/usr/bin/python

import subprocess

from ansible.module_utils.basic import *

DOCUMENTATION = r'''
module: remote_login
short_description: Manage remote login on OSX machine for a given user
description:
    - Enable and disable remote login
options:
    user:
        description:
            - The username of the user whose remote login access we are going to modify
        type: str
        required: True
    state:
        description:
            - Whether the remote login of the user is enabled or disabled, taking action if the state is different from what is stated.
        type: str
        choices: [ enable, disable ]
        default: enable
author:
- Ivan Spasov (@ispasov)
'''

EXAMPLES = r'''
- name: Enable remote login for user remote_user
  remote_login:
    user: remote_user
    state: enable
- name: Disable remote login for user remote_user
  remote_login:
    user: remote_user
    state: disable
'''

def run_system_setup(module, *args):
    cmd = ['systemsetup'] + list(args)
    return module.run_command(cmd)

def run_dsedit_group(module, edit_operation, user):
    return module.run_command(['dseditgroup', '-o', 'edit', '-{}'.format(edit_operation), user, '-t', 'user', 'com.apple.access_ssh'])

def get_access_ssh_info(module):
    rawData = module.run_command(['dscl', '.', '-read', '/Groups/com.apple.access_ssh'])[1]
    rawLines = [line.strip().split(': ') for line in rawData.splitlines()]
    return {line[0]:line[1:] for line in rawLines}

def main():
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(default='enable', choices=['enable', 'disable']),
            user=dict(type='str', required=True),
        ),
        supports_check_mode=False,
    )

    state = module.params['state']
    user = module.params['user']

    remote_login_output = run_system_setup(module, '-getremotelogin')[1]
    remote_login_enabled = 'on' in remote_login_output.lower()

    changed = False

    if not remote_login_enabled:
        run_system_setup(module, '-setremotelogin', 'on')
        changed = True

    access_ssh_info = get_access_ssh_info(module)
    access_ssh_users = access_ssh_info.get('GroupMembership', [''])[0].split(' ')
    edit_operation = 'a' if state == 'enable' else 'd'
    should_add_user = user not in access_ssh_users and state == 'enable'
    should_remove_user = user in access_ssh_users and state == 'disable'

    if (should_add_user or should_remove_user):
        run_dsedit_group(module, edit_operation, user)
        changed = True

    module.exit_json(changed=changed)

if __name__ == '__main__':
    main()