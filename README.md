# aurora-refs

Reference images for the Aurora project. Hugging Face Spaces read them over MCP through their raw URLs.

## Files

All images are 768×1344 PNG.

| File | What it is | Raw URL |
|---|---|---|
| `aurora_portrait_gta_v1.png` | Aurora, face/identity reference | https://raw.githubusercontent.com/leadbit-flash1/aurora-refs/main/aurora_portrait_gta_v1.png |
| `estebald_human_v1.png` | Estebald, human form | https://raw.githubusercontent.com/leadbit-flash1/aurora-refs/main/estebald_human_v1.png |
| `estebald_horse_v2.png` | Estebald, horse form | https://raw.githubusercontent.com/leadbit-flash1/aurora-refs/main/estebald_horse_v2.png |
| `petrovich_portrait_v3.png` | Petrovich, portrait | https://raw.githubusercontent.com/leadbit-flash1/aurora-refs/main/petrovich_portrait_v3.png |
| `poses/pose_aurora_pilates.png` | Aurora layout sheet: outfit colours only (see note below) | https://raw.githubusercontent.com/leadbit-flash1/aurora-refs/main/poses/pose_aurora_pilates.png |
| `poses/collage_aurora_pilates.png` | Aurora face pasted on the layout sheet | https://raw.githubusercontent.com/leadbit-flash1/aurora-refs/main/poses/collage_aurora_pilates.png |

Always link to `raw.githubusercontent.com/...`. A `github.com/.../blob/...` link points to a web page, not to the image.

## Space to use

**[`Guaryn/qwen-image-2.1-uncensored-aio-loras`](https://huggingface.co/spaces/Guaryn/qwen-image-2.1-uncensored-aio-loras)**, the uncensored Qwen-Image 2.1 model (Q4_K_M GGUF) on ZeroGPU.

This is the only Qwen-Image 2.1 Space we found that takes reference images as **separate fields** (`ref_image_1`, `ref_image_2`). That matters because of the gallery bug described below.

Tool: `qwen_image_2_1_uncensored_aio_loras_generate`

### One reference: pose and scene from the prompt (best for poses)

```json
{
  "mode": "Edit Image (1 Ref)",
  "lora_adapter": "Viggle Turbo (6-Step)",
  "steps": 6,
  "aspect_ratio": "Portrait · 9:16 (768x1344)",
  "custom_repo": "",
  "custom_file": "",
  "ref_image_1": "https://raw.githubusercontent.com/leadbit-flash1/aurora-refs/main/aurora_portrait_gta_v1.png",
  "prompt": "..."
}
```

### Two references: identity plus a second image

Use the same settings with `"mode": "Transform & Swap (2 Refs)"` and add `ref_image_2`. In the prompt, call them "image 1" and "image 2".

Notes:

- `custom_repo` and `custom_file` are required fields. Send them as empty strings.
- Viggle Turbo always runs 6 steps. One generation takes about 5–7 s of GPU time.
- The Space can't take more than 2 references. To pass more, merge them into one collage image and use it as one of the two refs.

## Prompt that worked: Aurora, pilates, GTA V style

Result: seed `584075567`, 1 ref mode, Viggle Turbo, 9:16.

> Grand Theft Auto V loading screen illustration, Rockstar-style comic art: thick bold black contour lines, flat cel-shaded colors with hard graphic shadows, high contrast, stylized vector-like painting, no photorealism. Subject: the woman from image 1 (same face, long brown hair, silver hoop earrings, crescent moon necklace) doing a pilates teaser pose on a black yoga mat, body in a V shape balanced on her hips, both legs straight and raised, arms stretched forward parallel to her legs, hands free and not holding the legs. Full body in frame. White sports crop top, light grey sport leggings with small orange chevrons at the knees, white running sneakers. Background: stylized sunny Los Santos beach gym with palm trees and orange sky, same comic poster style.

Lessons:

- **Put the style words first and make them strong.** "GTA V style" alone at the end of the prompt comes out semi-photographic. Thick outlines, cel shading and "no photorealism" at the start give the loading-screen look.
- **Don't use `poses/pose_aurora_pilates.png` as a pose reference.** It's a standing stick figure, so the model copies a standing pose and even the heels. Describe the exercise in the prompt and use 1 ref mode instead.
- **Name the footwear** (sneakers, or grip socks for the mat). If you don't, the model carries over shoes from the references.

## Known issues

### Gallery inputs fail over MCP (all Spaces)

Any Space whose MCP tool takes several images as one gallery list fails before the image is generated, with this error:

```
PointerToNowhere: '/$defs/GalleryImage' does not exist
```

The cause is a bug in Gradio's MCP tool description for `gr.Gallery` inputs. Our images and links have nothing to do with it. Spaces affected:

- `Jamesmiltonp/qwen-image-2-1-lightning`
- `hugging-apps/qwen-image-2-1-lightning`
- `hugging-apps/turbo8-qwen-image-2-1`
- `linoyts/qwen-image-2-1-realtime`

Use Spaces with separate image fields instead.

### ZeroGPU quota

The Guaryn Space reserves **60 s** of ZeroGPU quota per call, even though one generation takes about 6 s. Once less than 60 s of daily quota is left, calls are rejected with "quota exceeded". Quota refills over a rolling 24 hours. Prepare collages and prompts before you call it.

### Other Spaces tested

`amisima/Qwen-2.1-Turbo-...-Face-Swap-MOSS-...` has two image fields, but its numeric dropdowns (`camera_azimuth`, `resolution_multiple`) fail validation over MCP whatever type is sent.
