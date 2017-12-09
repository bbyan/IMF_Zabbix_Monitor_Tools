from fabric.api import run, env, roles, execute
from fabric.colors import red
from fabric.state import output

# Hostgroup
env.roledefs = {
    'ibuser': ['ibuser@10.211.55.200']
}
output['commands'] = False

df_command = 'df -h'


def print_red(command):
    print red(run(command))


@roles('ibuser')
def task1():
    print_red(df_command)


def dotask():
    execute(task1)
