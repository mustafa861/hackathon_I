// Handle authentication status in navbar
document.addEventListener('DOMContentLoaded', function() {
  // Check if auth container exists
  const authContainer = document.getElementById('auth-status-container');
  if (!authContainer) return;

  // Get auth status from localStorage (where our React context stores it)
  const token = localStorage.getItem('auth_token');
  const email = localStorage.getItem('user_email');

  if (token && email) {
    // User is authenticated
    authContainer.innerHTML = `
      <div style="display: flex; align-items: center; gap: 1rem;">
        <span style="color: white; font-size: 0.875rem;">${email}</span>
        <button id="logout-btn" style="
          background: none;
          border: none;
          color: white;
          cursor: pointer;
          text-decoration: underline;
          font-size: 0.875rem;
          padding: 0;
          margin: 0;
        ">Logout</button>
      </div>
    `;

    // Add logout functionality
    document.getElementById('logout-btn').addEventListener('click', function() {
      // Clear auth data
      localStorage.removeItem('auth_token');
      localStorage.removeItem('user_email');

      // Refresh the page to update UI
      window.location.reload();
    });
  } else {
    // User is not authenticated
    authContainer.innerHTML = `
      <div style="display: flex; align-items: center; gap: 1rem;">
        <a href="/signup" style="
          color: white;
          text-decoration: none;
          font-size: 0.875rem;
          padding: 6px 12px;
          border: 1px solid white;
          border-radius: 4px;
          display: inline-block;
        ">SIGNUP</a>
        <a href="/login" style="
          color: white;
          text-decoration: none;
          font-size: 0.875rem;
          padding: 6px 12px;
          border: 1px solid white;
          border-radius: 4px;
          display: inline-block;
        ">SIGNIN</a>
      </div>
    `;
  }
});

// Listen for auth state changes from React app
window.addEventListener('storage', function(e) {
  if (e.key === 'auth_token' || e.key === 'user_email') {
    // Auth state changed, refresh the navbar
    const authContainer = document.getElementById('auth-status-container');
    if (authContainer) {
      window.location.reload(); // Simple approach to refresh auth status
    }
  }
});