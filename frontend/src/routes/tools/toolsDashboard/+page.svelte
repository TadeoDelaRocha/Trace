<script>
    // Hard coded for now, we would fetch this from project information
    // TODO tool tip does not correctly overflow and is unreadable
    const tools = [
      {
        name: 'HTTP Tester',
        progress: 100,
        status: 'Completed',
        color: 'progress-green',
        action: 'View',
        tooltip: null,
        route: 'httpTester',
      },
      {
        name: 'SQL Injection',
        progress: 75,
        status: 'Error',
        color: 'progress-red',
        action: 'View',
        tooltip: null
      },
      {
        name: 'Parameter Fuzzing',
        progress: 30,
        status: 'Scanning...',
        color: 'progress-blue',
        action: 'Info',
        tooltip: null,
        route: 'fuzzer'
      },
      {
        name: 'Brute Force Tester',
        progress: 0,
        status: 'Ready to Go!',
        color: 'progress-gray',
        action: 'Set Up',
        tooltip: null
      },
      {
        name: 'Intruder',
        progress: 0,
        status: 'Ready to Go!',
        color: 'progress-gray',
        action: 'Set Up',
        tooltip: null
      },
      {
        name: 'Crawler',
        progress: 0,
        status: 'Ready to Go!',
        color: 'progress-gray',
        action: 'Set Up',
        tooltip: 'This is an example of a warning that might show up!'
      }
    ];

    function navigate(route) {
      window.location.href = route;
    }
  </script>
  
  <h1>Tools</h1>
  <h2>Base Perimeter Network</h2>
  
  {#each tools as tool}
    <div class="tool-row">
      <div class="tool-name">{tool.name}</div>
  
      <div class="progress-bar-container">
        <div class="progress-bar {tool.color}" style="width: {tool.progress}%"></div>
      </div>
  
      <div class="status-text">{tool.progress}% {tool.status}</div>
  
      {#if tool.tooltip}
        <div class="tooltip-container">
          <div class="tooltip-icon">i</div>
          <div class="tooltip-text">{tool.tooltip}</div> 
        </div>
      {/if}
  
      <div class="actions">
        <button on:click={() => navigate(`/tools/${tool.route}`)}>Info</button>
        <button class="action-button">{tool.action}</button>
      </div>
    </div>
  {/each}
  
  <button class="stop-button">Stop Project</button>
  
  <style>
    :global(body) {
      font-family: Arial, sans-serif;
      background-color: #f9fafb;
      padding: 40px;
    }
  
    h1 {
      font-size: 24px;
      margin-bottom: 4px;
    }
  
    h2 {
      font-size: 14px;
      color: #6b7280;
      margin-bottom: 20px;
    }
  
    .tool-row {
      display: flex;
      align-items: center;
      background-color: #fff;
      border-radius: 8px;
      padding: 16px;
      margin-bottom: 12px;
      box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
    }
  
    .tool-name {
      flex: 1;
      font-weight: 500;
    }
  
    .progress-bar-container {
      flex: 2;
      background-color: #e5e7eb;
      height: 12px;
      border-radius: 6px;
      margin-right: 12px;
      overflow: hidden;
    }
  
    .progress-bar {
      height: 12px;
      border-radius: 6px;
    }
  
    .progress-green {
      background-color: #22c55e;
    }
  
    .progress-red {
      background-color: #ef4444;
    }
  
    .progress-blue {
      background-color: #60a5fa;
    }
  
    .progress-gray {
      background-color: #d1d5db;
    }
  
    .status-text {
      font-size: 14px;
      color: #6b7280;
      width: 130px;
    }
  
    .tooltip-container {
      position: relative;
      margin-right: 8px;
    }
  
    .tooltip-icon {
      width: 22px;
      height: 22px;
      border-radius: 50%;
      background-color: #fee2e2;
      color: #dc2626;
      font-weight: bold;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 14px;
      cursor: default;
    }
  
    .tooltip-container:hover .tooltip-text {
      display: block;
    }
  
    .tooltip-text {
      display: none;
      position: absolute;
      top: 50%;
      left: 30px;
      transform: translateY(-50%);
      background-color: #fff;
      color: #111827;
      padding: 10px;
      font-size: 13px;
      border-radius: 4px;
      box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
      width: 260px;
      z-index: 10;
    }
  
    .actions {
      margin-left: auto;
      display: flex;
      gap: 10px;
    }
  
    .info-link {
      color: #3b82f6;
      font-size: 14px;
      text-decoration: none;
      padding-top: 2px;
    }
  
    .info-link:hover {
      text-decoration: underline;
    }
  
    .action-button {
      font-size: 14px;
      padding: 6px 14px;
      border: none;
      border-radius: 4px;
      background-color: #e5e7eb;
      cursor: pointer;
    }
  
    .action-button:hover {
      background-color: #d1d5db;
    }
  
    .stop-button {
      margin-top: 32px;
      padding: 10px 20px;
      background-color: #2563eb;
      color: white;
      border: none;
      border-radius: 6px;
      cursor: pointer;
    }
  
    .stop-button:hover {
      background-color: #1d4ed8;
    }
  </style>
  