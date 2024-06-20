import os

def get_current_version():
    with open('VERSION', 'r') as f:
        return f.read().strip()

def bump_version(version, part='patch'):
    major, minor, patch = map(int, version.split('.'))
    
    if part == 'major':
        major += 1
        minor = 0
        patch = 0
    elif part == 'minor':
        minor += 1
        patch = 0
    elif part == 'patch':
        patch += 1
    
    new_version = f'{major}.{minor}.{patch}'
    return new_version

def write_version_to_file(version):
    with open('VERSION', 'w') as f:
        f.write(version + '\n')

def commit_and_tag_version(version):
    os.system(f'git add VERSION')
    os.system(f'git commit -m "Bump version to {version}"')
    os.system(f'git tag -a v{version} -m "Version {version}"')

if __name__ == '__main__':
    current_version = get_current_version()
    print(f'Current version: {current_version}')

    # Incrementa la versión según tu estrategia de versión
    new_version = bump_version(current_version, 'patch')  # Puedes cambiar 'patch' por 'minor' o 'major'

    # Escribe la nueva versión al archivo VERSION
    write_version_to_file(new_version)

    # Commitea y etiqueta la nueva versión en Git
    commit_and_tag_version(new_version)

    print(f'New version: {new_version}')
