# ComfyUI ExLlama Nodes
A simple prompt generator for [ComfyUI](https://github.com/comfyanonymous/ComfyUI) using [ExLlama](https://github.com/turboderp/exllama).

## Installation
Clone the repository to `custom_nodes` in your ComfyUI directory and install dependencies:
```
git clone https://github.com/Zuellni/ComfyUI-ExLlama-Nodes
python -m pip install -r requirements.txt
```

If you see any ExLlama-related errors while loading, manually install the wheel matching your system from [here](https://github.com/jllllll/exllama/releases/latest).
For example, on Windows with Python 3.10 and PyTorch CUDA 11.7:
```
python -m pip install https://github.com/jllllll/exllama/releases/download/0.0.17/exllama-0.0.17+cu117-cp310-cp310-win_amd64.whl
```

## Nodes
Name | Description
:--- | :---
Loader | Used to load 4-bit GPTQ Llama/2 models. You can find a lot of them on [Hugging Face](https://huggingface.co/TheBloke).<br>Clone the model repository or download all the files in it and place them in an empty directory, then specify the path in `model_dir`. The `model.safetensors` file won't work on its own.<br><br>ExLlama allocates memory based on `max_seq_len`. Lowering it is a good way to save on VRAM. It's currently not possible to [offload](https://github.com/turboderp/exllama/issues/177) the model to RAM.
LoRA Loader | Used to load LoRAs. Specify the directory in `lora_dir`, it should contain `adapter_model.bin` and `adapter_config.json`. LoRA parameter count has to match the model.
Generator | Generates a `string` based on the given `prompt` for use with other nodes. Default values correspond to the `simple-1` preset from [text-generation-webui](https://github.com/oobabooga/text-generation-webui). ExLlama isn't [deterministic](https://github.com/turboderp/exllama/issues/201), so the outputs may differ even with the same seed.
Previewer | Displays generated outputs in the UI.

## Workflow
The workflow below can be opened in ComfyUI. Peak VRAM usage with SDXL around 10GB. Model: [MythoLogic-Mini-7B](https://huggingface.co/TheBloke/MythoLogic-Mini-7B-GPTQ).

![workflow](https://github.com/Zuellni/ComfyUI-ExLlama-Nodes/assets/123005779/c6821ba6-3a7a-4dd2-9852-372f79f63569)
