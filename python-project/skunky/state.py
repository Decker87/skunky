import os, json, typing, re, pdb

#######################
### indexer_running ###
#######################
def determine_indexer_running() -> bool:
    brew_services_output = os.popen('brew services list').read()
    indexer_running = not not re.search(r'\nskunky\s+started', brew_services_output)
    set_indexer_running(indexer_running)
    return indexer_running

def set_indexer_running(running: bool) -> None:
    config_write('indexer_running', running)

def get_indexer_running() -> bool:
    return config_read('indexer_running')

###################
### other utils ###
###################
def skunky_base_dir() -> str:
    """Return the base directory for the skunky project."""
    return os.path.dirname(os.path.abspath(__file__))

def config_file_path() -> str:
    """Return the path to the configuration file."""
    return os.path.join(skunky_base_dir(), 'config.json')

def instantiate_config_file() -> None:
    """Create a new configuration file if it doesn't exist."""
    try:
        content = json.load(open(config_file_path(), 'r'))
        if not isinstance(content, dict):
            raise ValueError
    except (json.JSONDecodeError, FileNotFoundError, ValueError):
        json.dump({}, open(config_file_path(), 'w'), indent=2)

def config_write(key: str, value: typing.Any) -> None:
    """Write a key-value pair to the configuration file."""
    instantiate_config_file()
    content = json.load(open(config_file_path(), 'r'))
    content[key] = value
    json.dump(content, open(config_file_path(), 'w'), indent=2)

def config_read(key: str) -> typing.Any:
    """Read a value from the configuration file."""
    instantiate_config_file()
    content = json.load(open(config_file_path(), 'r'))
    return content.get(key, '')
