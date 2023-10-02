import os
import shutil
from datetime import datetime
from models import Base, Author, AnalysisResult

from flask import Flask, request, jsonify
import git
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.orm import sessionmaker


# Inicializa o app Flask
app = Flask(__name__)

# Configuração SQLAlchemy
engine = create_engine('sqlite:///git_analysis_results.db')
Session = sessionmaker(bind=engine)
session = Session()


@app.route('/analisador-git', methods=['GET'])
def git_analysis():
    try:
        # Define a URL do repositório
        usuario = request.args.get('usuario')
        repositorio = request.args.get('repositorio')

        if not usuario or not repositorio:
            return "Por favor, disponibilize o usuário e o nome do repositório."

        repo_url = f'https://github.com/{usuario}/{repositorio}.git'

        # Define o diretório local
        repo_dir = 'diretorio_local_repositorio'

        # Remove o repositório se já existir
        if os.path.exists(repo_dir):
            shutil.rmtree(repo_dir)

            # # Clona o repositório
            # try:
            #     repo = git.Repo.clone_from(repo_url, repo_dir)
            # except git.exc.GitCommandError:
            #     return f"O repositório {repo_url} não existe ou é privado."

        # Verifica se o diretório do repositório clonado está vazio
        if not os.listdir(repo_dir):
            return f"O repositório {repo_url} não existe ou é privado."

        # Inicializa dicionário para armazenar os commits por desenvolvedor
        commits_por_desenvolvedor = {}

        # Itera pelo histórico de commit
        for commit in repo.iter_commits():
            # Obtem o nome do autor
            autor = commit.author.name

            # Se o autor não estiver no dicionário inicia com 1
            if autor not in commits_por_desenvolvedor:
                commits_por_desenvolvedor[autor] = 1
            # Incrementa mais um ao autor
            else:
                commits_por_desenvolvedor[autor] += 1

            # Resgata a data do commit
            data_commit = commit.committed_datetime.date()

        # Inicializa o dicionário para armazenar o número de dias
        dias_por_desenvolvedor = {}

        # Itera pelo histórico de commits
        for commit in repo.iter_commits():
            # Obtem o nome do autor
            autor = commit.author.name
            data_commit = commit.committed_datetime.date()

            # Se o nome do autor não estiver no dicionário, adiciona e coloca a data de commit
            if autor not in dias_por_desenvolvedor:
                dias_por_desenvolvedor[autor] = {data_commit}
            # Adiciona mais commits ao set de datas do autor
            else:
                dias_por_desenvolvedor[autor].add(data_commit)

        response = ''

        # Retorna o total de commits e a média de commits por dia por desenvolvedor
        for autor, commits in commits_por_desenvolvedor.items():
            dias = len(dias_por_desenvolvedor[autor])
            media_commits_por_dia = commits/dias
            response += f'{autor} realizou {commits} commits com uma média de {media_commits_por_dia:.2f} commits por dia.<br>'

            # Cria todas as tabelas se não existir
            Base.metadata.create_all(engine)

            # Insira o autor na tabela Authors (ou recupere se já existir)
            author = session.query(Author).filter_by(author_name=autor).first()
            if not author:
                author = Author(author_name=autor)
                session.add(author)
                session.commit()

            # Insira os resultados da análise na tabela AnalysisResult
            analysis_result = AnalysisResult(
                author_id=author.author_id,
                analyze_date=datetime.now(),
                average_commits=media_commits_por_dia,
                repository_url=repo_url,
                repository_name=repositorio
            )

            # Adiciona o objeto AnalysisResult na transação e fazer o commit no banco
            session.add(analysis_result)
            session.commit()

            # Fecha a conexão com o banco
            session.close()

        # Remove o repositório clonado após a análise
        if os.path.exists(repo_dir):
            shutil.rmtree(repo_dir)

        return response

    except Exception as err:
        return f'ERROR: {str(err)}', 400


@app.route('/analisador-git/buscar', methods=['GET'])
def buscar_medias_de_commit():
    try:
        autor1 = request.args.get('autor1')
        autor2 = request.args.get('autor2')
        autor3 = request.args.get('autor3')
        autores = [autor1, autor2, autor3]

        engine = create_engine('sqlite:///git_analysis_results.db')
        Session = sessionmaker(bind=engine)
        session = Session()

        resultados = set()  # Use a set to store unique results

        for autor in autores:
            if autor:
                # Consulta ambas as tabelas e obtém os resultados desejados
                query = session.query(Author.author_name, AnalysisResult.average_commits).\
                    join(AnalysisResult).\
                    filter(Author.author_name.ilike(f"%{autor}%"))

                for author_name, average_commits in query.all():
                    resultados.add(f'{author_name} possui uma média de {average_commits:.2f} commits por dia.')

        # Close the database session
        session.close()

        # Return results as JSON
        return jsonify(list(resultados))

    except Exception as e:
        return str(e), 400


if __name__ == '__main__':
    app.run(debug=True)
