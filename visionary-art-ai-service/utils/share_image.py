from pydantic import BaseModel, Field
import requests
import json
from modules import shared

host_url = "http://127.0.0.1:" + shared.opts.visionary_art_server_port

class ImageShareItem(BaseModel):
    uid: str = Field(title="uid")
    session_key: str = Field(title="session_key")
    path: str = Field(title="path")
    generation_info_html: str = Field(title="generation_info_html")

class ImageShareResponse(BaseModel):
    msg: str = Field(default="Image shared successfully", title="Msg", description="Image sharing status.")

def share_image(req: ImageShareItem):
    url = "{0}/image/share?uid={1}&session_key={2}&path={3}".format(
        host_url, req.uid, req.session_key, req.path
    )

    payload = {'generation_info_html': req.generation_info_html}
    headers = {
        'Accept': '*/*',
        'Connection': 'keep-alive'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    msg = json.loads(response.content).get('msg')
    return ImageShareResponse(msg=msg)
