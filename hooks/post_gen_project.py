"""
NOTE:
	the below code is to be maintained Python 2.x-compatible
	as the whole Cookiecutter Django project initialization
	can potentially be run in Python 2.x environment
	(at least so we presume in `pre_gen_project.py`).
TODO: ? restrict Cookiecutter Django project initialization to Python 3.x environments only
"""

import os
import shutil


def remove_rest_files():
	file_names = [
		"server/apps/users/tests/test_user_rest.py",
		"server/apps/users/routes.py",
		"server/apps/users/serializers.py",
		"server/apps/users/views.py",
		"client/src/api/rest.js"
	]

	for filename in file_names:
		os.remove(filename)


def remove_graphql_files():
	file_names = [
		"server/apps/users/tests/test_user_graphql.py",
		"server/apps/users/mutations.py",
		"server/apps/users/schema.py",
		"server/apps/auth/mutations.py",
		"server/apps/auth/schema.py",
		"server/config/schema.py",
		"client/src/api/apollo.js"
	]

	for filename in file_names:
		os.remove(filename)


def remove_users_app():
	shutil.rmtree("server/apps/users")
	shutil.rmtree("server/apps/auth")


def remove_commerce_app():
	shutil.rmtree("server/apps/shops")


def remove_geo_app():
	shutil.rmtree("server/apps/geo")


def main():
	{%- if cookiecutter.include_users == 'y' -%}
	remove_users_app()
	{%-  endif -%}
	{%- if cookiecutter.include_commerce == 'y' -%}
	remove_commerce_app()
	{%-  endif -%}
	{%- if cookiecutter.include_geo == 'y' -%}
	remove_geo_app()
	{%-  endif -%}

if __name__ == "__main__":
	main()
