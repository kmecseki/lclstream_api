from psik.models import Callback, JobState

JSON = {"content-type": "application/json"}


def test_invalid_body(client):
    response = client.post(
        "/callback/producer", content='{"name": "hello"}', headers=JSON
    )
    assert response.status_code == 422


def test_unknown_job(client):
    cb = Callback(jobid="123.456", jobndx=0, state=JobState.queued, info="ok")
    response = client.post(
        "/callback/producer", content=cb.model_dump_json(), headers=JSON
    )
    assert response.status_code == 404
