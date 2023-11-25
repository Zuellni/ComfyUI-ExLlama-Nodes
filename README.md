# ComfyUI ExLlama Nodes
A simple text generator for [ComfyUI](https://github.com/comfyanonymous/ComfyUI) utilizing [ExLlamaV2](https://github.com/turboderp/exllamav2).

## Installation
Navigate to the root ComfyUI directory, clone the repository to `custom_nodes` and install dependencies:
```
git clone https://github.com/Zuellni/ComfyUI-ExLlama-Nodes custom_nodes/ComfyUI-ExLlama-Nodes
pip install -r custom_nodes/ComfyUI-ExLlama-Nodes/requirements.txt
```
Optionally, you can install [flash-attention](https://github.com/Dao-AILab/flash-attention) by uncommenting the relevant lines in the requirements file. It should lower VRAM usage but your mileage may vary.
> [!IMPORTANT]
> The wheels included in the requirements file should match the latest portable ComfyUI build. If you see any ExLlama-related errors while loading the nodes, try to install it manually following the [official instructions](https://github.com/turboderp/exllamav2#installation).

## Usage
Only EXL2 and 4-bit GPTQ models are supported. You can find a lot of them on [Hugging Face](https://huggingface.co/TheBloke). Refer to the model card in each repository for details about quant differences and instruction formats.

To use a model with the nodes, you should clone its repository with git or manually download all the files and place them in `models/llm`. For example, if you'd like to download the 4-bit 32g version of [Zephyr 7B Beta](https://huggingface.co/TheBloke/zephyr-7B-beta-GPTQ), use the following command:
```
git clone https://huggingface.co/TheBloke/zephyr-7B-beta-GPTQ -b gptq-4bit-32g-actorder_True models/llm/zephyr-7b-gptq-32g
```
> [!TIP]
> You can add your own `llm` path to the [extra_model_paths.yaml](https://github.com/comfyanonymous/ComfyUI/blob/master/extra_model_paths.yaml.example) file and place the models there instead.

## Nodes
Name | Description
:--- | :---
Loader | Loads models from the `llm` directory.<br>`gpu_split` - comma-separated VRAM in GB per GPU, eg `6.9, 8`, if using more than one.<br>`cache_8bit` - lower VRAM usage but also lower speed if set to `True`.<br>`max_seq_len` - max context length, higher number equals higher VRAM usage. Setting it to `0` will make the model use the default context length from its config file.
Generator | Generates text based on the given prompt. Refer to [text-generation-webui](https://github.com/oobabooga/text-generation-webui/wiki/03-%E2%80%90-Parameters-Tab#parameters-description) for parameter explanations.<br>`unload` - unloads the model after each generation if set to `True`, freeing all the VRAM used.<br>`single_line` - stops generation on new line.<br>`max_tokens` - max new tokens to generate, setting it to `0` will make the model use all available context.
Preview | Displays generated text in the UI.
Replace | Replaces variable names enclosed in brackets, such as `[a]`, with their values.

## Workflow
The example workflow is embedded in the image below and can be opened in ComfyUI.

![workflow](https://github.com/Zuellni/ComfyUI-ExLlama-Nodes/assets/123005779/cb20b040-9856-4dab-aed0-4b318bc2d805)
