<script>
    function navigateTo(route) {
      window.location.href = route;
    }
  </script>
  
  <div class="landing-page">
  
    <!-- Navigation Bar (Top Right) -->
    <nav class="nav">
      <button class="nav-button" on:click={() => navigateTo('/projects/myProjects')}>Projects Dashboard</button>
      <button class="nav-button" on:click={() => navigateTo('/settings')}>Settings</button>
    </nav>
  
    <!-- Main Content -->
    <main class="content">
      <h1 class="title">Elevate Your Security Strategy with TRACE</h1>
      <p class="description">
        A Cybersecurity Platform to Protect Your Digital Assets.  
        Detect Vulnerabilities, Strengthen Defense, and Secure Your Network Seamlessly.  
        Gain Real-Time Insights and Proactive Protection.
      </p>
      <button class="start-button" on:click={() => navigateTo('/tools/toolsDashboard')}>Get Started</button>
    </main>
  </div>
  
  <style>
    /* Layout styling for the whole page */
    .landing-page {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      background-color: var(--background-color);
      color: var(--text-color);
      padding: 20px;
      position: relative;
      overflow: hidden;
    }

    /* TRACE Logo Styling (Top Left) */
    .logo {
      position: absolute;
      top: 20px;
      left: 20px;
      width: var(--logo-size);
      max-width: 80px; /* Prevent the logo from becoming too large */
      height: auto;
    }
  
    /* Navigation Bar (Top Right) */
    .nav {
      position: absolute;
      top: 20px;
      right: 20px;
      display: flex;
      gap: 12px;
    }
  
    .nav-button {
      padding: 10px 20px;
      font-size: 1rem;
      border: none;
      background-color: transparent;
      color: var(--text-color);
      cursor: pointer;
    }
  
    .nav-button:hover {
      background-color: var(--primary-color);
      color: var(--background-color);
    }
  
    /* Main Content (Centered) */
    .content {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      max-width: 800px;
      padding: 20px;
      text-align: center;
      z-index: 1;
    }
  
    .title {
      font-size: 2.5rem;
      font-weight: bold;
      color: var(--text-color);
    }
  
    .description {
      max-width: 600px;
      font-size: 1.2rem;
      color: var(--text-color);
      margin-top: 10px;
    }
  
    /* Start Button Styling */
    .start-button {
      margin-top: 20px;
      padding: 12px 24px;
      font-size: 1rem;
      background-color: var(--primary-color);
      color: var(--text-color);
      border: none;
      cursor: pointer;
      border-radius: 5px;
    }
  
    .start-button:hover {
      background-color: var(--button-hover-color);
    }
  </style>