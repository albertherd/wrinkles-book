const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

const directory = './images';
const quality = 80;
const maxWidth = 1200;

// Files to skip (already optimized)
const skipFiles = [
    'og-social-card.jpg',
    'paul-caruana-artist-malta.jpg',
    'paul-caruana-artist-malta.webp'
];

fs.readdir(directory, (err, files) => {
    if (err) {
        console.error('Could not list the directory.', err);
        process.exit(1);
    }

    files.forEach(file => {
        if (!skipFiles.includes(file)) {
            const filePath = path.join(directory, file);
            const ext = path.extname(file).toLowerCase();
            const name = path.basename(file, ext);
            
            // Process only original JPGs that are not in skip list
            if (ext === '.jpg' || ext === '.jpeg') {
                console.log(`Processing ${file}...`);
                
                // 1. Optimize JPEG (Resize & Compress)
                sharp(filePath)
                    .resize({ width: maxWidth, withoutEnlargement: true })
                    .jpeg({ quality: quality, mozjpeg: true })
                    .toBuffer()
                    .then(buffer => {
                        fs.writeFile(filePath, buffer, (err) => {
                            if (err) console.error(`Error saving optimized JPG ${file}:`, err);
                            else console.log(`✅ Optimized ${file}`);
                        });
                    })
                    .catch(err => console.error(`Error processing ${file}:`, err));

                // 2. Generate/Overwrite WebP
                const webpPath = path.join(directory, `${name}.webp`);
                sharp(filePath)
                    .resize({ width: maxWidth, withoutEnlargement: true })
                    .webp({ quality: quality })
                    .toFile(webpPath)
                    .then(() => console.log(`✅ Generated ${name}.webp`))
                    .catch(err => console.error(`Error generating WebP for ${file}:`, err));
            }
        }
    }); 
});
