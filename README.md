# ComfyUI ExLlama Nodes
A simple text generator for [ComfyUI](https://github.com/comfyanonymous/ComfyUI) utilizing [ExLlamaV2](https://github.com/turboderp/exllamav2).

## Installation
Navigate to the root ComfyUI directory and clone the repository to `custom_nodes`:
```
git clone https://github.com/Zuellni/ComfyUI-ExLlama-Nodes custom_nodes/ComfyUI-ExLlama-Nodes
```

Install the requirements depending on your system:
```
pip install -r custom_nodes/ComfyUI-ExLlama-Nodes/requirements-VERSION.txt
```

`requirements-no-wheels.txt` contains JIT version of ExLlamaV2 and [Flash Attention](https://github.com/Dao-AILab/flash-attention).<br>
`requirements-torch-21.txt` contains Windows wheels for Python 3.11, Torch 2.1, CUDA 12.1.<br>
`requirements-torch-22.txt` contains Windows wheels for Python 3.11, Torch 2.2, CUDA 12.1.

Check what you need with:
```
python -c "import platform; import torch; print(f'Python {platform.python_version()}, Torch {torch.__version__}, CUDA {torch.version.cuda}')"
```

> [!CAUTION]
> If none of the included wheels work for you or there are any ExLlama-related errors while the nodes are loading, try to install it manually following the [official instructions](https://github.com/turboderp/exllamav2#installation). Keep in mind that wheels >= `0.0.13` require Torch 2.2.

## Usage
Only EXL2 and 4-bit GPTQ models are supported. You can find a lot of them on [Hugging](https://huggingface.co/LoneStriker) [Face](https://huggingface.co/TheBloke). Refer to the model card in each repository for details about quant differences and instruction formats.

To use a model with the nodes, you should clone its repository with git or manually download all the files and place them in `models/llm`. For example, if you'd like to download [Mistral-7B](https://huggingface.co/LoneStriker/Mistral-7B-Instruct-v0.2-5.0bpw-h6-exl2-2), use the following command:
```
git clone https://huggingface.co/LoneStriker/Mistral-7B-Instruct-v0.2-5.0bpw-h6-exl2-2 models/llm/mistral-7b-exl2-b5
```
> [!TIP]
> You can add your own `llm` path to the [extra_model_paths.yaml](https://github.com/comfyanonymous/ComfyUI/blob/master/extra_model_paths.yaml.example) file and place the models there instead.

## Nodes
<table>
  <tr>
    <td><b>Loader</b></td>
    <td colspan="2">Loads models from the <code>llm</code> directory.</td>
  </tr>
  <tr>
    <td></td>
    <td><i>gpu_split</i></td>
    <td>Comma-separated VRAM in GB per GPU, eg <code>6.9, 8</code>.</td>
  </tr>
  <tr>
    <td></td>
    <td><i>cache_8bit</i></td>
    <td>Lower VRAM usage but also lower speed.</td>
  </tr>
  <tr>
    <td></td>
    <td><i>max_seq_len</i></td>
    <td>Max context, higher number equals higher VRAM usage. <code>0</code> will default to config.</td>
  </tr>
  <tr>
    <td><b>Generator</b></td>
    <td colspan="2">Generates text based on the given prompt. Refer to <a href="https://github.com/oobabooga/text-generation-webui/wiki/03-%E2%80%90-Parameters-Tab#parameters-description">text-generation-webui</a> for parameters.</td>
  </tr>
  <tr>
    <td></td>
    <td><i>unload</i></td>
    <td>Unloads the model after each generation.</td>
  </tr>
  <tr>
    <td></td>
    <td><i>single_line</i></td>
    <td>Stops the generation on newline.</td>
  </tr>
  <tr>
    <td></td>
    <td><i>max_tokens</i></td>
    <td>Max new tokens, <code>0</code> will use available context.</td>
  </tr>
  <tr>
    <td><b>Preview</b></td>
    <td colspan="2">Displays generated text in the UI.</td>
  </tr>
  <tr>
    <td><b>Replace</b></td>
    <td colspan="2">Replaces variable names enclosed in brackets, eg <code>[a]</code>, with their values.</td>
  </tr>
</table>

## Workflow
The example workflow is embedded in the image below and can be opened in ComfyUI.

![workflow](https://github.com/Zuellni/ComfyUI-ExLlama-Nodes/assets/123005779/f9a42a5b-e708-4cc4-98c3-20bf11c6233a)
