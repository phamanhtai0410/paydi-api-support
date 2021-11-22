# -*- coding: utf-8 -*-



# File: base.py
# Created at 03/11/2021
"""
   Description:
        -
        -
"""

import json
import traceback
from datetime import datetime

import sentry_sdk
from bson import ObjectId
from pymodm import fields, MongoModel, connection
from sentry_sdk import capture_exception
from src.decorators.cache import cache_id, cache_filter
from src.utils.datetime import get_current_time
from src.utils.validators import is_oid

SIZE = 10000



class BaseMG(MongoModel):
    created_by = fields.CharField(default='', blank=True)
    updated_by = fields.CharField(default='', blank=True)
    created_time = fields.DateTimeField(default=None)
    updated_time = fields.DateTimeField(default=None)

    @classmethod
    def current(cls):
        print(cls._mongometa)
        return connection._get_db(cls._mongometa.connection_alias)[cls._mongometa.collection_name]

    @classmethod
    def update_many(cls, filter, update_data):
        try:

            _keys = update_data.keys()
            _delete_keys = ['created_by', 'created_time', '_id']
            for _key in _delete_keys:
                if _key in _keys:
                    del update_data[_key]
            update_data['updated_time'] = datetime.utcnow()
            return cls.objects.raw(filter).update({
                '$set': update_data
            })
        except cls.DoesNotExist:
            return []
        except Exception as e:
            capture_exception(e)
            traceback.print_exc()
            return []

            
    @classmethod
    def update_one(cls, filter, update_data):
        try:
            _keys = update_data.keys()
            _delete_keys = ['created_by', 'created_time', '_id']
            for _key in _delete_keys:
                if _key in _keys:
                    del update_data[_key]
            update_data['updated_time'] = datetime.utcnow()
            return cls.current().update_one(filter, update={
                '$set': update_data
            })
        except cls.DoesNotExist:
            return {}
        except Exception as e:
            capture_exception(e)
            traceback.print_exc()
            return {}


    @classmethod
    def init_row(cls, payload):
        _init = {}
        for field in cls._mongometa.get_fields():
            if field.mongo_name == '_id':
                if not isinstance(payload.get('_id'), ObjectId):
                    if is_oid(payload.get(field.mongo_name)):
                        _init[field.mongo_name] = ObjectId(payload.get(field.mongo_name))
                    else:
                        _init[field.mongo_name] = ObjectId()
            else:
                if field.mongo_name in ['created_time', 'updated_time']:
                    if not isinstance(field.mongo_name, datetime):
                        if isinstance(field.mongo_name, (float, int)):
                            _init[field.mongo_name] = datetime.fromtimestamp(
                                payload.get(field.mongo_name, field.default))
                        else:
                            _init[field.mongo_name] = get_current_time()
                else:
                    _init[field.mongo_name] = payload.get(field.mongo_name, field.default)
        return _init

    @classmethod
    def add(cls, payload):
        return cls(**cls.init_row(payload)).save()

    def to_dict(self):
        _dict = self.to_son().to_dict()
        if '_id' in _dict.keys():
            _dict['_id'] = str(_dict['_id'])
        return _dict

    @classmethod
    def get_one(cls, filter, with_cache=True):
        try:
            _keys = list(filter.keys())

            def get_db():
                value = cls.objects.get(filter)
                if value:
                    return value.to_dict()
                return {}

            if with_cache:
                @cache_filter(key_prefix=cls.Meta.collection_name, key_fields=_keys, options=[])
                def get_cache_by_filter(*args, **kwargs):
                    return get_db()

                return get_cache_by_filter(**filter, options=[])
            return get_db()

        except cls.DoesNotExist:
            return {}
        except:
            capture_exception()
            traceback.print_exc()
            return {}

    @classmethod
    def get_by_filter(cls, filter={}, options={}, with_cache=True):
        try:
            _keys = filter.keys()
            __option_keys = options.keys()

            def get_db():
                _query = [{
                    '$match': filter
                }]
                if 'sort' in __option_keys:
                    _query.append({
                        '$sort': options.get('sort')
                    })
                if 'offset' in __option_keys:
                    _query.append({
                        '$skip': options.get('offset')
                    })
                if 'limit' in __option_keys:
                    _query.append({
                        '$limit': options.get('limit')
                    })
                values = cls.objects.aggregate(*_query)
                return list(values)

            if with_cache:
                @cache_filter(key_prefix=cls.Meta.collection_name, key_fields=_keys, options=__option_keys)
                def get_cache_by_filter(*args, **kwargs):
                    return get_db()

                return get_cache_by_filter(**filter, options=options)
            return get_db()
        except cls.DoesNotExist:
            return {}
        except:
            capture_exception()
            traceback.print_exc()
            return {}

    @classmethod
    def get_by_id(cls, _id, with_cache=True):
        try:
            def get_db():
                try:
                    value = cls.objects.get({'_id': fields.ObjectId(_id)})
                    if value:
                        return value.to_dict()
                except cls.DoesNotExist:
                    return {}
                except:
                    sentry_sdk.capture_exception()
                    traceback.print_exc()
                return {}

            if with_cache:
                @cache_id(key_prefix=cls.Meta.collection_name)
                def get_cache_by_id(with_id):
                    return get_db()

                return get_cache_by_id(_id)
            return get_db()
        except:
            capture_exception()
            traceback.print_exc()
            return {}
