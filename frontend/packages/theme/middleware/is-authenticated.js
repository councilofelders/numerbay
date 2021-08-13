
export default async ({ app, redirect }) => {
  if (!app.$cookies.get('nb-token')) {
    return redirect('/');
  }
};
