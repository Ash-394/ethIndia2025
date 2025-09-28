export const fetchFileFromCID = async (cid: string) => {
    try {
      const url = `https://gateway.lighthouse.storage/ipfs/${cid}`;
      const response = await fetch(url);
      if (!response.ok) throw new Error("Failed to fetch file");
      
      // You can return as text, JSON, or blob depending on your use-case
      const contentType = response.headers.get("Content-Type") || "";
      if (contentType.includes("application/json")) {
        return await response.json();
      } else if (contentType.includes("text")) {
        return await response.text();
      } else {
        return await response.blob();
      }
    } catch (err) {
      console.error("Fetch error:", err);
      throw err;
    }
  };

  