from asgiref.sync import sync_to_async
from django.core.cache import cache
from django.db import models


class AsyncCacheClient:
    @classmethod
    async def get(cls, key):
        return await sync_to_async(cache.get)(key)

    @classmethod
    async def set(cls, key, value, timeout=None):
        return await sync_to_async(cache.set)(key, value, timeout)
    
    @classmethod
    async def delete(cls, key):
        return await sync_to_async(cache.delete)(key)
    

class Repository:
    cache_client = AsyncCacheClient
    model: models.Model = None
    filter_cache_attr = ""
    detail_cache_attr = ""

    @classmethod
    async def get_id_cache_key(cls, *args, **kwargs):
        value = kwargs.get(cls.detail_cache_attr)
        if value:
            return f"{cls.model._meta.model_name}:{value}"
        return None
    
    @classmethod
    async def get_kwargs_cache_key(cls, **kwargs):        
        value = kwargs.get(cls.filter_cache_attr)
        if value:
            return f"{cls.model._meta.model_name}:filter:{value}"
        return None

    @classmethod
    async def get(cls, **kwargs):
        cache_key = await cls.get_id_cache_key(**kwargs)
        instance = None
        if cache_key:
            instance = await cls.cache_client.get(cache_key)
        if not instance:
            instance = await cls.model.objects.aget(**kwargs)
            await cls.cache_client.set(cache_key, instance)
        return instance
    
    @classmethod
    async def filter(cls, **kwargs):
        cache_key = await cls.get_kwargs_cache_key(**kwargs)
        instances = None
        if cache_key:
            instances = await cls.cache_client.get(cache_key)
        if not instances:
            instances = cls.model.objects.filter(**kwargs)
            if cache_key:
                await cls.cache_client.set(cache_key, instances)
        return instances

    @classmethod
    async def create(cls,**kwargs):        
        instance = kwargs.get("instance")
        if instance:
            await sync_to_async(instance.save)()
        else:
            instance = await cls.model.objects.acreate(**kwargs)
        cache_kwargs = {
            cls.detail_cache_attr: getattr(instance, cls.detail_cache_attr)
        }
        instance_cache_key = await cls.get_id_cache_key(**cache_kwargs)
        await cls.cache_client.set(instance_cache_key, instance)
        list_cache_key = await cls.get_kwargs_cache_key(**kwargs)
        if not list_cache_key:
            await cls.cache_client.delete(list_cache_key)
        return instance
    
    @classmethod
    async def update(cls, **kwargs):
        instance = kwargs.pop("instance", None)
        if instance:
            instance.update(**kwargs)
        else:
            instance = await cls.model.objects.aupdate(**kwargs)
        cache_kwargs = {
            cls.detail_cache_attr: getattr(instance, cls.detail_cache_attr)
        }
        instance_cache_key = await cls.get_id_cache_key(**cache_kwargs)
        await cls.cache_client.set(instance_cache_key, instance)
        list_cache_key = await cls.get_kwargs_cache_key(**cache_kwargs)
        await cls.cache_client.delete(list_cache_key)
        return instance

    @classmethod
    async def delete(cls, instance):
        cache_kwargs = {
            cls.detail_cache_attr: getattr(instance, cls.detail_cache_attr)
        }
        instance_cache_key = await cls.get_id_cache_key(**cache_kwargs)
        await cls.cache_client.delete(instance_cache_key)
        list_cache_key = await cls.get_kwargs_cache_key(**cache_kwargs)
        await cls.cache_client.delete(list_cache_key)
        instance.adelete()
