// export async function generateSignedUrl (signingURL, file, includeFile, config) {
//   const fd = new FormData();
//   fd.append('filename', file.upload.filename);
//   fd.append('filesize', file.size);
//   fd.append('type', file.type);
//   if (includeFile) {
//     fd.append('file', file);
//   }
//   const result = await makeRequest('POST', `${signingURL}`, fd, config);
//   return result;
// }

// eslint-disable-next-line no-unused-vars,@typescript-eslint/no-unused-vars
export async function generateSignedUrl (signingURL, params, file, includeFile, config) {
  const response = await signingURL({
    filename: file.upload.filename,
    filesize: file.size,
    type: file.type,
    ...params
  });
  // console.log('upload url', response.url)
  return response;
}

// function makeRequest(method, url, params, config) {
//   return new Promise((resolve, reject) => {
//     const xhr = new XMLHttpRequest();
//     xhr.responseType = 'json';
//     xhr.open(method, url);
//
//     Object.entries(config.headers || {}).forEach(([name, value]) => {
//       xhr.setRequestHeader(name, value);
//     });
//
//     // eslint-disable-next-line func-names
//     xhr.onload = function () {
//       if (this.status >= 200 && this.status < 300) {
//         resolve(xhr.response);
//       } else {
//         reject({
//           status: this.status,
//           statusText: xhr.statusText
//         });
//       }
//     };
//     // eslint-disable-next-line func-names
//     xhr.onerror = function () {
//       reject({
//         status: this.status,
//         statusText: xhr.statusText
//       });
//     };
//     xhr.send(params);
//   });
// }
