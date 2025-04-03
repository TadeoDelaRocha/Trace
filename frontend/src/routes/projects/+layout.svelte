<script>
    import { onMount } from 'svelte';
    import { derived } from 'svelte/store';
    import { page } from '$app/stores';

    const currentPath = derived(page, ($page) => $page?.url?.pathname ?? '/');

    function navigate(route) {
      window.location.href = route;
    }
</script>
  
<div class="layout">
    <aside class="sidebar">
      <!-- Top: Home -->
      <div class="top">
        <button class="icon-button" on:click={() => navigate('/')}>
            <img src="/icons/favicon.png" alt="Home" class="icon-img" />
        </button>
      </div>
  
      <!-- Middle: Main nav -->
      <div class="middle">
        <button
          class="icon-button-mid"
          class:active={$currentPath === '/projects/myProjects'}
          on:click={() => navigate('/projects/myProjects')}
        >
          <img src="/icons/folder.svg" alt="Projects" class="icon-img" />
        </button>
        <button
          class="icon-button-mid"
          class:active={$currentPath === '/projects/folders'}
          on:click={() => navigate('/projects/folders')}
        >
          <img src="/icons/folder_open.svg" alt="Projects" class="icon-img" />
        </button>
        <button
          class="icon-button-mid"
          class:active={$currentPath === '/projects/deleted'}
          on:click={() => navigate('/projects/deleted')}
        >
          <img src="/icons/trash.svg" alt="Projects" class="icon-img" />
        </button>
      </div>
  
      <!-- Bottom: Settings -->
      <div class="bottom">
        <button
          class="icon-button"
          class:active={$currentPath === '/settings'}
          on:click={() => navigate('/settings')}
        >
          <img src="/icons/gear.svg" alt="Projects" class="icon-img" />
        </button>
      </div>
    </aside>
  
    <main class="content">
      <slot />
    </main>
  </div>
  
  <style>  
    .layout {
      display: flex;
      height: 100vh;
      overflow: hidden;
    }
  
    .sidebar {
      position: fixed;
      top: 0;
      left: 0;
      width: 80px;
      height: 100vh;
      background-color: hwb(0 77% 23%);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      align-items: center;
      padding: 1rem 0;
      box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
      z-index: 10;
    }
  
    .bottom {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        align-items: center;
        margin-bottom: 2rem;
    }

    .top,
    .middle{
      display: flex;
      flex-direction: column;
      gap: 1rem;
      align-items: center;
    }
  
    .icon-button {
      width: 48px;           
      height: 48px;
      background-color: transparent;
      border: none;
      border-radius: 9999px;  /* full round */
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: background 0.2s, color 0.2s;
    }

    .icon-button-mid {
      width: 48px;            
      height: 48px;
      background-color: #969ba1;
      border: none;
      border-radius: 9999px;  /* full round */
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: background 0.2s, color 0.2s;
    }

    .icon-button-mid:hover {
      background-color: #374151;
      color: white;
    }

    .icon-button-mid.active {
      background-color: #3d62a5;
      color: white;
    }

    .icon-button:hover {
      background-color: #868b94;
      color: white;
    }

    .icon-button.active {
      background-color: #3d62a5;
      color: white;
    }

    .icon-img {
      width: 28px;       /* smaller icon */
      height: 28px;
      object-fit: contain;
    }

  
    .content {
      margin-left: 80px; /* offset for fixed sidebar */
      flex: 1;
      padding: 2rem;
      overflow-y: auto;
      height: 100vh;
    }
  </style>