import lighthouse from "@lighthouse-web3/sdk";

/**
 * Sign a message with wallet for Lighthouse auth
 */
export const signMessage = async (signer: any, account: string) => {
  const { message } = (await lighthouse.getAuthMessage(account)).data;
  const signature = await signer.signMessage(message);
  return { signature, account };
};

/**
 * Upload a file encrypted
 */
export const uploadFileEncrypted = async (
  file: File,
  apiKey: string,
  signer: any,
  account: string,
  progressCallback?: (progress: number) => void
) => {
  const { signature, account: signerAddress } = await signMessage(signer, account);
  const output = await lighthouse.uploadEncrypted(file, apiKey, signerAddress, signature, progressCallback);
  return output.data[0].Hash; // Returns CID
};

/**
 * Upload a text string encrypted
 */
export const uploadTextEncrypted = async (
  text: string,
  apiKey: string,
  signer: any,
  account: string,
  name?: string
) => {
  const { signature, account: signerAddress } = await signMessage(signer, account);
  const output = await lighthouse.textUploadEncrypted(text, apiKey, signerAddress, signature, name);
  return output.data.Hash; // Returns CID
};
