# ComfyUI ExLlama Nodes
A simple prompt generator for [ComfyUI](https://github.com/comfyanonymous/ComfyUI) utilizing [ExLlamaV2](https://github.com/turboderp/exllamav2).

## Installation
Clone the repository to `custom_nodes` in your ComfyUI directory and install dependencies:
```
git clone https://github.com/Zuellni/ComfyUI-ExLlama-Nodes
python -m pip install -r requirements.txt
```

If you see any ExLlama errors while loading, install it manually from [here](https://github.com/turboderp/exllamav2/releases/latest).<br>
For example, on Windows with Python 3.10 and CUDA 11.7:
```
python -m pip install https://github.com/turboderp/exllamav2/releases/download/v0.0.4/exllamav2-0.0.4+cu117-cp310-cp310-win_amd64.whl
```

## Nodes
Name | Description
:--- | :---
Loader | Used to load 4-bit GPTQ Llama/2 models. You can find a lot of them on [Hugging Face](https://huggingface.co/TheBloke).<br>Clone the model repository or download all the files and place them in an empty directory, then specify the path in `model_dir`. The `model.safetensors` file won't work on its own.<br><br>ExLlama allocates memory based on `max_seq_len`. Lowering it is a good way to save on VRAM.<br>It's currently not possible to offload the model to RAM.
Generator | Generates a `string` based on the given `prompt` for use with other nodes.<br>Default values correspond to the `simple-1` preset from [text-generation-webui](https://github.com/oobabooga/text-generation-webui).<br><br>ExLlama isn't deterministic, so the outputs may differ even with the same seed.
Previewer | Displays generated outputs in the UI and appends them to workflow metadata.

## Workflow
The workflow below can be opened in ComfyUI. Peak VRAM usage with SDXL around 10GB.<br>
Model: [MythoLogic-Mini-7B-GPTQ](https://huggingface.co/TheBloke/MythoLogic-Mini-7B-GPTQ).

![workflow](https://github.com/Zuellni/ComfyUI-ExLlama-Nodes/assets/123005779/b0bfd1f5-c981-4aaa-9a15-9f208387f0d5)
