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


@schedules.command()
@click.pass_obj
def list(ctx):
    """List all schedules."""
    try:
        click.echo(get('/api/schedules'))
    except requests.exceptions.RequestException as e:
        click.echo(e)


@schedules.command()
@click.option('--run', is_flag=True)
@click.argument('schedule', type=click.File('rb'))
@click.pass_obj
def add(ctx, schedule, run):
    """Add a schedule."""
    click.echo('Adding schedule {}'.format(schedule.name))
    post('/api/schedules', json.dumps({'program': schedule.read().decode('utf-8')}))
    if run:
        click.echo('Running schedule {}'.format(schedule))


@schedules.command()
@click.argument('schedule_id', type=click.INT)
@click.pass_obj
def stop(ctx, schedule_id):
    """Stop a schedule."""
    click.echo('Stopping schedule {}'.format(schedule_id))
    patch('/api/schedules/' + str(schedule_id), json.dumps({'command': 'stop'}))


@schedules.command()
@click.argument('schedule_id', type=click.INT)
@click.pass_obj
def start(ctx, schedule_id):
    """Starts a schedule."""
    click.echo('Starting schedule {}'.format(schedule_id))
    patch('/api/schedules/' + str(schedule_id), json.dumps({'command': 'start'}))


if __name__ == '__main__':
    cli()
