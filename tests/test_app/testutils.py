import psycopg2

from django.db import connection


def postgres_version_gte(*version):
    """
    Return True if the version of postgresql is greater than
    or equal to the given version
    """
    version = version + (0,) * (3 - len(version))
    server_version = connection.cursor().db.connection.server_version
    if server_version < int("%d%02d%02d" % version):
        return False
    return True


def psycopg2_version_gte(version_string):
    version = psycopg2.__version__[:5]
    return version >= version_string


def skip_before_psycopg(version_string):
    def wrapper(f):
        def wrapper_(self):
            if psycopg2_version_gte(version_string):
                return f(self)
            else:
                return
        return wrapper_
    return wrapper