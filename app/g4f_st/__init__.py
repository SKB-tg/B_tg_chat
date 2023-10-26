import sys
from . import GetGpt
#from g4f.models import Model, ModelUtils
from app.g4f_st.GetGpt import _create_completion
import os
import json
import uuid
import requests
from Crypto.Cipher import AES
from typing import Dict, NewType, Union, Optional, List, get_type_hints

sha256 = NewType('sha_256_hash', str)
logging = False




class Model:
    class model:
        name: str
        base_provider: str
        best_provider: str

    class gpt_35_turbo:
        name: str = 'gpt-3.5-turbo'
        base_provider: str = 'openai'
        best_provider = GetGpt

class ModelUtils:
    convert: dict = {
        'gpt-3.5-turbo': Model.gpt_35_turbo,}

class ChatCompletions:
    @staticmethod
    def create(model: Model.model or str, messages: list, provider = 'GetGpt', stream: bool = False, auth: str = False, **kwargs):
        # kwargs['auth'] = auth
        # if provider and provider.working == False:
        #     return f'{provider.__name__} is not working'

        # if provider and provider.needs_auth and not auth:
        #     print(
        #         f'ValueError: {provider.__name__} requires authentication (use auth="cookie or token or jwt ..." param)', file=sys.stderr)
        #     sys.exit(1)

        try:
            if isinstance(model, str):
                try:
                    model = ModelUtils.convert[model]
                except KeyError:
                    raise Exception(f'The model: {model} does not exist')
            engine = model.best_provider if not provider else provider
            print(500, model.name, engine)

            # if not engine.supports_stream and stream == True:
            #     print(
            #         f"ValueError: {engine.__name__} does not support 'stream' argument", file=sys.stderr)
            #     sys.exit(1)

            if logging: print(f'Using {engine} provider')

            return (GetGpt._create_completion(model.name, messages, stream, **kwargs)
                    if stream else ''.join(GetGpt._create_completion(model.name, messages, stream, **kwargs)))
        except TypeError as e:
            print(400, e)
            arg: str = str(e).split("'")
            print(
                f"ValueError: {engine} does not support '{arg}' argument", file=sys.stderr)
            sys.exit(1)
