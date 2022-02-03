import os
from typing import Any

from celery import Celery
from flask import Flask, request, make_response

from app.main import threaded_pull_for_account_sql
from app.flask_.mappings import team_to_account_id, service_to_controller
from app.database import Session

app = Flask(__name__)


def make_celery(app: Flask):
    '''Create celery instance with flask app context.'''
    celery = Celery(
        app.import_name,
        broker=os.environ.get("BROKER_URL", "redis://redis:6379"),
        backend=os.environ.get("BACKEND_URL", "redis://redis:6379"),
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args: Any, **kwargs: Any) -> Any:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask

    return celery


celery_ = make_celery(app)


@celery_.task
def run_sync(updated_after, updated_before):
    session = Session()
    for team, account_id in team_to_account_id.items():
        for service, controller in service_to_controller.items():
            threaded_pull_for_account_sql(
                account_id=str(account_id),
                fetcher_service=service,
                writer_controller=controller,
                pages=10,
                session=session,
                updated_after=updated_after,
                updated_before=updated_before,
            )

@app.route('/',methods = ['GET','POST'])
def index():
    print('evet api working successfully.')
    return "evet api success."


@app.post('/sync')
def sync():
    updated_after = request.args.get("updated_after")
    updated_before = request.args.get("updated_before")

    run_sync.apply_async(args=[updated_after, updated_before])

    return make_response("Started sync", 200)
