<script>
    import { onMount } from 'svelte';
    import { derived } from 'svelte/store';
    import { page } from '$app/stores';

    const currentPath = derived(page, ($page) => $page.url.pathname);

    function navigateTo(route) {
      window.location.href = route;
    }
</script>
  
<div class="layout">
    <aside class="sidebar">
      <!-- Top: Home -->
      <div class="top">
        <button class="icon-button" on:click={() => navigate('/')}>
            <img src="/favicon.png" alt="Home" class="icon-img" />
        </button>
      </div>
  
      <!-- Middle: Main nav -->
      <div class="middle">
        <button
          class="icon-button"
          class:active={$currentPath === '/projects/myprojects'}
          on:click={() => navigate('/projects/myprojects')}
        >
          📁
        </button>
        <button
          class="icon-button"
          class:active={$currentPath === '/dashboard'}
          on:click={() => navigate('/dashboard')}
        >
          📊
        </button>
        <button
          class="icon-button"
          class:active={$currentPath === '/analytics'}
          on:click={() => navigate('/analytics')}
        >
          📈
        </button>
      </div>
  
      <!-- Bottom: Settings -->
      <div class="bottom">
        <button
          class="icon-button"
          class:active={$currentPath === '/settings'}
          on:click={() => navigate('/settings')}
        >
          ⚙️
        </button>
      </div>
    </aside>
  
    <main class="content">
      <slot />
    </main>
  </div>
  
  <style>
    .icon-img {
        width: 42px;
        height: 42px;
        object-fit: contain;
        border-radius: 6px; /* optional for a softer look */
        }
            
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
      background: none;
      border: none;
      font-size: 1.5rem;
      color: #9ca3af;
      cursor: pointer;
      padding: 0.5rem;
      border-radius: 0.5rem;
      transition: background 0.2s, color 0.2s;
    }
  
    .icon-button:hover {
      background-color: #374151;
      color: white;
    }
  
    .icon-button.active {
      background-color: #2563eb;
      color: white;
    }
  
    .content {
      margin-left: 80px; /* offset for fixed sidebar */
      flex: 1;
      padding: 2rem;
      overflow-y: auto;
      height: 100vh;
    }
  </style>