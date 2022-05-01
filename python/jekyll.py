#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import subprocess
from shlex import split

import rich
from clk.decorators import group, argument
from clk.log import get_logger
from rich.panel import Panel

LOGGER = get_logger(__name__)


def stream_command(command):
    process = subprocess.Popen(command,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    while True:
        output = process.stdout.readline()
        if not output and process.poll() is not None:
            break
        if output:
            rich.print(output.decode("utf-8").rstrip())
    rc = process.poll()

    if rc:
        rich.print(
            Panel(
                ":no_entry: " +
                f"{' '.join(command)} :\n\n{process.stderr.read().decode('utf-8')}"
            ))
    else:
        rich.print(
            Panel('[bold green]:heavy_check_mark: [/bold green] ' +
                  ' '.join(command)))

    return rc


@group()
def jekyll():
    """Commands to play with tezos-client

    While playing with the tezos block chain, this command aims to make it easier to use the underlying tezos-client command.
    See:
    \t- Tezos - https://tezos.com \r
    \t- https://tezos.gitlab.io/shell/cli-commands.html
    """


@jekyll.command()
def install():
    """Install required dependencies"""
    stream_command(split('sudo apt update'))
    stream_command(split('sudo apt install --yes ruby-full ruby-dev build-essential zlib1g-dev'))
    stream_command(split('sudo gem install jekyll bundler'))
    stream_command(split('bundle add webrick'))


@jekyll.command()
@argument('project-name', help='Your project name')
def create(project_name):
    """Create a new jekyll project"""
    stream_command(split('jekyll new ' + project_name))


@jekyll.command()
def run():
    """Run current project"""
    stream_command(split('bundle exec jekyll serve'))
