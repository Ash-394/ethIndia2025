import { Web3Storage } from "web3.storage";

const API_TOKEN = import.meta.env.VITE_WEB3_STORAGE_API_KEY; // Use environment variable for API key

export const client = new Web3Storage({ token: API_TOKEN });

export async function uploadFile(file) {
  try {
    const cid = await client.put([file]);
    console.log("File uploaded with CID:", cid);
    return cid;
  } catch (err) {
    console.error("Upload failed:", err);
    throw err;
  }
}

// Function to upload text as a Blob
export async function uploadText(text, filename = "text_evidence.txt") {
  try {
    const blob = new Blob([text], { type: 'text/plain' });
    const file = new File([blob], filename);
    const cid = await client.put([file]);
    console.log("Text uploaded with CID:", cid);
    return cid;
  } catch (err) {
    console.error("Text upload failed:", err);
    throw err;
  }
}