# Runway asset generator

CLI for generating ICE READY image/video assets via the [Runway API](https://docs.dev.runwayml.com/).

## Setup

```sh
cd tools/runway
npm install
export RUNWAYML_API_SECRET=your_api_key_here
```

## Usage

Generate an image from a text prompt:

```sh
node generate.js image "A frosty ice cube mascot for the ICE READY app, blue and white, flat vector style" hero.png
```

Generate a video from a text prompt + a starting image (local file or URL):

```sh
node generate.js video "The ice cube mascot waves and melts into a puddle" ../../ice_ready_fixed.png promo.mp4
```

Output files are written to `tools/runway/output/` by default (or wherever you point `outFile`).
