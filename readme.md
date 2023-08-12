# CG's custom nodes

A set of custom nodes for ComfyUI. These nodes have been built to support a series of workflows described below, but are designed to be as flexible as possible. They are also a work in progress...

## Installation

```
cd [ComfyUI root]/custom_nodes
git clone https://github.com/chrisgoringe/cg_custom_nodes.git
```
then restart your ComfyUI server. All these nodes will appear under `Add Node > CG`.

## Update

```
cd [ComfyUI root]/custom_nodes
git pull
```
then restart your ComfyUI server.

## Workflows

- [Merge Latents](docs/merge_latents.md) - combine two images in latent space
- Masks tools
- Iterating with stash
- Logging and other string tools
- Comparing images
- Unprompt
- Randoms
- Standard Sized
- Development tools (can also be used like reroute, but typed and nestable)

(docs to do)

## Other documentation

- [All the nodes](docs/all_nodes.md)
- [Changelog](docs/change_log.md)
- [Future possibilities](docs/)