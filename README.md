# ComfyUI ExLlamaV2 Nodes
A simple local text generator for [ComfyUI](https://github.com/comfyanonymous/ComfyUI) using [ExLlamaV2](https://github.com/turboderp/exllamav2).

## Installation
Clone the repository to `custom_nodes` and install the requirements:
```
git clone https://github.com/Zuellni/ComfyUI-ExLlama-Nodes custom_nodes/ComfyUI-ExLlamaV2-Nodes
pip install -r custom_nodes/ComfyUI-ExLlamaV2-Nodes/requirements.txt
```

Use wheels for [ExLlamaV2](https://github.com/turboderp/exllamav2/releases/latest) and [Flash Attention](https://github.com/bdashore3/flash-attention/releases/latest) on Windows:
```
pip install exllamav2-X.X.X+cuXXX.torch2.X.X-cp3XX-cp3XX-win_amd64.whl
pip install flash_attn-X.X.X+cuXXX.torch2.X.X-cp3XX-cp3XX-win_amd64.whl
```

## Usage
Only EXL2, 4-bit GPTQ and unquantized models are supported. You can find them on [Hugging Face](https://huggingface.co).

To use a model with the nodes, you should clone its repository with `git` or manually download all the files and place them in `models/llm`.
For example, if you want to download the 6-bit [Llama-3-8B-Instruct](https://huggingface.co/turboderp/Llama-3-8B-Instruct-exl2), use the following command:
```
git install lfs
git clone https://huggingface.co/turboderp/Llama-3-8B-Instruct-exl2 -b 6.0bpw models/llm/Llama-3-8B-Instruct-exl2-6.0bpw
```

> [!TIP]
> You can add your own `llm` path to the [extra_model_paths.yaml](https://github.com/comfyanonymous/ComfyUI/blob/master/extra_model_paths.yaml.example) file and put the models there instead.

## Nodes
<table>
  <tr>
    <td><b>Loader</b></td>
    <td colspan="2">Loads models from the <code>llm</code> directory.</td>
  </tr>
  <tr>
    <td></td>
    <td><i>cache_bits</i></td>
    <td>A lower value reduces VRAM usage, but also affects generation speed and quality.</td>
  </tr>
  <tr>
    <td></td>
    <td><i>fast_tensors</i></td>
    <td>Enabling reduces RAM usage and speeds up model loading.</td>
  </tr>
  <tr>
    <td></td>
    <td><i>flash_attention</i></td>
    <td>Enabling reduces VRAM usage, not supported on cards with compute capability below <code>8.0</code>.</td>
  </tr>
  <tr>
    <td></td>
    <td><i>max_seq_len</i></td>
    <td>Max context, higher value equals higher VRAM usage. <code>0</code> will default to model config.</td>
  </tr>
  <tr>
    <td><b>Generator</b></td>
    <td colspan="2">Generates text based on the given prompt. Refer to <a href="https://docs.sillytavern.app/usage/common-settings/#sampler-parameters">SillyTavern</a> for sampler parameters.</td>
  </tr>
  <tr>
    <td></td>
    <td><i>unload</i></td>
    <td>Unloads the model after each generation to reduce VRAM usage.</td>
  </tr>
  <tr>
    <td></td>
    <td><i>stop_conditions</i></td>
    <td>List of strings to stop generation on, e.g. <code>["\n"]</code> to stop on newline. Leave empty to only stop on <code>eos</code> token.</td>
  </tr>
  <tr>
    <td></td>
    <td><i>max_tokens</i></td>
    <td>Max new tokens, <code>0</code> will use available context.</td>
  </tr>
  <tr>
    <td><b>Previewer</b></td>
    <td colspan="2">Displays generated text in the UI.</td>
  </tr>
  <tr>
    <td><b>Replacer</b></td>
    <td colspan="2">Replaces variable names in brackets, e.g. <code>[a]</code>, with their values.</td>
  </tr>
</table>

## Workflow
An example workflow is embedded in the image below and can be opened in ComfyUI.

![workflow](https://github.com/Zuellni/ComfyUI-ExLlama-Nodes/assets/123005779/bf688acb-6f7a-4410-98ff-cf22b6937ae7)
