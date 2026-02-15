const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

const imagesDir = path.join(__dirname, 'public/images');

fs.readdir(imagesDir, (err, files) => {
    if (err) {
        console.error('Could not list the directory.', err);
        process.exit(1);
    }

    files.forEach((file, index) => {
        if (path.extname(file).toLowerCase() === '.jpg' || path.extname(file).toLowerCase() === '.jpeg') {
            const inputFile = path.join(imagesDir, file);
            const outputFile = path.join(imagesDir, path.parse(file).name + '.webp');

            sharp(inputFile)
                .webp({ quality: 80 })
                .toFile(outputFile)
                .then(info => {
                    console.log(`Converted ${file} to ${path.parse(file).name}.webp`);
                })
                .catch(err => {
                    console.error(`Error converting ${file}:`, err);
                });
        }
    });
});