const https = require('https');

const fetchUrl = (url) => {
  return new Promise((resolve, reject) => {
    https.get(url, { headers: { 'User-Agent': 'Mozilla/5.0' } }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(data));
    }).on('error', reject);
  });
};

const extract = async () => {
  const urls = [
    'https://www.midseabooks.com/shop/art-photography/wrinkles/',
    'https://wrinklesbook.com/'
  ];
  
  for (const url of urls) {
    console.log(`\n--- ${url} ---`);
    const html = await fetchUrl(url);
    const regex = /<script[^>]*type=["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/gi;
    let match;
    let i = 1;
    while ((match = regex.exec(html)) !== null) {
      console.log(`Script ${i++}:`);
      try {
        const json = JSON.parse(match[1]);
        console.log(JSON.stringify(json, null, 2));
      } catch (e) {
        console.log("Error parsing JSON:", e.message);
        console.log(match[1]);
      }
    }
  }
};

extract();
