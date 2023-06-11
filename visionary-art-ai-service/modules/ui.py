import os
import mimetypes

import gradio as gr
import gradio.routes
import gradio.utils

import modules
import modules.ui_common
from modules import localization, shared
from modules.ui_components import ToolButton, FormRow, FormGroup
from modules.sd_samplers import samplers
from modules.paths_internal import script_path, data_path
from modules.scripts import list_files_with_name
from modules.call_queue import wrap_gradio_gpu_call, wrap_queued_call, wrap_gradio_call
from modules.shared import opts

from initialize import initialize
from utils.txt2img import txt2img, img2img

mimetypes.init()
mimetypes.add_type('application/javascript', '.js')

random_symbol = '\U0001f3b2\ufe0f'  # 🎲️
reuse_symbol = '\u267b\ufe0f'  # ♻️
paste_symbol = '\u2199\ufe0f'  # ↙
refresh_symbol = '\U0001f504'  # 🔄
save_style_symbol = '\U0001f4be'  # 💾
apply_style_symbol = '\U0001f4cb'  # 📋
clear_prompt_symbol = '\U0001f5d1\ufe0f'  # 🗑️
extra_networks_symbol = '\U0001F3B4'  # 🎴
switch_values_symbol = '\U000021C5'  # ⇅
folder_symbol = '\U0001f4c2'  # 📂

GradioTemplateResponseOriginal = gradio.routes.templates.TemplateResponse


def gr_show(visible=True):
    return {"visible": visible, "__type__": "update"}


def create_checkpoint_refresh_button(refresh_component, refresh_method, refreshed_args, elem_id, refresh_js_method=None, inputs=[]):
    def refresh(*args):
        refresh_method() if callable(refresh_method) else None

        args = refreshed_args() if callable(refreshed_args) else refreshed_args

        for k, v in args.items():
            setattr(refresh_component, k, v)

    refresh_button = ToolButton(value=refresh_symbol, elem_id=elem_id)
    refresh_button.click(
        fn=refresh,
        _js=refresh_js_method,
        inputs=inputs,
        outputs=[]
    )
    return refresh_button


def create_sampler_and_steps_selection(choices, tabname):
    with FormGroup(elem_id=f"sampler_selection_{tabname}"):
        steps = gr.Slider(interactive=True, minimum=1, maximum=30, step=1,
                          elem_id=f"{tabname}_steps", label="Sampling steps", value=20)
        sampler_index = gr.Radio(interactive=True, label='Sampling method', elem_id=f"{tabname}_sampling", choices=[
            x.name for x in choices], value=choices[0].name, type="index")

    return steps, sampler_index


def create_toprow(is_img2img):
    id_part = "img2img" if is_img2img else "txt2img"

    with gr.Row(elem_id=f"{id_part}_toprow", variant="compact"):
        with gr.Column(elem_id=f"{id_part}_prompt_container", scale=6):
            with gr.Row():
                with gr.Column(scale=80):
                    with gr.Row():
                        prompt = gr.Textbox(label="Prompt", elem_id=f"{id_part}_prompt", show_label=False,
                                            lines=3, placeholder="Prompt (press Ctrl+Enter or Alt+Enter to generate)")

            with gr.Row():
                with gr.Column(scale=80):
                    with gr.Row():
                        negative_prompt = gr.Textbox(
                            label="Negative prompt", elem_id=f"{id_part}_neg_prompt", show_label=False, lines=3, placeholder="Negative prompt (press Ctrl+Enter or Alt+Enter to generate)")

        button_interrogate = None
        button_deepbooru = None
        # if is_img2img:
        #     with gr.Column(scale=1, elem_classes="interrogate-col"):
        #         button_interrogate = gr.Button(
        #             'Interrogate\nCLIP', elem_id="interrogate")
        #         button_deepbooru = gr.Button(
        #             'Interrogate\nDeepBooru', elem_id="deepbooru")

        with gr.Column(scale=1, elem_id=f"{id_part}_actions_column"):
            with gr.Row(elem_id=f"{id_part}_generate_box", elem_classes="generate-box"):
                interrupt = gr.Button(
                    'Interrupt', elem_id=f"{id_part}_interrupt", elem_classes="generate-box-interrupt")
                skip = gr.Button(
                    'Skip', elem_id=f"{id_part}_skip", elem_classes="generate-box-skip")
                submit = gr.Button(
                    'Generate', elem_id=f"{id_part}_generate", variant='primary')

                skip.click(
                    fn=lambda: shared.state.skip(),
                    inputs=[],
                    outputs=[],
                )

                interrupt.click(
                    fn=lambda: shared.state.interrupt(),
                    inputs=[],
                    outputs=[],
                )

            with gr.Row(elem_id=f"{id_part}_tools"):
                clear_prompt_button = ToolButton(
                    value=clear_prompt_symbol, elem_id=f"{id_part}_clear_prompt")

                token_counter = gr.HTML(
                    value="<span>0/75</span>", elem_id=f"{id_part}_token_counter", elem_classes=["token-counter"])
                token_button = gr.Button(
                    visible=False, elem_id=f"{id_part}_token_button")
                negative_token_counter = gr.HTML(
                    value="<span>0/75</span>", elem_id=f"{id_part}_negative_token_counter", elem_classes=["token-counter"])
                negative_token_button = gr.Button(
                    visible=False, elem_id=f"{id_part}_negative_token_button")

                def clear_prompt(prompt, negative_prompt):
                    prompt = ""
                    negative_prompt = ""
                    return prompt, negative_prompt

                clear_prompt_button.click(
                    fn=clear_prompt,
                    inputs=[prompt, negative_prompt],
                    outputs=[prompt, negative_prompt],
                )

    return prompt, negative_prompt, submit, button_interrogate, button_deepbooru, token_counter, token_button, negative_token_counter, negative_token_button


def create_seed_inputs(target_interface):
    with FormRow(elem_id=target_interface + '_seed_row', variant="compact"):
        seed = (gr.Number)(label='Seed', value=-1,
                           elem_id=target_interface + '_seed')
        seed.style(container=False)
        random_seed = ToolButton(
            random_symbol, elem_id=target_interface + '_random_seed')
        reuse_seed = ToolButton(
            reuse_symbol, elem_id=target_interface + '_reuse_seed')

    random_seed.click(fn=lambda: -1, show_progress=False,
                      inputs=[], outputs=[seed])

    return seed, reuse_seed


def create_output_panel(tabname):
    return modules.ui_common.create_output_panel(tabname)


def webpath(fn):
    if fn.startswith(script_path):
        web_path = os.path.relpath(fn, script_path).replace('\\', '/')
    else:
        web_path = os.path.abspath(fn)

    return f'file={web_path}?{os.path.getmtime(fn)}'


def javascript_html():
    script_js = os.path.join(script_path, "script.js")
    head = f'<script type="text/javascript" src="{webpath(script_js)}"></script>\n'

    inline = f"{localization.localization_js(shared.opts.localization)};"

    for script in modules.scripts.list_scripts("javascript", ".js"):
        head += f'<script type="text/javascript" src="{webpath(script.path)}"></script>\n'

    for script in modules.scripts.list_scripts("javascript", ".mjs"):
        head += f'<script type="module" src="{webpath(script.path)}"></script>\n'

    head += f'<script type="text/javascript">{inline}</script>\n'

    return head


def css_html():
    head = ""

    def stylesheet(fn):
        return f'<link rel="stylesheet" property="stylesheet" href="{webpath(fn)}">'

    for cssfile in list_files_with_name("style.css"):
        if not os.path.isfile(cssfile):
            continue

        head += stylesheet(cssfile)

    if os.path.exists(os.path.join(data_path, "user.css")):
        head += stylesheet(os.path.join(data_path, "user.css"))

    return head


def reload_javascript():
    js = javascript_html()
    css = css_html()

    def template_response(*args, **kwargs):
        res = shared.GradioTemplateResponseOriginal(*args, **kwargs)
        res.body = res.body.replace(b'</head>', f'{js}</head>'.encode("utf8"))
        res.body = res.body.replace(b'</body>', f'{css}</body>'.encode("utf8"))
        res.init_headers()
        return res

    gradio.routes.templates.TemplateResponse = template_response


if not hasattr(shared, 'GradioTemplateResponseOriginal'):
    shared.GradioTemplateResponseOriginal = gradio.routes.templates.TemplateResponse


def create_webui():
    reload_javascript()

    # create txt2img interface
    with gr.Blocks(analytics_enabled=False) as txt2img_interface:
        # Basic components
        txt2img_prompt, txt2img_negative_prompt, txt2img_submit, button_interrogate, button_deepbooru, token_counter, token_button, negative_token_counter, negative_token_button = create_toprow(
            is_img2img=False)

        dummy_component = gr.Label(visible=False)

        txt_prompt_img = gr.File(label="", elem_id="txt2img_prompt_image",
                                 file_count="single", type="binary", visible=False)

        with FormRow(elem_classes="checkboxes-row", variant="compact"):
            txt2img_restore_faces = gr.Checkbox(label='Restore faces', value=False, visible=len(
                shared.face_restorers) > 1, elem_id="txt2img_restore_faces")
            txt2img_tiling = gr.Checkbox(label='Tiling', value=False,
                                         elem_id="txt2img_tiling")
            txt2img_enable_hr = gr.Checkbox(
                label='Hires. fix', value=False, elem_id="txt2img_enable_hr")

        with gr.Row().style(equal_height=False):
            with gr.Column(variant='compact', elem_id="txt2img_settings"):
                txt2img_steps, txt2img_sampler_index = create_sampler_and_steps_selection(
                    samplers, "txt2img")

                with FormRow():
                    with gr.Column(elem_id="txt2img_column_size", scale=4):
                        txt2img_width = gr.Slider(
                            minimum=64, maximum=512, step=8, label="Width", value=512, elem_id="txt2img_width")
                        txt2img_height = gr.Slider(
                            minimum=64, maximum=512, step=8, label="Height", value=512, elem_id="txt2img_height")

                    with gr.Column(elem_id="txt2img_column_batch"):
                        txt2img_batch_count = gr.Slider(
                            minimum=1, step=1, label='Batch count', value=1, elem_id="txt2img_batch_count")
                        txt2img_batch_size = gr.Slider(
                            minimum=1, maximum=3, step=1, label='Batch size', value=1, elem_id="txt2img_batch_size")

                txt2img_cfg_scale = gr.Slider(minimum=1.0, maximum=30.0, step=0.5,
                                              label='CFG Scale', value=7.0, elem_id="txt2img_cfg_scale")
                txt2img_seed, txt2img_reuse_seed = create_seed_inputs(
                    'txt2img')

            txt2img_gallery, txt2img_generation_info, txt2img_html_info, txt2img_html_log = create_output_panel(
                "txt2img")

    # create img2img interface
    with gr.Blocks(analytics_enabled=False) as img2img_interface:
        img2img_prompt, img2img_negative_prompt, img2img_submit, img2img_interrogate, img2img_deepbooru, token_counter, token_button, negative_token_counter, negative_token_button = create_toprow(
            is_img2img=True)

        img2img_prompt_img = gr.File(
            label="", elem_id="img2img_prompt_image", file_count="single", type="binary", visible=False)
        # 0062cctx
        # drop image controller
        copy_image_buttons = []
        copy_image_destinations = {}

        img2img_init_img = gr.Image(label="Image for img2img", elem_id="img2img_image", show_label=False,
                                    source="upload", interactive=True, type="pil", tool="editor", image_mode="RGBA").style(height=480)

        with FormRow(elem_classes="checkboxes-row", variant="compact"):
            img2img_restore_faces = gr.Checkbox(label='Restore faces', value=False, visible=len(
                shared.face_restorers) > 1, elem_id="img2img_restore_faces")
            img2img_tiling = gr.Checkbox(label='Tiling', value=False,
                                         elem_id="img2img_tiling")

        with gr.Row().style(equal_height=False):
            with gr.Column(variant='compact', elem_id="img2img_settings"):
                img2img_steps, img2img_sampler_index = create_sampler_and_steps_selection(
                    samplers, "img2img")

                with FormRow():
                    with gr.Column(elem_id="img2img_column_size", scale=4):
                        img2img_width = gr.Slider(
                            minimum=64, maximum=512, step=8, label="Width", value=512, elem_id="img2img_width")
                        img2img_height = gr.Slider(
                            minimum=64, maximum=512, step=8, label="Height", value=512, elem_id="img2img_height")

                    with gr.Column(elem_id="img2img_column_batch"):
                        img2img_batch_count = gr.Slider(
                            minimum=1, step=1, label='Batch count', value=1, elem_id="img2img_batch_count")
                        img2img_batch_size = gr.Slider(
                            minimum=1, maximum=3, step=1, label='Batch size', value=1, elem_id="img2img_batch_size")

                img2img_cfg_scale = gr.Slider(minimum=1.0, maximum=30.0, step=0.5,
                                              label='CFG Scale', value=7.0, elem_id="img2img_cfg_scale")
                img2img_seed, img2img_reuse_seed = create_seed_inputs(
                    'img2img')

            img2img_gallery, img2img_generation_info, img2img_html_info, img2img_html_log = create_output_panel(
                "img2img")

    interfaces = [
        (txt2img_interface, "txt2img", "txt2img"),
        (img2img_interface, "img2img", "img2img"),
    ]

    with gr.Blocks(analytics_enabled=False, title="Stable Diffusion") as webui:
        with gr.Row(elem_id="quicksettings", variant="compact"):
            def list_checkpoint_tiles():
                import modules.sd_models
                return modules.sd_models.checkpoint_tiles()

            # def refresh_checkpoints():
            #     import modules.sd_models
            #     return modules.sd_models.list_models_with_filter(1, 'Checkpoint', sd_model_list_option.value)

            # def get_first_checkpoint_value():
            #     sd_model_checkpoint_choices = list_checkpoint_tiles()
            #     if len(sd_model_checkpoint_choices) == 0:
            #         return 'No results'
            #     else:
            #         return sd_model_checkpoint_choices[0]

            # sd_model_checkpoint_choices = list_checkpoint_tiles()
            sd_model_checkpoint_choices = []
            sd_model_checkpoint = gr.Dropdown(interactive=True, label="Stable Diffusion checkpoint", choices=sd_model_checkpoint_choices,
                                              value="Loading...", elem_id="setting_" + "sd_model_checkpoint")
            model_not_loadable_warning = gr.Text(interactive=False, label="Notice: ", placeholder="If you select a model which has invalid file format and try to generate image with it, visionary art will use default SD1.5 model instead.")
            sd_model_list_option = gr.Radio(interactive=True, label='Model Filter', elem_id=f"sd_model_list_option", choices=[
                'All', 'Uploaded', 'Liked'], value='All', type="value")
            
            refresh_button = ToolButton(value=refresh_symbol, elem_id="refresh_" + "sd_model_checkpoint")
            refresh_button.click(
                fn=None,
                _js="refreshCheckpoints",
                inputs=[sd_model_list_option],
                outputs=[sd_model_checkpoint]
            )
            # create_checkpoint_refresh_button(sd_model_checkpoint, None, None, "refresh_" + "sd_model_checkpoint", "refreshCheckpoints", [sd_model_list_option])

            def onRadioChange(choice):
                setattr(sd_model_list_option, 'value', choice)
                return choice

            sd_model_list_option.change(
                fn=onRadioChange,
                inputs=sd_model_list_option,
                outputs=sd_model_list_option
            )

        with gr.Tabs(elem_id="tabs") as tabs:
            for interface, label, ifid in interfaces:
                with gr.TabItem(label, id=ifid, elem_id='tab_' + ifid):
                    interface.render()

        txt2img_args = dict(
            # fn=txt2img,
            fn=wrap_gradio_gpu_call(txt2img, extra_outputs=[None, '', '']),
            _js="submit",
            inputs=[
                dummy_component,
                sd_model_checkpoint,
                txt2img_prompt,
                txt2img_negative_prompt,
                txt2img_steps,
                txt2img_sampler_index,
                txt2img_batch_count,
                txt2img_batch_size,
                txt2img_cfg_scale,
                txt2img_seed,
                txt2img_height,
                txt2img_width,
                txt2img_enable_hr,
                txt2img_tiling,
                txt2img_restore_faces
                # denoising_strength,
                # hr_scale,
                # hr_upscaler,
                # hr_second_pass_steps,
                # hr_resize_x,
                # hr_resize_y,
                # override_settings,
            ],

            outputs=[
                txt2img_gallery,
                txt2img_generation_info,
                txt2img_html_info,
                txt2img_html_log,
            ],

            show_progress=False,
        )

        txt2img_submit.click(**txt2img_args)

        img2img_args = dict(
            # fn=txt2img,
            fn=wrap_gradio_gpu_call(img2img, extra_outputs=[None, '', '']),
            _js="submit_img2img",
            inputs=[
                dummy_component,
                sd_model_checkpoint,
                img2img_init_img,
                img2img_prompt,
                img2img_negative_prompt,
                img2img_steps,
                img2img_sampler_index,
                img2img_batch_count,
                img2img_batch_size,
                img2img_cfg_scale,
                img2img_seed,
                img2img_height,
                img2img_width,
                img2img_tiling,
                img2img_restore_faces
                # denoising_strength,
                # hr_scale,
                # hr_upscaler,
                # hr_second_pass_steps,
                # hr_resize_x,
                # hr_resize_y,
                # override_settings,
            ],

            outputs=[
                img2img_gallery,
                img2img_generation_info,
                img2img_html_info,
                img2img_html_log,
            ],

            show_progress=False,
        )

        img2img_submit.click(**img2img_args)

        text_settings = gr.Textbox(
            elem_id="settings_json", value=lambda: opts.dumpjson(), visible=False)

        text_uid = gr.Textbox(
            elem_id="elem_uid", value="0", visible=True, interactive=True)

        text_session_key = gr.Textbox(
            elem_id="elem_session_key", value="", visible=True, interactive=True)

    return webui


if __name__ == '__main__':
    webui = create_webui()
    webui.launch(shared=False, show_api=False,
                 server_name="0.0.0.0", server_port=7860)
