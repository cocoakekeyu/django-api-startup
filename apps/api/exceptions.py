# -*- coding: utf-8 -*-
import logging

from rest_framework.views import exception_handler as rest_handler
from rest_framework.exceptions import (
    ValidationError, ParseError, AuthenticationFailed, NotAuthenticated,
    PermissionDenied, MethodNotAllowed, NotFound
)
from django.core.exceptions import ObjectDoesNotExist
from django import db
from rest_framework.response import Response


logger = logging.getLogger('exception')


class ViewException(Exception):

    def __init__(self, message, error, errors=None, errcode=400):
        self.message = message
        self.error = error
        self.errors = errors
        self.errcode = errcode


def error_response(message='invalid request', error=None,
                   errcode=422, errors=None):

    r = {
        'message': message,
        'error': error,
        'errcode': errcode,
    }
    if errors:
        r['errors'] = errors
    return Response(r, status=errcode)


# django db exception
DB_EXCEPTION = (db.Error, db.InterfaceError, db.DatabaseError,
                db.DataError, db.OperationalError, db.InternalError,
                db.ProgrammingError, db.NotSupportedError,
                db.models.ProtectedError,
                )


def exception_handler(exc, context):
    request = context.get('request')
    if request:
        request_path = request.path
        request_data = request.data
    else:
        request_path = 'null'
        request_data = 'null'
    logger.warn('{}: {!s}\nRequest path: {}\nRequest data: {!r}'
                .format(type(exc).__name__, exc, request_path, request_data),
                exc_info=True)

    if isinstance(exc, ViewException):
        return error_response(exc.message, exc.error, exc.errcode, exc.errors)

    # rest_framework exception
    elif isinstance(exc, ValidationError):
        return error_response('提交记录不合法', str(exc), 422, exc.detail)
    elif isinstance(exc, ParseError):
        return error_response('不合法的参数', str(exc), 400)
    elif isinstance(exc, (AuthenticationFailed, NotAuthenticated)):
        return error_response('未授权访问', str(exc), 401)
    elif isinstance(exc, PermissionDenied):
        return error_response('禁止访问', str(exc), 403)
    elif isinstance(exc, MethodNotAllowed):
        return error_response('方法不允许', str(exc), 405)
    elif isinstance(exc, NotFound):
        return error_response('资源未找到', str(exc), 404)

    # django exception
    elif isinstance(exc, ObjectDoesNotExist):
        return error_response('资源未找到', str(exc), 404)

    # django db exception
    elif isinstance(exc, DB_EXCEPTION):
        return error_response('处理参数时发生错误', str(exc), 422)

    else:
        return rest_handler(exc, context)
