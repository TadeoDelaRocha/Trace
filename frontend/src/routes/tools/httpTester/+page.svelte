<script lang="ts">
   import { ProxyServer, HTTPClient } from '$lib/ProxyServer';

let proxyServer = new ProxyServer();
let httpClient = new HTTPClient(proxyServer);

let requestUrl = '';
let requestMethod = 'GET';
let requestBody = '';
let headers = '';
let cookies = '';
let additionalParams = '';
let hideStatusCode = false;

let response = '';
let loading = false;
let history = { requests: [], responses: [] };
let logs: string[] = [];

function parseHeaders(headerString: string): Record<string, string> {
    return headerString
        .split('\n')
        .map(line => line.trim())
        .filter(line => line.includes(':'))
        .reduce((acc, line) => {
            const [key, value] = line.split(':').map(s => s.trim());
            acc[key] = value;
            return acc;
        }, {});
}

async function sendRequest() {
    loading = true;
    const config = {
        url: requestUrl,
        method: requestMethod,
        headers: parseHeaders(headers),
        body: requestBody,
        cookies,
        params: additionalParams,
    };
    response = await httpClient.sendRequestToProxy(config);
    history = proxyServer.getHistory();
    logs = httpClient.getLogs();
    loading = false;
}
</script>

<main>
    <h1>HTTP Tester</h1>
    <p class="subtext">Configuration</p>
  
    <div class="form-section">
        <input bind:value={requestUrl} placeholder="Target URL (e.g. https://example.com)" />
        <textarea bind:value={headers} placeholder="Headers (one per line: Key: Value)" rows="3"></textarea>
        <textarea bind:value={cookies} placeholder="Cookies" rows="2"></textarea>
        <textarea bind:value={additionalParams} placeholder="Additional Params (e.g. id=1&type=fast)" rows="2"></textarea>
        <textarea bind:value={requestBody} placeholder="Request Body (for POST/PUT)" rows="4"></textarea>
  
        <label>
            <input type="checkbox" bind:checked={hideStatusCode} />
            Hide Status Code
        </label>
  
        <p class="subtext">HTTP Method</p>
        <label><input type="radio" value="GET" bind:group={requestMethod} /> GET</label>
        <label><input type="radio" value="POST" bind:group={requestMethod} /> POST</label>
        <label><input type="radio" value="PUT" bind:group={requestMethod} /> PUT</label>
    
        <button on:click={sendRequest} disabled={loading}>
            {loading ? "Running..." : "Start"}
        </button>
    </div>
  
    {#if response}
        <h2>Response</h2>
        {#if response.startsWith("{") || response.startsWith("[")}
            <pre>{response}</pre>
        {:else}
            {@html response}
        {/if}
    {/if}
  
    <h2>Logs</h2>
    <ul>
        {#each logs as log}
            <li>{log}</li>
        {/each}
    </ul>
  
    <h2>Request History</h2>
    <ul>
        {#each history.requests as req, i}
            <li>{i + 1}: {req}</li>
        {/each}
    </ul>
  
    <h2>Response History</h2>
    <ul>
        {#each history.responses as res, i}
            <li>{i + 1}: {res}</li>
        {/each}
    </ul>
</main>

<style>
    main {
  max-width: 700px;
  margin: 2rem auto;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  padding: 2rem;
  background-color: #f9f9f9;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.05);
}

h1 {
  font-size: 2rem;
  margin-bottom: 1rem;
  font-weight: 600;
}

.subtext {
  font-size: 1rem;
  font-weight: 500;
  color: #888;
  margin-top: 2rem;
  margin-bottom: 0.5rem;
}

.form-section {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

input[type="text"],
input[type="url"],
textarea {
  padding: 0.75rem 1rem;
  border: 1px solid #ccc;
  border-radius: 10px;
  font-size: 1rem;
  width: 100%;
  box-sizing: border-box;
}

input[type="radio"],
input[type="checkbox"] {
  margin-right: 0.5rem;
}

label {
  font-size: 0.95rem;
  color: #333;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

button {
  margin-top: 1rem;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  background-color: #b6d3f2;
  color: #000;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

button:hover {
  background-color: #9ec3ee;
}

button:disabled {
  background-color: #d3d3d3;
  cursor: not-allowed;
}

pre {
  background-color: #eee;
  padding: 1rem;
  border-radius: 10px;
  overflow-x: auto;
}

ul {
  list-style-type: disc;
  padding-left: 1.5rem;
  color: #444;
}
</style>