function authHeaders(token: string) {
  return {
    headers: {
      Authorization: `Bearer ${token}`
    }
  };
}

export {
  authHeaders
};
