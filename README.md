# ComfyUI ExLlama Nodes
A simple local text generator for [ComfyUI](https://github.com/comfyanonymous/ComfyUI) using [ExLlamaV2](https://github.com/turboderp/exllamav2).

## Installation
Clone the repository to `custom_nodes` and install the requirements:
```
cd custom_nodes
git clone https://github.com/Zuellni/ComfyUI-ExLlama-Nodes
pip install -r ComfyUI-ExLlama-Nodes/requirements.txt
```

Use wheels for [ExLlamaV2](https://github.com/turboderp/exllamav2/releases/latest) and [FlashAttention](https://github.com/bdashore3/flash-attention/releases/latest) on Windows:
```
pip install exllamav2-X.X.X+cuXXX.torch2.X.X-cp3XX-cp3XX-win_amd64.whl
pip install flash_attn-X.X.X+cuXXX.torch2.X.X-cp3XX-cp3XX-win_amd64.whl
```

## Usage
Only EXL2, 4-bit GPTQ and FP16 models are supported. You can find them on [Hugging Face](https://huggingface.co).
To use a model with the nodes, you should clone its repository with `git` or manually download all the files and place them in a folder in `models/llm`.
For example, if you'd like to download the 4-bit [Llama-3.1-8B-Instruct](https://huggingface.co/turboderp/Llama-3.1-8B-Instruct-exl2):
```
cd models
mkdir llm
git install lfs
git clone https://huggingface.co/turboderp/Llama-3.1-8B-Instruct-exl2 -b 4.0bpw
```

> [!TIP]
> You can add your own `llm` path to the [extra_model_paths.yaml](https://github.com/comfyanonymous/ComfyUI/blob/master/extra_model_paths.yaml.example) file and put the models there instead.

## Nodes
<table width="100%">
  <tr>
    <td colspan="3" align="center"><b>ExLlama Nodes</b></td>
  </tr>
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
    <td ><i>flash_attention</i></td>
    <td>Enabling reduces VRAM usage, not supported on cards with compute capability lower than <code>8.0</code>.</td>
  </tr>
  <tr>
    <td></td>
    <td><i>max_seq_len</i></td>
    <td>Max context, higher value equals higher VRAM usage. <code>0</code> will default to model config.</td>
  </tr>
  <tr>
    <td><b>Formatter</b></td>
    <td colspan="2">Formats messages using the model's chat template.</td>
  </tr>
  <tr>
    <td></td>
    <td><i>add_assistant_role</i></td>
    <td>Appends assistant role to the formatted output.</td>
  </tr>
  <tr>
    <td><b>Tokenizer</b></td>
    <td colspan="2">Tokenizes input text using the model's tokenizer.</td>
  </tr>
  <tr>
    <td></td>
    <td><i>add_bos_token</i></td>
    <td>Prepends the input with a <code>bos</code> token if enabled.</td>
  </tr>
  <tr>
    <td></td>
    <td><i>encode_special_tokens</i></td>
    <td>Encodes special tokens such as <code>bos</code> and <code>eos</code> if enabled, otherwise treats them as normal strings.</td>
  </tr>
  <tr>
    <td><b>Settings</b></td>
    <td colspan="2">Optional sampler settings node. Refer to <a href="https://docs.sillytavern.app/usage/common-settings/#sampler-parameters">SillyTavern</a> for parameters.</td>
  </tr>
  <tr>
    <td><b>Generator</b></td>
    <td colspan="2">Generates text based on the given input.</td>
  </tr>
  <tr>
    <td></td>
    <td><i>unload</i></td>
    <td>Unloads the model after each generation to reduce VRAM usage.</td>
  </tr>
  <tr>
    <td></td>
    <td><i>stop_conditions</i></td>
    <td>A list of strings to stop generation on, e.g. <code>"\n"</code> to stop on newline. Leave empty to only stop on <code>eos</code>.</td>
  </tr>
  <tr>
    <td></td>
    <td><i>max_tokens</i></td>
    <td>Max new tokens to generate. <code>0</code> will use available context.</td>
  </tr>
  <tr>
    <td colspan="3" align="center"><b>Text Nodes</b></td>
  </tr>
  <tr>
    <td><b>Clean</b></td>
    <td colspan="2">Strips punctuation, fixes whitespace, and changes case for input text.</td>
  </tr>
  <tr>
    <td><b>Message</b></td>
    <td colspan="2">A message for the <code>Formatter</code> node. Can be chained to create a conversation.</td>
  </tr>
  <tr>
    <td><b>Preview</b></td>
    <td colspan="2">Displays generated text in the UI.</td>
  </tr>
  <tr>
    <td><b>Replace</b></td>
    <td colspan="2">Replaces variable names in curly brackets, e.g. <code>{a}</code>, with their values.</td>
  </tr>
  <tr>
    <td><b>String</b></td>
    <td colspan="2">A string constant.</td>
  </tr>
</table>

## Workflow
An example workflow is embedded in the image below and can be opened in ComfyUI.

![Workflow](https://github.com/user-attachments/assets/359c0340-fe0e-4e69-a1b4-259c6ff5a142)

