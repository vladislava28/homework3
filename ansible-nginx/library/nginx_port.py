from ansible.module_utils.basic import AnsibleModule
import os

def main():
    module = AnsibleModule(
        argument_spec={
		'port': dict(type='int', default=80)
	}
    )

    port = module.params['port']

    if port < 1 or port > 65535:
        module.fail_json(msg="Порт неверный! Диапазон от 1 до 65535")

    config_path = config_path = '/etc/nginx/sites-available/files'

    if not os.path.exists(config_path):
        module.fail_json(msg="Конфигурация не найдена")

    with open(config_path, 'r') as f:
        content = f.read()

    old_string = "listen 80;"
    new_string = f"listen {port};"

    if old_string not in content:
        module.fail_json(msg="Не найдена строка 'listen 80;'")

    new_content = content.replace(old_string, new_string)
    changed = False

    if content != new_content:
        with open(config_path, 'w') as f:
            f.write(new_content)
        changed = True

    module.exit_json(changed=changed, msg=f"Порт {port} принят")

if __name__ == '__main__':
    main()
