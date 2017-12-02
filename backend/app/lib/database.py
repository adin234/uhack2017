from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import sqltypes

__all__ = ['db', 'Serializer']

db = SQLAlchemy()


class Serializer(object):
    """ Serializer object to be used by
        models to serialize and format
        returns
    """
    __public__ = None
    __meta__ = ['created_at', 'updated_at']

    def serialize(self, exclude_columns=[], include_columns=[]):
        """ Safely serializes the object
        """
        _ret = dict()

        # NOTE: Add special cases here, special cases are those that
        # are not serailzable by nature. Add custom function to serialize
        _special_cases = dict()
        _special_cases[sqltypes.DateTime] = lambda x: x.strftime('%Y-%m-%dT%H:%M:%SZ')
        _special_cases[sqltypes.DECIMAL] = lambda x: float(str(x or 0))
        _special_cases[sqltypes.Enum] = lambda x: x.value


        for cols in self.__table__.columns:
            col_val = getattr(self, cols.name)

            if cols.name not in exclude_columns:
                if len(include_columns) > 0 and cols.name not in include_columns:
                    continue
                if col_val is None:
                    # Ignore none values
                    _ret[cols.name] = None
                elif type(cols.type) in _special_cases:
                    _ret[cols.name] = _special_cases[type(cols.type)](col_val)
                else:
                    _ret[cols.name] = col_val

        return _ret


    def set_public(self, column_list):
        """ Defines public variable to be used
            by serialize.
        """
        if type(column_list) is not list:
            raise TypeError('Values must be list')

        self.__public__ = column_list

        return self
