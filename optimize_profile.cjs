const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

const inputPath = path.join(__dirname, 'images/paul-caruana-artist-malta.jpeg');
const outputWebP = path.join(__dirname, 'images/paul-caruana-artist-malta.webp');
const outputJpg = path.join(__dirname, 'images/paul-caruana-artist-malta.jpg'); // Normalize extension

// Create variants
async function processImage() {
  try {
    // webp
    await sharp(inputPath)
      .resize(800) // robust width for portraits
      .webp({ quality: 80 })
      .toFile(outputWebP);
      
    // normalized jpg
    await sharp(inputPath)
      .resize(800)
      .jpeg({ quality: 80, mozjpeg: true })
      .toFile(outputJpg);
      
    console.log('Success! Created optimized profile images.');
  } catch (err) {
    console.error('Error processing profile image:', err);
  }
}

processImage();
