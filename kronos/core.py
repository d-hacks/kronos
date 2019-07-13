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
def ipython(gpu):
    command.ipython(gpu)


@main.command(help='build docker container')
@click.option('--gpu/--local', default=False)
def build(gpu):
    command.build(gpu)


@main.command(help='run notebook in docker container')
@click.option('--gpu/--local', default=False)
def notebook(gpu):
    command.notebook(gpu)


@main.command(help='run jupter lab in docker container')
@click.option('--gpu/--local', default=False)
def lab(gpu):
    command.lab(gpu)


@main.command(help='run /bin/bash in the container')
@click.option('--gpu/--local', default=False)
@click.option('--name', default=None)
def bash(gpu, name):
    command.bash(gpu, name)


if __name__ == '__main__':
    main()
