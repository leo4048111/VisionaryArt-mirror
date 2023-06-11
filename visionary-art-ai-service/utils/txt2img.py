import modules
from modules.api.api import encode_pil_to_base64
from modules import shared, sd_samplers
from modules.processing import StableDiffusionProcessingTxt2Img, process_images, StableDiffusionProcessingImg2Img
from modules.ui_common import plaintext_to_html
from modules.sd_models import get_closet_checkpoint_match, reload_model_weights
from modules.shared import opts, PROMPT_PREFIX, NEG_PROMPT_PREFIX

from PIL import Image, ImageOps

def txt2img(id_task: str, sd_model_checkpoint: str, prompt: str, negative_prompt: str, steps: int, sampler_index: int, n_iter: int, batch_size: int, cfg_scale: float, seed: int, height: int, width: int, enable_hr: bool, tiling: bool, restore_faces: bool):
    # override_settings = create_override_settings_dict(override_settings_texts)
    if sd_model_checkpoint == 'No results': return

    sd_model_info = get_closet_checkpoint_match(sd_model_checkpoint)
    sd_model = reload_model_weights(info=sd_model_info)

    prompt = PROMPT_PREFIX + prompt
    negative_prompt = NEG_PROMPT_PREFIX + negative_prompt

    p = StableDiffusionProcessingTxt2Img(
        sd_model=sd_model,
        outpath_samples=opts.outdir_samples or opts.outdir_txt2img_samples,
        outpath_grids=opts.outdir_grids or opts.outdir_txt2img_grids,
        prompt=prompt,
        negative_prompt=negative_prompt,
        seed=seed,
        sampler_name=sd_samplers.samplers[sampler_index].name,
        batch_size=batch_size,
        n_iter=n_iter,
        steps=steps,
        cfg_scale=cfg_scale,
        width=width,
        height=height,
        enable_hr=enable_hr,
        tiling=tiling,
        restore_faces=restore_faces,
        # denoising_strength=denoising_strength if enable_hr else None,
    )

    processed = process_images(p)

    p.close()

    shared.total_tqdm.clear()

    generation_info_js = processed.js()

    return processed.images, generation_info_js, plaintext_to_html(processed.info), plaintext_to_html(processed.comments)

def img2img(id_task: str, sd_model_checkpoint: str, init_image, prompt: str, negative_prompt: str, steps: int, sampler_index: int, n_iter: int, batch_size: int, cfg_scale: float, seed: int, height: int, width: int, tiling: bool, restore_faces: bool):
    # override_settings = create_override_settings_dict(override_settings_texts)
    if sd_model_checkpoint == 'No results': return

    sd_model_info = get_closet_checkpoint_match(sd_model_checkpoint)
    sd_model = reload_model_weights(info=sd_model_info)

    image = init_image.convert("RGB")
    # Use the EXIF orientation of photos taken by smartphones.
    if image is not None:
        image = ImageOps.exif_transpose(image)

    prompt = PROMPT_PREFIX + prompt
    negative_prompt = NEG_PROMPT_PREFIX + negative_prompt

    p = StableDiffusionProcessingImg2Img(
        sd_model=sd_model,
        outpath_samples=opts.outdir_samples or opts.outdir_txt2img_samples,
        outpath_grids=opts.outdir_grids or opts.outdir_txt2img_grids,
        init_images=[image],
        prompt=prompt,
        negative_prompt=negative_prompt,
        seed=seed,
        sampler_name=sd_samplers.samplers[sampler_index].name,
        batch_size=batch_size,
        n_iter=n_iter,
        steps=steps,
        cfg_scale=cfg_scale,
        width=width,
        height=height,
        tiling=tiling,
        restore_faces=restore_faces,
    )

    processed = process_images(p)

    p.close()

    shared.total_tqdm.clear()

    generation_info_js = processed.js()

    return processed.images, generation_info_js, plaintext_to_html(processed.info), plaintext_to_html(processed.comments)