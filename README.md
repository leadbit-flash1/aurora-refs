# aurora-refs

Reference images for the Aurora project. Hugging Face Spaces read them over MCP through their raw URLs.

## Files

All images are 768×1344 PNG.

| File | What it is | Raw URL |
|---|---|---|
| `aurora_face_ref_straight.png` | **Aurora, face/identity reference — use this one.** The portrait rotated 32° so the head is upright; prevents the tilt from carrying into new images |
| `aurora_portrait_gta_v1.png` | Aurora, original approved portrait (head tilted — don't use as ref for new poses) | https://raw.githubusercontent.com/leadbit-flash1/aurora-refs/main/aurora_portrait_gta_v1.png |
| `estebald_human_v1.png` | Estebald, human form | https://raw.githubusercontent.com/leadbit-flash1/aurora-refs/main/estebald_human_v1.png |
| `estebald_horse_v2.png` | Estebald, horse form | https://raw.githubusercontent.com/leadbit-flash1/aurora-refs/main/estebald_horse_v2.png |
| `petrovich_portrait_v3.png` | Petrovich, portrait | https://raw.githubusercontent.com/leadbit-flash1/aurora-refs/main/petrovich_portrait_v3.png |
| `poses/pose_aurora_pilates.png` | Aurora layout sheet: outfit colours only (see note below) | https://raw.githubusercontent.com/leadbit-flash1/aurora-refs/main/poses/pose_aurora_pilates.png |
| `poses/collage_aurora_pilates.png` | Aurora face pasted on the layout sheet | https://raw.githubusercontent.com/leadbit-flash1/aurora-refs/main/poses/collage_aurora_pilates.png |

Work in progress lives in `wip/`. Each WIP folder has a `STATUS.json` saying what's done, what's broken and what to run next. **Read it before generating anything.**

Always link to `raw.githubusercontent.com/...`. A `github.com/.../blob/...` link points to a web page, not to the image.

## ⚠️ To regenerate

| File | Problem | What to change |
|---|---|---|
| `outputs/aurora_stage_584075567.png` | Outfit too dark: navy sequins and dark tights merge with the violet stage light | Brighter costume (e.g. silver/white or light lilac sequined top, light tights), keep modest PEGI-12 cut; background colour must contrast with the costume |

## Character rules

- **Cops' wives are NEVER shown from the front — always from behind** (back view, faces not visible), so they don't take attention from the main characters.
- **Cops are always silhouettes in shadow** — faces never visible.
- **Sprites: generate on a flat warm sunset-orange background** (e.g. `#F78929`), not greenscreen: a green key tints rim light and reflections green. Say "plain flat warm sunset orange background, completely empty, no objects" and cut it out with `python3 tools/key_out.py in.png out.png` (colour key, soft edges, keeps small bg-coloured clothing details, clears big gaps like between the legs); no ML background removal needed. Pick a background colour that contrasts with the costume; if parts of the costume match it (dark tights on violet), add `--ml`.

## Outputs

| File | What it is |
|---|---|
| `outputs/aurora_pilates_side_584075567.png` | Aurora pilates teaser, side view, transparent PNG sprite (approved pose) |
| `outputs/aurora_pilates_side_584075567_src.png` | Same, original on flat orange background |
| `outputs/aurora_stage_584075567.png` | ⚠️ **TEMPORARY — REGENERATE: outfit too dark.** Aurora stage costume (PEGI-12: long sleeves, high neck, tights, chiffon skirt), pole, glowing UV henna wings; generated on flat deep violet, cut with `--ml` (`_src.png` = on violet) |
| `outputs/aurora_casual_v3_584075567.png` | **Approved.** Aurora casual/riding sprite: linen shirt, jeans, knee-high riding boots, apple; dancer proportions (~8 heads, long legs); transparent PNG (`_src.png` = on orange) |

Params: Guaryn Space, `Edit Image (1 Ref)`, base model (no LoRA), 28 steps, seed `584075567`, 9:16; prompt = the pilates prompt below + "head held straight and upright, not tilted", "Side view, camera at mat level", flat orange background.

## Prompt add-ons that fixed problems

- Body proportions (from the model's body photo, measured, sent as text only — the photo itself is never uploaded): "Body proportions of a tall slim athletic dancer: about 8 heads tall, small head relative to the body, very long slender legs making up half of her total height, narrow waist, slim toned arms, narrow shoulders, slim hips."
- Legs merging in profile: "feet apart at shoulder width, BOTH legs clearly visible and separate, two legs and two feet, anatomically correct".

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
- Viggle Turbo always runs 6 steps and ignores the `steps` field. One generation takes about 5–7 s of GPU time. Hands come out blurry, so use it for drafts only (see "Steps and quality" below).
- The Space can't take more than 2 references. To pass more, merge them into one collage image and use it as one of the two refs.

## Prompt that worked: Aurora, pilates, GTA V style

Result: seed `584075567`, 1 ref mode, Viggle Turbo, 9:16.

> Grand Theft Auto V loading screen illustration, Rockstar-style comic art: thick bold black contour lines, flat cel-shaded colors with hard graphic shadows, high contrast, stylized vector-like painting, no photorealism. Subject: the woman from image 1 (same face, long brown hair, silver hoop earrings, crescent moon necklace) doing a pilates teaser pose on a black yoga mat, body in a V shape balanced on her hips, both legs straight and raised, arms stretched forward parallel to her legs, hands free and not holding the legs. Full body in frame. White sports crop top, light grey sport leggings with small orange chevrons at the knees, white running sneakers. Background: stylized sunny Los Santos beach gym with palm trees and orange sky, same comic poster style.

Lessons:

- **Put the style words first and make them strong.** "GTA V style" alone at the end of the prompt comes out semi-photographic. Thick outlines, cel shading and "no photorealism" at the start give the loading-screen look.
- **Don't use `poses/pose_aurora_pilates.png` as a pose reference.** It's a standing stick figure, so the model copies a standing pose and even the heels. Describe the exercise in the prompt and use 1 ref mode instead.
- **Name the footwear** (sneakers, or grip socks for the mat). If you don't, the model carries over shoes from the references.

## Steps and quality

Same prompt, same seed `584075567`, 1-ref mode:

| Setting | Steps | GPU time | Result |
|---|---|---|---|
| Viggle Turbo | 6 (fixed) | 5.4 s | Style OK, hands blurry and fused |
| Base, no LoRA | 16 | 10.2 s | Sharp fingers, but an **extra third hand** |
| Base, no LoRA | 28 | ~17 s expected | **Not tested yet**, runs limit hit |
| Quality Fix LoRA | 28 | ~17 s expected | **Not tested yet**, runs limit hit |

The Space charges 60 s of quota per call whatever the step count. Up to about 40 steps still finishes well inside 60 s, so more steps cost no extra quota. 16 steps is too few for the base model. The next candidates are 28 steps with the base model and 28 steps with Quality Fix.

## Work in progress

### `wip/aurora_pilates_gta/`: WIP, damaged

| | |
|---|---|
| Status | **WIP / DAMAGED, not final** |
| Pose, style, outfit, face | OK |
| Hands | Broken: extra third hand by her head, and her right hand rests on the knee |
| Clean image | [`aurora_pilates_gta_base16_DAMAGED.png`](wip/aurora_pilates_gta/aurora_pilates_gta_base16_DAMAGED.png) |
| Defects marked | [`aurora_pilates_gta_base16_DAMAGED_annotated.png`](wip/aurora_pilates_gta/aurora_pilates_gta_base16_DAMAGED_annotated.png). Red = damaged, yellow = weak, green = OK |
| Exact params, prompt, defect boxes, next steps | [`STATUS.json`](wip/aurora_pilates_gta/STATUS.json) |

**Next agent:** once the ZeroGPU limit resets, rerun the params in `STATUS.json` at 28 steps, first with the base model, then with Quality Fix. Keep the version whose hands are correct. Then update `STATUS.json`, and move the image to `outputs/` only when the hands are clean.

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

There's also a daily **runs** limit. On 2026-11-24 the free account was blocked after about 5 generations with `ZeroGPU quota exceeded: You have exceeded your ZeroGPU runs limit`. Plan each test run before you spend it.

### Other Spaces tested

`amisima/Qwen-2.1-Turbo-...-Face-Swap-MOSS-...` has two image fields, but its numeric dropdowns (`camera_azimuth`, `resolution_multiple`) fail validation over MCP whatever type is sent.
