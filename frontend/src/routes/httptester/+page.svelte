<script lang="ts">
   import { ProxyServer, HTTPClient } from '../../lib/ProxyServer';

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
