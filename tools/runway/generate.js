#!/usr/bin/env node
// CLI for generating ICE READY image/video assets with the Runway API.
//
// Usage:
//   RUNWAYML_API_SECRET=... node generate.js image "prompt text" [outFile]
//   RUNWAYML_API_SECRET=... node generate.js video "prompt text" [inputImagePathOrUrl] [outFile]

import fs from 'node:fs';
import path from 'node:path';
import RunwayML from '@runwayml/sdk';

const OUTPUT_DIR = new URL('./output/', import.meta.url).pathname;
const POLL_INTERVAL_MS = 5000;

function usageAndExit() {
  console.error(
    'Usage:\n' +
      '  node generate.js image "<prompt>" [outFile.png]\n' +
      '  node generate.js video "<prompt>" <inputImagePathOrUrl> [outFile.mp4]'
  );
  process.exit(1);
}

function requireApiKey() {
  if (!process.env.RUNWAYML_API_SECRET) {
    console.error('Missing RUNWAYML_API_SECRET environment variable.');
    process.exit(1);
  }
}

function toDataUri(imagePath) {
  const buffer = fs.readFileSync(imagePath);
  const ext = path.extname(imagePath).slice(1).toLowerCase();
  const mime = ext === 'jpg' ? 'jpeg' : ext;
  return `data:image/${mime};base64,${buffer.toString('base64')}`;
}

async function waitForTask(client, taskId) {
  for (;;) {
    const task = await client.tasks.retrieve(taskId);
    if (task.status === 'SUCCEEDED') return task;
    if (task.status === 'FAILED' || task.status === 'CANCELLED') {
      throw new Error(`Task ${taskId} ${task.status}: ${task.failure ?? 'unknown error'}`);
    }
    console.log(`  ...task ${taskId} status: ${task.status}`);
    await new Promise((resolve) => setTimeout(resolve, POLL_INTERVAL_MS));
  }
}

async function downloadTo(url, outPath) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Failed to download output: ${res.status} ${res.statusText}`);
  const buffer = Buffer.from(await res.arrayBuffer());
  fs.mkdirSync(path.dirname(outPath), { recursive: true });
  fs.writeFileSync(outPath, buffer);
}

async function generateImage(promptText, outFile) {
  const client = new RunwayML();
  const task = await client.textToImage.create({
    model: 'gen4_image',
    promptText,
    ratio: '1920:1080',
  });
  console.log(`Started image task ${task.id}, waiting for completion...`);
  const result = await waitForTask(client, task.id);
  const outputUrl = result.output?.[0];
  if (!outputUrl) throw new Error('Task succeeded but no output URL was returned.');
  const outPath = path.resolve(OUTPUT_DIR, outFile ?? `image-${task.id}.png`);
  await downloadTo(outputUrl, outPath);
  console.log(`Saved image to ${outPath}`);
}

async function generateVideo(promptText, inputImage, outFile) {
  const client = new RunwayML();
  const promptImage = /^https?:\/\//.test(inputImage) ? inputImage : toDataUri(inputImage);
  const task = await client.imageToVideo.create({
    model: 'gen4_turbo',
    promptImage,
    promptText,
    ratio: '1280:720',
  });
  console.log(`Started video task ${task.id}, waiting for completion...`);
  const result = await waitForTask(client, task.id);
  const outputUrl = result.output?.[0];
  if (!outputUrl) throw new Error('Task succeeded but no output URL was returned.');
  const outPath = path.resolve(OUTPUT_DIR, outFile ?? `video-${task.id}.mp4`);
  await downloadTo(outputUrl, outPath);
  console.log(`Saved video to ${outPath}`);
}

async function main() {
  requireApiKey();
  const [command, ...rest] = process.argv.slice(2);

  if (command === 'image') {
    const [promptText, outFile] = rest;
    if (!promptText) usageAndExit();
    await generateImage(promptText, outFile);
  } else if (command === 'video') {
    const [promptText, inputImage, outFile] = rest;
    if (!promptText || !inputImage) usageAndExit();
    await generateVideo(promptText, inputImage, outFile);
  } else {
    usageAndExit();
  }
}

main().catch((err) => {
  console.error(err.message ?? err);
  process.exit(1);
});
