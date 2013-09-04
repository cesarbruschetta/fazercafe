#!/bin/bash
#Conexão do banco de dados
#export DATABASE_URL = 'postgres://foo:bar@localhost:5432/db'

export DATABASE_URL='postgres://root:root@localhost:5432/quemfezcafe'
/opt/projetos/quemfezcafe/bin/python ./manage.py runserver