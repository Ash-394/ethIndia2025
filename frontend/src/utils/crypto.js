export async function calculateSha256(file) {
    const buffer = await file.arrayBuffer();
    const hashBuffer = await crypto.subtle.digest('SHA-256', buffer);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const sha256Hash = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    return sha256Hash;
  }
  
  export async function calculateSha256OfText(text) {
    const textEncoder = new TextEncoder();
    const data = textEncoder.encode(text);
    const hashBuffer = await crypto.subtle.digest('SHA-256', data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const sha256Hash = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    return sha256Hash;
  }