/** @type {import('./$types').PageLoad} */
export function load() {
    // For example, check if a user is already logged in:
    const user = typeof window !== 'undefined' ? localStorage.getItem('user') : null;
    if (user) {
      // Optionally redirect to a different page if logged in:
      // return { status: 302, redirect: '/' };
    }
    return {};
  }
  