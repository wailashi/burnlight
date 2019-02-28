import click
import requests
import json


class Context:
    def __init__(self, url):
        self.url = url


def get(address):
    ctx = click.get_current_context()
    result = None
    try:
        result = requests.get(ctx.obj.url + address).text
    except requests.exceptions.RequestException as e:
        click.echo(e)
    return result


def put(address, payload):
    ctx = click.get_current_context()
    try:
        requests.put(ctx.obj.url + address, data=payload)
    except requests.exceptions.RequestException as e:
        click.echo(e)


def post(address, payload):
    ctx = click.get_current_context()
    try:
        requests.post(ctx.obj.url + address, data=payload)
    except requests.exceptions.RequestException as e:
        click.echo(e)


def patch(address, payload):
    ctx = click.get_current_context()
    try:
        requests.patch(ctx.obj.url + address, data=payload)
    except requests.exceptions.RequestException as e:
        click.echo(e)


@click.group()
@click.option('--host', '-H', default='localhost')
@click.option('--port', '-P', type=click.INT, default='34455')
@click.pass_context
def cli(ctx, host, port):
    """Burnlight client.

    This is a client for interacting with a burnlight server.
    """
    url = 'http://{}:{}'.format(host, port)
    ctx.obj = Context(url)


@cli.group()
@click.pass_context
def schedules(ctx):
    """Manage schedules."""


@schedules.command(name='list')
@click.pass_obj
def schedules_list(ctx):
    """List all schedules."""
    try:
        click.echo(get('/api/schedules'))
    except requests.exceptions.RequestException as e:
        click.echo(e)


@schedules.command(name='add')
@click.option('--start_time')
@click.argument('schedule', type=click.File('rb'))
@click.pass_obj
def schedules_add(ctx, schedule, start_time=None):
    """Add a schedule."""
    click.echo('Adding schedule {}'.format(schedule.name))
    post('/api/schedules', json.dumps({'program': schedule.read().decode('utf-8'), 'start_time': start_time}))


@schedules.command(name='stop')
@click.argument('schedule_id', type=click.INT)
@click.pass_obj
def schedules_stop(ctx, schedule_id):
    """Stop a schedule."""
    click.echo('Stopping schedule {}'.format(schedule_id))
    patch('/api/schedules/' + str(schedule_id), json.dumps({'command': 'stop'}))


@schedules.command(name='start')
@click.argument('schedule_id', type=click.INT)
@click.option('--start_time')
@click.pass_obj
def schedules_start(ctx, schedule_id, start_time=None):
    """Starts a schedule."""
    click.echo('Starting schedule {}'.format(schedule_id))
    patch('/api/schedules/' + str(schedule_id), json.dumps({'command': 'start', 'start_time': start_time}))


@cli.group()
@click.pass_context
def channels(ctx):
    """Manage channels."""


@channels.command(name='list')
@click.pass_obj
def channels_list(ctx):
    try:
        click.echo(get('/api/channels'))
    except requests.exceptions.RequestException as e:
        click.echo(e)


if __name__ == '__main__':
    cli()
