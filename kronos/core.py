import click
import os
import shutil
from .src import command as command
from .src.modules import utils

@click.group('kronos cli')
def main():
    pass

@main.command(help='initialize machine learning project')
@click.option('--dir', default=None)
def init(dir):
    command.init(dir)


@main.command(help='run script in docker container')
@click.argument('filename')
@click.option('--gpu/--local', default=False)
def run(gpu, filename):
    command.run(gpu, filename)

@main.command(help='ipython shell in docker container')
@click.option('--gpu/--local', default=False)
def shell(gpu):
    command.shell(gpu)

@main.command(help='build docker container')
@click.option('--gpu/--local', default=False)
def build(gpu):
    command.build(gpu)

@main.command(help='run notebook in docker container')
@click.option('--gpu/--local', default=False)
def notebook(gpu):
    command.notebook(gpu)

if __name__ == '__main__':
    main()
