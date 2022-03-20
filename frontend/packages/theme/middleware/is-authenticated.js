
export default async ({ app, redirect }) => {
  const token = app.$cookies.get('nb-token');
  if (!token || token === 'undefined') {
    return redirect('/login-v2');
  }
};
