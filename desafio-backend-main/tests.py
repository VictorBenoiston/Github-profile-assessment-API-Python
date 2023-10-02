import git
import pytest
from flask import Flask

import api


@pytest.fixture
def flask_app():
    app = Flask(__name__)
    return app


def test_git_analysis(flask_app):
    with flask_app.test_request_context(
        'analisador-git?usuario=gitpython-developers&repositorio=gitdb'
    ):
        result = api.git_analysis()
        assert 'Sebastian Thiel realizou 275 commits com uma média de 2.96 commits por dia.' in result


def test_buscar_medias_de_commit(flask_app):
    with flask_app.test_request_context(
            'analisador-git/buscar?autor1=Sebastian'
    ):
        response = api.buscar_medias_de_commit()
        expected_result = 'Sebastian Thiel possui uma média de 2.96 commits por dia'
        assert expected_result in response.get_json()[0]



def test_git_analysis_no_repo(flask_app):
    with flask_app.test_request_context(
        'analisador-git?usuario=gitpython-developers&repositorio=gitdb'
    ):
        with pytest.raises(git.exc.GitCommandError):
            result = api.git_analysis()
