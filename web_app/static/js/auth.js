async function fetchCurrentUser() {
  try {
    const resp = await fetch('/api/auth/me');
    if (!resp.ok) return null;
    const data = await resp.json();
    return data.user;
  } catch {
    return null;
  }
}

async function logout() {
  await fetch('/api/auth/logout', { method: 'POST' });
  window.location.href = '/login';
}

document.addEventListener('DOMContentLoaded', async () => {
  const userInfo = document.getElementById('user-info');
  const logoutBtn = document.getElementById('logout-btn');
  if (userInfo) {
    const user = await fetchCurrentUser();
    if (user) {
      userInfo.textContent = `欢迎，${user.username}`;
    }
  }
  if (logoutBtn) {
    logoutBtn.addEventListener('click', logout);
  }
});
