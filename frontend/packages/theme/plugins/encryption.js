import Vue from 'vue';

import { ethers } from 'ethers';
import nacl from "tweetnacl";
import {decodeBase64, decodeUTF8, encodeBase64, encodeUTF8} from "tweetnacl-util";


// eslint-disable-next-line no-unused-vars,@typescript-eslint/no-unused-vars
export default async ({env}, inject) => {

  const encryption = Vue.observable({
    // Generic
    async createKeys(signer) {
      const encryptionKeyPair = nacl.box.keyPair();
      const symmetricalKey = await this.getSymmetricalKeyFromSignature(signer);
      return {
          publicKey: encodeBase64(encryptionKeyPair.publicKey),
          privateKey: encodeBase64(encryptionKeyPair.secretKey),
          storageEncryptionKey: symmetricalKey.symmetricalKey,
          storageEncryptionKeySalt: symmetricalKey.symmetricalKeySalt,
      };
    },

    // Asymmetrical Encryption
    decrypt({encryptedData, publicKey, privateKey}) {
      return nacl.sealedbox.open(new Uint8Array(encryptedData), decodeBase64(publicKey), decodeBase64(privateKey))
    },

    // Symmetrical Encryption
    async getSymmetricalKeyFromSignature(signer, salt) {
      const symmetricalKeySalt = salt ?? `Sign this to retrieve your encryption key.\n\nSalt:${encodeBase64(
          nacl.randomBytes(nacl.secretbox.keyLength),
      )}`;
      const signature = await signer.signMessage(symmetricalKeySalt);

      return {
        symmetricalKey: this.generateSymmetricalKey(ethers.utils.arrayify(ethers.utils.keccak256(signature))),
        symmetricalKeySalt
      }
    },

    generateSymmetricalKey(seed) {
        return seed
            ? encodeBase64(seed)
            : encodeBase64(nacl.randomBytes(nacl.secretbox.keyLength));
    },

    newNonce() {
        return nacl.randomBytes(nacl.secretbox.nonceLength);
    },

    symmetricalEncrypt(json, key) {
        const keyUint8Array = decodeBase64(key);

        const nonce = this.newNonce();
        const messageUint8 = decodeUTF8(JSON.stringify(json));
        const box = nacl.secretbox(messageUint8, nonce, keyUint8Array);

        const fullMessage = new Uint8Array(nonce.length + box.length);
        fullMessage.set(nonce);
        fullMessage.set(box, nonce.length);

        const base64FullMessage = encodeBase64(fullMessage);
        return base64FullMessage;
    },

    symmetricalDecrypt(messageWithNonce, key) {
        const keyUint8Array = decodeBase64(key);
        const messageWithNonceAsUint8Array = decodeBase64(messageWithNonce);
        const nonce = messageWithNonceAsUint8Array.slice(0, nacl.secretbox.nonceLength);
        const message = messageWithNonceAsUint8Array.slice(
            nacl.secretbox.nonceLength,
            messageWithNonce.length,
        );

        const decrypted = nacl.secretbox.open(message, nonce, keyUint8Array);

        if (!decrypted) {
            throw new Error('Could not decrypt message');
        }

        const base64DecryptedMessage = encodeUTF8(decrypted);
        return JSON.parse(base64DecryptedMessage);
    },

  });

  inject('encryption', encryption);
};
