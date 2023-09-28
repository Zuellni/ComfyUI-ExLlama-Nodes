# ComfyUI ExLlama Nodes
A simple prompt generator for [ComfyUI](https://github.com/comfyanonymous/ComfyUI) utilizing [ExLlama](https://github.com/turboderp/exllamav2).

## Installation
Clone the repository to `custom_nodes` in your ComfyUI directory and install dependencies:
```
git clone https://github.com/Zuellni/ComfyUI-ExLlama-Nodes
pip install -r requirements.txt
```

If you see any ExLlama errors while loading, install it manually from [here](https://github.com/turboderp/exllamav2/releases/latest).<br>
For example, on Windows with Python 3.10 and CUDA 11.7:
```
pip install https://github.com/turboderp/exllamav2/releases/download/v0.0.4/exllamav2-0.0.4+cu117-cp310-cp310-win_amd64.whl
```

## Nodes
Name | Description
:--- | :---
Loader | Loads EXL2/GPTQ Llama models. You can find a lot of them on [Hugging Face](https://huggingface.co/TheBloke).<br>Clone the model repository or download all the files and place them in an empty directory, then specify the path in `model_dir`. The `model.safetensors` file won't work on its own.<br><br>ExLlama allocates memory based on `max_seq_len`. Lowering it is a good way to save on VRAM.<br>It's currently not possible to offload the model to RAM.
Generator | Generates a `string` based on the given `prompt` for use with other nodes.<br>Default values correspond to the `simple-1` preset from [text-generation-webui](https://github.com/oobabooga/text-generation-webui).<br><br>ExLlama isn't deterministic, so the outputs may differ even with the same seed.
Previewer | Displays generated outputs in the UI and appends them to workflow metadata.

## Workflow
The workflow below can be opened in ComfyUI.<br>
Only around 3GB VRAM usage without SDXL.<br>
Model: [Mistral-7B-instruct-exl2-2.5bpw](https://huggingface.co/turboderp/Mistral-7B-instruct-exl2/tree/2.5bpw).

![workflow](https://github.com/Zuellni/ComfyUI-ExLlama-Nodes/assets/123005779/09da1788-f879-4076-baea-b257dd682ded)
