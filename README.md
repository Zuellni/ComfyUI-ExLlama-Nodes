# ComfyUI ExLlamaV2 Nodes
A simple local text generator for [ComfyUI](https://github.com/comfyanonymous/ComfyUI) using [ExLlamaV2](https://github.com/turboderp/exllamav2).

## Installation
Clone the repository to `custom_nodes`:
```
git clone https://github.com/Zuellni/ComfyUI-ExLlama-Nodes custom_nodes/ComfyUI-ExLlamaV2-Nodes
```

Install the requirements:
```
pip install -r custom_nodes/ComfyUI-ExLlamaV2-Nodes/requirements.txt
```

On Windows, install one of the precompiled [wheels](https://github.com/turboderp/exllamav2/releases) instead:
```
pip install https://github.com/turboderp/exllamav2/releases/download/v0.0.xx/exllamav2-0.0.xx+cuXXX-cpXXX-cpXXX-win_amd64.whl
```

Check which one you need with:
```
python -c "import sys, torch; print(f'cu{torch.version.cuda.replace('.', '')}-cp{sys.version_info[0]}{sys.version_info[1]}')"
```

> [!CAUTION]
> If you see errors related to ExLlamaV2 while loading the nodes, try to install it following the [official instructions](https://github.com/turboderp/exllamav2#installation).

## Usage
Only EXL2, 4-bit GPTQ, and unquantized HF models are supported. You can find them on [Hugging Face](https://huggingface.co). See the model card in each repository for details on instruction formats.

To use a model with the nodes, you should clone its repository with git or manually download all the files and place them in `models/llm`.
For example, if you'd like to download the 6-bit [Llama-3-8B-Instruct](https://huggingface.co/turboderp/Llama-3-8B-Instruct-exl2), use the following command:
```
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
    <td>Lower value equals lower VRAM usage but also impacts generation speed.</td>
  </tr>
  <tr>
    <td></td>
    <td><i>max_seq_len</i></td>
    <td>Max context, higher value equals higher VRAM usage. <code>0</code> will default to config.</td>
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
    <td><b>Previewer</b></td>
    <td colspan="2">Displays generated text in the UI.</td>
  </tr>
  <tr>
    <td><b>Replacer</b></td>
    <td colspan="2">Replaces variable names enclosed in brackets, eg <code>[a]</code>, with their values.</td>
  </tr>
</table>

## Workflow
The example workflow is embedded in the image below and can be opened in ComfyUI.

![workflow](https://github.com/Zuellni/ComfyUI-ExLlama-Nodes/assets/123005779/d496acee-d556-40d4-aef4-5ca34247f2e4)

