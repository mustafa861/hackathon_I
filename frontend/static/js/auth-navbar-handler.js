// Handle authentication status in navbar
function initializeAuthStatus() {
  // Check if auth container exists
  const authContainer = document.getElementById('auth-status-container');
  if (!authContainer) return false; // Return false to indicate container not ready

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
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
      logoutBtn.addEventListener('click', function() {
        // Clear auth data
        localStorage.removeItem('auth_token');
        localStorage.removeItem('user_email');

        // Refresh the page to update UI
        window.location.reload();
      });
    }
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

  return true; // Return true to indicate successful initialization
}

// Initialize immediately and repeatedly until container is found
function waitForContainerAndInitialize() {
  if (initializeAuthStatus()) {
    // Successfully initialized, stop trying
    return true;
  } else {
    // Container not found yet, try again in a bit
    setTimeout(waitForContainerAndInitialize, 50);
    return false;
  }
}

// Start the initialization process
waitForContainerAndInitialize();

// Listen for auth state changes from React app
window.addEventListener('storage', function(e) {
  if (e.key === 'auth_token' || e.key === 'user_email') {
    // Auth state changed, refresh the navbar after a short delay to ensure DOM is ready
    setTimeout(function() {
      const authContainer = document.getElementById('auth-status-container');
      if (authContainer) {
        initializeAuthStatus();
      }
    }, 100);
  }
});

// Also listen for potential dynamic navbar updates (in case navbar gets re-rendered by Docusaurus)
if ('MutationObserver' in window) {
  const observer = new MutationObserver(function(mutations) {
    mutations.forEach(function(mutation) {
      mutation.addedNodes.forEach(function(node) {
        if (node.nodeType === 1 && node.id === 'auth-status-container') {
          // New auth container added, initialize it
          setTimeout(initializeAuthStatus, 50);
        }
      });
    });
  });

  observer.observe(document.body, {
    childList: true,
    subtree: true
  });
}