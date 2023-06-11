import requests
import json
from modules import shared
from modules.sd_models import checkpoint_alisases, checkpoints_list, CheckpointInfo, list_models_from_local_files
from pydantic import BaseModel, Field
import gradio as gr

host_url = "http://127.0.0.1:" + shared.opts.visionary_art_server_port


class ModelListFilter(BaseModel):
    uid: str = Field(title="uid")
    session_key: str = Field(title="session_key")
    model_type: str = Field(title="model_type")
    list_type: str = Field(title="list_type")


class ModelListResponse(BaseModel):
    models: dict = Field(default=None, title="models",
                         description="List results")


def list_models(req: ModelListFilter):
    list_models_from_local_files()

    url = "{0}/model/list?uid={1}&session_key={2}&list_type={3}&model_type={4}".format(
        host_url, req.uid, req.session_key, req.list_type, req.model_type
    )

    payload = {}
    headers = {
        'Accept': '*/*',
        'Connection': 'keep-alive'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    model_list = json.loads(response.content).get('data')
    res = []
    for model in model_list:
        res.append(model['path'])

    models = []
    for filename in sorted(res, key=str.lower):
        checkpoint_info = CheckpointInfo(filename)
        models.append(checkpoint_info.title)

    return ModelListResponse(models=gr.Dropdown.update(choices=models, value="No result" if len(models) == 0 else models[0], label="Stable Diffusion checkpoint", show_label=True))
