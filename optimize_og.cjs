const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

const inputPath = path.join(__dirname, 'images/wrinkles-book-cover.jpg');
const outputPath = path.join(__dirname, 'images/og-social-card.jpg');

// Resize to standard OG size (1200x630)
// Use 'contain' to fit the whole book cover without cropping
// Use a dark background to match the website theme
sharp(inputPath)
  .resize(1200, 630, {
    fit: 'contain',
    background: { r: 26, g: 26, b: 26, alpha: 1 } // #1a1a1a matching the dark theme
  })
  .jpeg({ quality: 80, mozjpeg: true }) // Optimize for size (<300KB target)
  .toFile(outputPath)
  .then(info => {
    console.log('Success! Created optimized OG image:', info);
  })
  .catch(err => {
    console.error('Error creating OG image:', err);
  });
